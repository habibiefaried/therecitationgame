import urllib
import os
import zipfile
from glob import glob

from python_speech_features import mfcc
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from PIL import Image

# ffmpeg -i test.ogg -ar 22050 test.wav

(rate,sig) = wav.read("test.wav")
mfcc_feat = mfcc(sig,rate,nfft=1024)

fig = plt.figure()
plt.plot(mfcc_feat)

imagename = "test"

fig.savefig(imagename+".png", dpi=fig.dpi,bbox_inches='tight')
im = Image.open(imagename+".png")
im = im.convert("RGB")
im = im.save(imagename+".jpg",'JPEG')
os.remove(imagename+".png")
plt.close()