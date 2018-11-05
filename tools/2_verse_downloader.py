import urllib
import os
import zipfile
from glob import glob
import librosa
import numpy as np

isReDownload = True
surah = 1 
total_ayah = 7

if (isReDownload):
	os.system("rm -rf ../audio/*") #clearing folder audio first

os.system("rm -rf ../dataset/*") #clearing folder dataset first

def download(urls):
	i = 1
	folder_t = "../audio/"+str(i)
	rename_surah = "{0:0=3d}".format(surah)

	for url in urls:
		os.system("mkdir -p "+folder_t)
		file_name = folder_t+"/"+rename_surah+".zip"

		print "Downloading: "+url+rename_surah+".zip"
		testfile = urllib.URLopener()
		testfile.retrieve(url+rename_surah+".zip", file_name)

		print "Unzipping..."
		zip_ref = zipfile.ZipFile(file_name, 'r')
		zip_ref.extractall(folder_t)
		zip_ref.close()

		i = i + 1

def analysis(max_pad_len=11):
	for ayah in range(1,total_ayah+1):
		mfcc_vectors = []

		for reciter in range(1,len(urls)+1):	
			#Analysis take 
			print "[+]  progress: "+str(reciter)+"-"+"{0:0=3d}".format(ayah)
			wave, sr = librosa.load("../audio/"+str(reciter)+"/"+"{0:0=3d}".format(surah)+"{0:0=3d}".format(ayah)+".mp3.wav", mono=True, sr=None)
		    wave = wave[::3]
		    mfcc = librosa.feature.mfcc(wave, sr)
		    pad_width = max_pad_len - mfcc.shape[1]
		    mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
			
			#append to mfcc_vectors
			mfcc_vectors.append(mfcc)

		np.save("../dataset/ayat-"+str(ayah)+".npy", mfcc_vectors)

urls = [		
		"http://www.everyayah.com/data/Abdul_Basit_Murattal_64kbps/zips/",
		"http://www.everyayah.com/data/Abdullah_Basfar_64kbps/zips/",
		"http://www.everyayah.com/data/Abdurrahmaan_As-Sudais_64kbps/zips/",
		"http://www.everyayah.com/data/Abu_Bakr_Ash-Shaatree_64kbps/zips/",
		"http://www.everyayah.com/data/Ahmed_ibn_Ali_al-Ajamy_64kbps_QuranExplorer.Com/zips/",
		"http://www.everyayah.com/data/Alafasy_64kbps/zips/",
		"http://www.everyayah.com/data/Hani_Rifai_64kbps/zips/",
		"http://www.everyayah.com/data/Hudhaify_64kbps/zips/",
		"http://www.everyayah.com/data/Husary_64kbps/zips/",
		"http://www.everyayah.com/data/Maher_AlMuaiqly_64kbps/zips/",
		"http://www.everyayah.com/data/Mohammad_al_Tablaway_64kbps/zips/",
		"http://www.everyayah.com/data/Muhammad_Jibreel_64kbps/zips/",
		"http://www.everyayah.com/data/Saood_ash-Shuraym_64kbps/zips/","http://www.everyayah.com/data/Abdul_Basit_Mujawwad_128kbps/zips/",
		"http://www.everyayah.com/data/Abdullaah_3awwaad_Al-Juhaynee_128kbps/zips/",
		"http://www.everyayah.com/data/Abdullah_Basfar_192kbps/zips/",
		"http://www.everyayah.com/data/Abdullah_Matroud_128kbps/zips/",
		"http://www.everyayah.com/data/Abdurrahmaan_As-Sudais_192kbps/zips/",
		"http://www.everyayah.com/data/Abu_Bakr_Ash-Shaatree_128kbps/zips/",
		"http://www.everyayah.com/data/Ahmed_Neana_128kbps/zips/",
		"http://www.everyayah.com/data/Ahmed_ibn_Ali_al-Ajamy_128kbps_ketaballah.net/zips/",
		"http://www.everyayah.com/data/Akram_AlAlaqimy_128kbps/zips/",
		"http://www.everyayah.com/data/Alafasy_128kbps/zips/",
		"http://www.everyayah.com/data/Ali_Hajjaj_AlSuesy_128kbps/zips/",
		"http://www.everyayah.com/data/Ali_Jaber_64kbps/zips/",
		"http://www.everyayah.com/data/Fares_Abbad_64kbps/zips/",
		"http://www.everyayah.com/data/Ghamadi_40kbps/zips/",
		"http://www.everyayah.com/data/Hani_Rifai_192kbps/zips/",
		"http://www.everyayah.com/data/Hudhaify_128kbps/zips/",
		"http://www.everyayah.com/data/Husary_128kbps/zips/",
		"http://www.everyayah.com/data/Husary_Muallim_128kbps/zips/",
		"http://www.everyayah.com/data/Husary_Mujawwad_64kbps/zips/",
		"http://www.everyayah.com/data/Karim_Mansoori_40kbps/zips/",
		"http://www.everyayah.com/data/Khaalid_Abdullaah_al-Qahtaanee_192kbps/zips/",
		"http://www.everyayah.com/data/MaherAlMuaiqly128kbps/zips/",
		"http://www.everyayah.com/data/Menshawi_16kbps/zips/",
		"http://www.everyayah.com/data/Muhammad_AbdulKareem_128kbps/zips/",
		"http://www.everyayah.com/data/Muhammad_Ayyoub_128kbps/zips/",
		"http://www.everyayah.com/data/Muhammad_Jibreel_64kbps/zips/",
		"http://www.everyayah.com/data/Muhsin_Al_Qasim_192kbps/zips/",
		"http://www.everyayah.com/data/Nasser_Alqatami_128kbps/zips/",
		"http://www.everyayah.com/data/Sahl_Yassin_128kbps/zips/",
		"http://www.everyayah.com/data/Salaah_AbdulRahman_Bukhatir_128kbps/zips/",
		"http://www.everyayah.com/data/Salah_Al_Budair_128kbps/zips/",
		"http://www.everyayah.com/data/Yaser_Salamah_128kbps/zips/",
		"http://www.everyayah.com/data/aziz_alili_128kbps/zips/",
		"http://www.everyayah.com/data/Hudhaify_32kbps/zips/",
		"http://www.everyayah.com/data/ahmed_ibn_ali_al_ajamy_128kbps/zips/",
		"http://www.everyayah.com/data/Yasser_Ad-Dussary_128kbps/zips/",
		"http://www.everyayah.com/data/mahmoud_ali_al_banna_32kbps/zips/",
		"http://www.everyayah.com/data/khalefa_al_tunaiji_64kbps/zips/",
		]

if (isReDownload):
	download(urls)
else:
	print "Skipping download"

print "Converting all of the files to wav..."
result = [y for x in os.walk("../audio") for y in glob(os.path.join(x[0], '*.mp3'))]

for r in result:
	print "Processing: ffmpeg -i "+r+" -acodec pcm_u8 -ar 22050 "+r+".wav > /dev/null 2>&1"
	os.system("ffmpeg -i "+r+" -acodec pcm_u8 -ar 22050 "+r+".wav > /dev/null 2>&1")

analysis()
