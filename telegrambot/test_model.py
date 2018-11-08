#!/usr/bin/python
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
total_ayah = int(configParser.get("ml-config

def wav2mfcc(file_path, max_pad_len=512):
#Generate mfcc from wav
    wave, sr = librosa.load(file_path, mono=True, sr=None)
    wave = wave[::3]
    mfcc = librosa.feature.mfcc(wave)
    pad_width = max_pad_len - mfcc.shape[1]
    mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    return mfcc

def load():
    print "Loading model..."

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


