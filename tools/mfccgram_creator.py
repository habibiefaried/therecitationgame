from python_speech_features import mfcc
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from PIL import Image
import os

total_surah = 96
total_ayah = 19
total_reciter = 11

for reciter in range(1,total_reciter+1):
	for ayah in range(1,total_ayah+1):
		print "Progress: "+str(reciter)+"-"+"{0:0=3d}".format(ayah)
		(rate,sig) = wav.read("dataset/audio/"+str(reciter)+"/"+"{0:0=3d}".format(total_surah)+"{0:0=3d}".format(ayah)+".mp3.wav")
		mfcc_feat = mfcc(sig,rate,nfft=1024)

		fig = plt.figure()
		plt.plot(mfcc_feat)

		imagename = "dataset/mfcc/"+str(ayah)+"/"+str(ayah)+"."+str(reciter)

		fig.savefig(imagename+".png", dpi=fig.dpi,bbox_inches='tight')
		im = Image.open(imagename+".png")
		im = im.convert("RGB")
		im = im.save(imagename+".jpg",'JPEG')
		os.remove(imagename+".png")
		plt.close()