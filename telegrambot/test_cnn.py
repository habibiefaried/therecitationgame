import ConfigParser
import librosa
import numpy as np

from sklearn.model_selection import train_test_split
from keras.models import load_model
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import backend as K
from pprint import pprint

configParser = ConfigParser.RawConfigParser()
configFilePath = r'../config/model.conf'
configParser.read(configFilePath)
channel = 1

surah = int(configParser.get("ml-config","surah"))
total_ayah = int(configParser.get("ml-config","total_ayah"))

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

def get_labels():
	labels = []
	for i in range(1, total_ayah+1):
		labels.append("ayat-"+str(i))

	label_indices = np.arange(0, len(labels))
	return labels, label_indices, to_categorical(label_indices)

model = load_model("../generatedmodel/surah-"+str(surah)+"-model.h5",custom_objects={"f1": f1, "precision": precision})

def isCorrect(location, label):
	sample = wav2mfcc(location)
	sample_reshaped = sample.reshape(1, int(configParser.get("ml-config","shape_1")), int(configParser.get("ml-config","shape_2")), channel)
	answer = get_labels()[0][np.argmax(model.predict(sample_reshaped))]
	print("[DEBUG] Predicted label: "+answer+". Actual Label: ayat-"+label)
	if (answer == "ayat-"+label):
		return True
	else:
		return False

def testing():
	for i in range(1,total_ayah+1):
		sample = wav2mfcc("../testing/"+str(surah)+"/"+str(i)+".wav")
        	sample_reshaped = sample.reshape(1, int(configParser.get("ml-config","shape_1")), int(configParser.get("ml-config","shape_2")), channel)
		answer = get_labels()[0][np.argmax(model.predict(sample_reshaped))]
       		print("Predicted label: "+answer+". Actual Label: ayat-"+str(i))

def load():
	if (str(type(model)) == "<class 'keras.engine.sequential.Sequential'>"):
		print "Model is loaded!"
