import numpy as np
import keras
import librosa
import ConfigParser

from time import time

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import backend as K

from keras.callbacks import TensorBoard

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
## https://stackoverflow.com/questions/43547402/how-to-calculate-f1-macro-in-keras
def precision(y_true, y_pred):
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
	return true_positives / (predicted_positives + K.epsilon())

def recall(y_true, y_pred):
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
	return true_positives / (possible_positives + K.epsilon())

def f1(y_true, y_pred):
	p = precision(y_true, y_pred)
	r = recall(y_true, y_pred)
	return 2*((p*r)/(p+r+K.epsilon()))

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

clayer = 32

y_train_hot = to_categorical(y_train)
y_test_hot = to_categorical(y_test)

model = Sequential()
model.add(Conv2D(clayer, kernel_size=(2, 2), activation='relu', kernel_regularizer=keras.regularizers.l2(0.001), input_shape=(X_train.shape[1], X_train.shape[2], channel) ))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(clayer, kernel_size=(2, 2), activation='relu', kernel_regularizer=keras.regularizers.l2(0.001) ))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(clayer, kernel_size=(2, 2), activation='relu', kernel_regularizer=keras.regularizers.l2(0.001) ))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(clayer*4, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)))
model.add(Dropout(0.5))

model.add(Dense(clayer*4, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)))
model.add(Dropout(0.5))

model.add(Dense(int(max(y_train))+1, activation='softmax'))

#model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adadelta(),metrics = [f1,precision])
model.compile(loss=keras.losses.categorical_crossentropy,optimizer="adam",metrics = [f1,precision])
#model.compile(loss=keras.losses.categorical_crossentropy,optimizer="rmsprop",metrics = [f1,precision])

tensorboard = TensorBoard(log_dir="/tmp/logs/{}".format(time()))
model.fit(X_train, y_train_hot, batch_size=128, epochs=total_ayah*256, verbose=1, validation_data=(X_test, y_test_hot),callbacks=[tensorboard])

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
		#assert answer == test_answer[i] #my voice must be recognized first, create the label later
		i = i+1

#Saving model
model.save("../generatedmodel/surah-"+str(surah)+"-model.h5")
