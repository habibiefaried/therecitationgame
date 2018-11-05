from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from preprocess import *
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils import to_categorical
import functools
from keras import backend as K
import tensorflow as tf
import librosa

channel = 1 #Assumption

def wav2mfcc(file_path, max_pad_len=512):
#Generate mfcc from wav
	wave, sr = librosa.load(file_path, mono=True, sr=None)
	wave = wave[::3]
	mfcc = librosa.feature.mfcc(wave)
	pad_width = max_pad_len - mfcc.shape[1]
	mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
	return mfcc

def precision(y_true, y_pred):
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
	precision = true_positives / (predicted_positives + K.epsilon())
	return precision

# Input: Folder Path
# Output: Tuple (Label, Indices of the labels, one-hot encoded labels)
def get_labels(path="../dataset/"):
	labels = os.listdir(path)
	label_indices = np.arange(0, len(labels))
	return labels, label_indices, to_categorical(label_indices)

def get_train_test(path="../dataset/", split_ratio=0.8, random_state=42):
    # Get available labels
    labels, indices, _ = get_labels(path)

    # Getting first arrays
    X = np.load(path+labels[0])
    y = np.zeros(X.shape[0])

    # Append all of the dataset into one single array, same goes for y
    for i, label in enumerate(labels[1:]):
        x = np.load(path+label)
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
model.add(Conv2D(32, kernel_size=(2, 2), activation='relu', input_shape=(X_train.shape[1], X_train.shape[2], channel)))
model.add(Conv2D(48, kernel_size=(2, 2), activation='relu'))
model.add(Conv2D(120, kernel_size=(2, 2), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(int(max(y_train))+1, activation='softmax'))
#model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adadelta(),metrics = [as_keras_metric(tf.metrics.precision)])
model.compile(loss=keras.losses.categorical_crossentropy,optimizer="adam",metrics = [precision])

model.fit(X_train, y_train_hot, batch_size=128, epochs=1024, verbose=1, validation_data=(X_test, y_test_hot))
