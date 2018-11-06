#from preprocess import *
import numpy as np
import keras
import librosa
import ConfigParser

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import backend as K


configParser = ConfigParser.RawConfigParser()
configFilePath = r'../config/model.conf'
configParser.read(configFilePath)

surah = int(configParser.get("ml-config","surah"))
total_ayah = int(configParser.get("ml-config","total_ayah"))
channel = 1 #treat wave as 1 channel image

def wav2mfcc(file_path, max_pad_len=512):
#Generate mfcc from wav
	wave, sr = librosa.load(file_path, mono=True, sr=None)
	wave = wave[::3]
	mfcc = librosa.feature.mfcc(wave)
	pad_width = max_pad_len - mfcc.shape[1]
	mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
	return mfcc

# Metrics
## Ref: https://github.com/GeekLiB/keras/blob/master/keras/metrics.py
def precision(y_true, y_pred):
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
	precision = true_positives / (predicted_positives + K.epsilon())
	return precision

def recall(y_true, y_pred):
    '''Calculates the recall, a metric for multi-label classification of
    how many relevant items are selected.
    '''
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def fbeta_score(y_true, y_pred, beta=1):
    '''Calculates the F score, the weighted harmonic mean of precision and recall.
    This is useful for multi-label classification, where input samples can be
    classified as sets of labels. By only using accuracy (precision) a model
    would achieve a perfect score by simply assigning every class to every
    input. In order to avoid this, a metric should penalize incorrect class
    assignments as well (recall). The F-beta score (ranged from 0.0 to 1.0)
    computes this, as a weighted mean of the proportion of correct class
    assignments vs. the proportion of incorrect class assignments.
    With beta = 1, this is equivalent to a F-measure. With beta < 1, assigning
    correct classes becomes more important, and with beta > 1 the metric is
    instead weighted towards penalizing incorrect class assignments.
    '''
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')
        
    # If there are no true positives, fix the F score at 0 like sklearn.
    if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
        return 0

    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    bb = beta ** 2
    fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
    return fbeta_score

# Input: Folder Path
# Output: Tuple (Label, Indices of the labels, one-hot encoded labels)
def get_labels():
	labels = []
	for i in range(1, total_ayah+1):
		labels.append("ayat-"+str(i))

	label_indices = np.arange(0, len(labels))
	return labels, label_indices, to_categorical(label_indices)

def get_train_test(split_ratio=0.75, random_state=42):
    # Get available labels
    labels, indices, _ = get_labels()

    # Getting first arrays
    X = np.load("../dataset/"+labels[0]+".npy")
    y = np.zeros(X.shape[0])

    # Append all of the dataset into one single array, same goes for y
    for i, label in enumerate(labels[1:]):
        x = np.load("../dataset/"+label+".npy")
        X = np.vstack((X, x))
        y = np.append(y, np.full(x.shape[0], fill_value= (i + 1)))

    assert X.shape[0] == len(y)

    return train_test_split(X, y, test_size= (1 - split_ratio), random_state=random_state, shuffle=True)

X_train, X_test, y_train, y_test = get_train_test()

# Reshaping to perform 2D convolution
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], channel)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], channel)

#Make sure dimension is same
assert X_train.shape[1] == X_test.shape[1]
assert X_train.shape[2] == X_test.shape[2]

y_train_hot = to_categorical(y_train)
y_test_hot = to_categorical(y_test)

model = Sequential()
model.add(Conv2D(16, kernel_size=(2, 2), activation='relu', kernel_regularizer=keras.regularizers.l2(0.001), input_shape=(X_train.shape[1], X_train.shape[2], channel) ))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(16, kernel_size=(2, 2), activation='relu', kernel_regularizer=keras.regularizers.l2(0.001) ))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(16, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)))
model.add(Dropout(0.5))

model.add(Dense(16, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)))
model.add(Dropout(0.5))

model.add(Dense(int(max(y_train))+1, activation='softmax'))

#model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0),metrics = [precision])
model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adadelta(lr=0.5, rho=0.95, epsilon=1e-08, decay=0.0),metrics = [fbeta_score(beta=0.5)])

learning_rate_reduction = keras.callbacks.ReduceLROnPlateau(monitor='val_loss',patience=5,verbose=1,factor=0.5,min_lr=0.001)

model.fit(X_train, y_train_hot, batch_size=128, epochs=1024, verbose=1, validation_data=(X_test, y_test_hot))

### Testing
# Getting the MFCC
from pprint import pprint
test_list = [
		"../testing/"+str(surah)+"/test.wav",
		"../testing/"+str(surah)+"/test2.wav",
		"../testing/"+str(surah)+"/001003.mp3.wav",
		"../testing/"+str(surah)+"/001005.mp3.wav",
		"../testing/outlier.wav"
		]
test_answer = [
		"ayat-1",
		"ayat-1",
		"ayat-3",
		"ayat-5",
]

i = 0

for t in test_list:
	sample = wav2mfcc(t)
	sample_reshaped = sample.reshape(1, X_train.shape[1], X_train.shape[2], channel)
	pprint(model.predict(sample_reshaped))
	answer = get_labels()[0][np.argmax(model.predict(sample_reshaped))]
	print("Predicted label: "+answer)
	if (t != "../testing/outlier.wav"): #no need to assert outlier
		assert answer == test_answer[i] #my voice must be recognized first, create the label later
		i = i+1

#Saving model
model.save("../generatedmodel/surah-"+str(surah)+"-model.h5")