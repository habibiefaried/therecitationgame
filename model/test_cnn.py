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


model = load_model("../generatedmodel/surah-"+str(surah)+"-model.h5",custom_objects={"f1": f1, "precision": precision})
X_train, X_test, y_train, y_test = get_train_test()

for i in range(1,total_ayah+1):
        sample = wav2mfcc("../testing/"+str(surah)+"/"+str(i)+".wav")
        sample_reshaped = sample.reshape(1, X_train.shape[1], X_train.shape[2], channel)
        answer = get_labels()[0][np.argmax(model.predict(sample_reshaped))]
        print("Predicted label: "+answer+". Actual Label: ayat-"+str(i))
