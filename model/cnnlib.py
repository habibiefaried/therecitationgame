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

class cnnlib:
	def __init__(self):
		self.configParser = ConfigParser.RawConfigParser()
		self.configFilePath = r'../config/model.conf'
		self.configParser.read(self.configFilePath)
		self.channel = 1

		self.surah = int(self.configParser.get("ml-config","surah"))
		self.total_ayah = int(self.configParser.get("ml-config","total_ayah"))

		self.model = load_model("../generatedmodel/surah-"+str(self.surah)+"-model.h5",custom_objects={"f1": self.f1, "precision": self.precision})

	def wav2mfcc(self, file_path, max_pad_len=int(self.configParser.get("ml-config", "max_pad_len"))):
		#Generate mfcc from wav
        	#wave, sr = librosa.load(file_path, mono=True, sr=None)
        	#wave = wave[::3]
        	
			y, sr = librosa.load("../audio/"+str(reciter)+"/"+"{0:0=3d}".format(surah)+"{0:0=3d}".format(ayah)+".mp3.wav")
			y = librosa.effects.harmonic(y)
			mfcc = librosa.feature.tonnetz(y=y, sr=sr) #this is tonnetz, but i'm too lazy to change

        	pad_width = max_pad_len - mfcc.shape[1]
        	mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
        	return mfcc

	# Metrics
	## https://stackoverflow.com/questions/43547402/how-to-calculate-f1-macro-in-keras
	def precision(self, y_true, y_pred):
        	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        	predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        	return true_positives / (predicted_positives + K.epsilon())

	def recall(self,y_true, y_pred):
        	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        	possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        	return true_positives / (possible_positives + K.epsilon())

	def f1(self, y_true, y_pred):
        	p = self.precision(y_true, y_pred)
        	r = self.recall(y_true, y_pred)
        	return 2*((p*r)/(p+r+K.epsilon()))

	def get_labels(self):
		labels = []
		for i in range(1, self.total_ayah+1):
			labels.append("ayat-"+str(i))

		label_indices = np.arange(0, len(labels))
		return labels, label_indices, to_categorical(label_indices)

	def isCorrect(self, location, label):
		print "Loading "+location+" ..."
		sample = self.wav2mfcc(location)
		sample_reshaped = sample.reshape(1, int(self.configParser.get("ml-config","shape_1")), int(self.configParser.get("ml-config","shape_2")), self.channel)
		answer = self.get_labels()[0][np.argmax(self.model.predict(sample_reshaped))]

		print("[DEBUG] Predicted label: "+answer+". Actual Label: ayat-"+label)
		if (answer == "ayat-"+label):
			return True
		else:
			return False

	def test(self):
		for i in range(1,self.total_ayah+1):
			sample = self.wav2mfcc("../testing/"+str(self.surah)+"/"+str(i)+".wav")
        		sample_reshaped = sample.reshape(1, int(self.configParser.get("ml-config","shape_1")), int(self.configParser.get("ml-config","shape_2")), self.channel)
			answer = self.get_labels()[0][np.argmax(self.model.predict(sample_reshaped))]
       			print("Predicted label: "+answer+". Actual Label: ayat-"+str(i))
