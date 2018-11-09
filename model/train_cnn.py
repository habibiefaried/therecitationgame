import numpy as np
import keras
import ConfigParser
import os

from time import time

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import backend as K

from keras.callbacks import TensorBoard
from cnnlib import cnnlib

configParser = ConfigParser.RawConfigParser()
configFilePath = r'../config/model.conf'
configParser.read(configFilePath)

surah = int(configParser.get("ml-config","surah"))
total_ayah = int(configParser.get("ml-config","total_ayah"))
channel = 1 #treat wave as 1 channel image

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

def get_train_test(split_ratio=0.6, random_state=42):
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

#Write to config file after assertion done
configParser.set("ml-config","shape_1",X_train.shape[1])
configParser.set("ml-config","shape_2",X_train.shape[2])
with open(configFilePath, 'wb') as configfile:
	configParser.write(configfile)

clayer = 8

dropout_ratio = 0.5
reg_score = 0.001

y_train_hot = to_categorical(y_train)
y_test_hot = to_categorical(y_test)

opts_list = [keras.optimizers.Adadelta(), keras.optimizers.RMSprop(), keras.optimizers.Adam(), keras.optimizers.SGD()]
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.system("rm -rf /tmp/logs/*")

for o in opts_list:
	model = Sequential()
	model.add(Conv2D(clayer, kernel_size=(2, 2), activation='relu', input_shape=(X_train.shape[1], X_train.shape[2], channel), kernel_regularizer=keras.regularizers.l2(reg_score) ))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(dropout_ratio))

	#model.add(Conv2D(clayer, kernel_size=(2, 2), activation='relu', kernel_regularizer=keras.regularizers.l2(reg_score)))
	#model.add(MaxPooling2D(pool_size=(2, 2)))
	#model.add(Dropout(dropout_ratio))

	model.add(Flatten())

	model.add(Dense(clayer*2, activation='relu' , kernel_regularizer=keras.regularizers.l2(reg_score)))
	model.add(Dropout(dropout_ratio))
	model.add(Dense(int(max(y_train))+1, activation='softmax'))

	model.compile(loss=keras.losses.categorical_crossentropy,optimizer=o,metrics = [f1,precision])

	tensorboard = TensorBoard(log_dir="/tmp/logs/{}".format(time()))
	model.fit(X_train, y_train_hot, batch_size=1024, epochs=512, validation_data=(X_test, y_test_hot),callbacks=[tensorboard], verbose=0)

	#Saving model
	model.save("../generatedmodel/surah-"+str(surah)+"-model.h5")

	print "============"
	C = cnnlib()
	C.test()
