import urllib
import os
import zipfile
from glob import glob
import matplotlib
matplotlib.use('Agg')

from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from PIL import Image
import librosa
import librosa.display
import numpy as np
import wave

FILENAME = "test.wav"
# ffmpeg -i test.ogg -ar 22050 FILENAME

# using python_speech lib
(rate,sig) = wav.read(FILENAME)
mfcc_feat = mfcc(sig,rate,nfft=1024)
fig = plt.figure()
plt.plot(mfcc_feat)

#using librosa lib
#hop_length = 512
#y, sr = librosa.load(FILENAME)
#y_harmonic, y_percussive = librosa.effects.hpss(y)
#tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,sr=sr)
#mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
#mfcc_delta = librosa.feature.delta(mfcc)
#beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),beat_frames)
#chromagram = librosa.feature.chroma_cqt(y=y_harmonic,sr=sr)
#beat_chroma = librosa.util.sync(chromagram,beat_frames,aggregate=np.median)
#music_graph = np.vstack([beat_chroma, beat_mfcc_delta])

#(rate,sig) = wav.read(FILENAME)
#fbank_feat = logfbank(sig,rate,nfft=1024)
#fig = plt.figure()
#plt.plot(fbank_feat)

imagename = FILENAME

fig.savefig(imagename+".png", dpi=fig.dpi,bbox_inches='tight')
im = Image.open(imagename+".png")
im = im.convert("RGB")
im = im.save(imagename+".jpg",'JPEG')
os.remove(imagename+".png")
plt.close()