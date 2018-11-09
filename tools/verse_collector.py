import urllib
import os
import sys
import zipfile
from glob import glob
import librosa
import numpy as np
import ConfigParser

counter = 126

configParser = ConfigParser.RawConfigParser()
configFilePath = r'../config/model.conf'
configParser.read(configFilePath)

isReDownload = True
if (configParser.get("ml-config", "redownload") == "0"):
	isReDownload = False

surah = int(configParser.get("ml-config","surah"))
total_ayah = int(configParser.get("ml-config","total_ayah"))

if (isReDownload):
	os.system("rm -rf ../audio/*") #clearing folder audio first
	counter = 1
else:
	if (counter == 0):
		print "Counter stil empty, should be set default"
		sys.exit(-1)

os.system("rm -rf ../dataset") #clearing folder dataset first

def download_1():
	global counter
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

	#from versebyverse quran
	rename_surah = "{0:0=3d}".format(surah)

	for url in urls:
		folder_t = "../audio/"+str(counter)
		os.system("mkdir -p "+folder_t)
		file_name = folder_t+"/"+rename_surah+".zip"

		print "Downloading: "+url+rename_surah+".zip"
		testfile = urllib.URLopener()
		testfile.retrieve(url+rename_surah+".zip", file_name)

		print "Unzipping..."
		zip_ref = zipfile.ZipFile(file_name, 'r')
		zip_ref.extractall(folder_t)
		zip_ref.close()

		counter = counter + 1

def download_2():
	#from https://verses.quran.com
	#from houseofquran.com
	import ssl

	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	global counter
	urls = [
		"https://verses.quran.com/AbdulBaset/Mujawwad/mp3/",
		"https://verses.quran.com/AbdulBaset/Murattal/mp3/",
		"https://verses.quran.com/Alafasy/mp3/",
		"https://verses.quran.com/Minshawi/Mujawwad/mp3/",
		"https://verses.quran.com/Minshawi/Murattal/mp3/",
		"https://verses.quran.com/Rifai/mp3/",
		"https://verses.quran.com/Shatri/mp3/",
		"https://verses.quran.com/Shuraym/mp3/",
		"https://verses.quran.com/Sudais/mp3/",
		"http://1c.houseofquran.com/Alafasy40kps1/",
		"http://1c.houseofquran.com/MinshaweeMurtal1/",
		"http://1c.houseofquran.com/Hussary1/",
		"http://1c.houseofquran.com/HusaryFaster/",
		"http://1c.houseofquran.com/HussaryMualim/",
		"http://1c.houseofquran.com/Basit40kbps1/",
		"http://1c.houseofquran.com/Gamedi1/",
		"http://1c.houseofquran.com/Hudhaify_32kbps/",
		"http://1c.houseofquran.com/Mostafa_Ismail_128kbps/",
		"http://1c.houseofquran.com/tunaiji_64kbps/",
		"http://1c.houseofquran.com/mahmoud_ali_al_banna_32kbps/",
		"http://1c.houseofquran.com/Ayman_Sowaid_64kbps/",
		"http://1c.houseofquran.com/tunaiji_teacher/",
		"http://1c.houseofquran.com/Ibrahim_Akhdar_32kbps/",
		"http://1c.houseofquran.com/Muhammad_Ayyoub_64kbps/",
		"http://1c.houseofquran.com/Hani_Rifai_192kbps/",
		"http://1c.houseofquran.com/Abdurrahmaan_As-Sudais_64kbps/",
		"http://1c.houseofquran.com/Abdullaah_3awwaad_Al-Juhaynee_128kbps/",
		"http://1c.houseofquran.com/Maher_AlMuaiqly_64kbps/",
		"http://1c.houseofquran.com/Minshawy_Mujawwad_64kbps/",
		"http://1c.houseofquran.com/Abu_Bakr_Ash-Shaatree_64kbps/",
		"http://1c.houseofquran.com/Ahmed_ibn_Ali_al-Ajamy_64kbps/",
		"http://1c.houseofquran.com/Muhammad_Jibreel_64kbps/",
		"http://1c.houseofquran.com/Mohammad_al_Tablaway_64kbps/",
		"http://1c.houseofquran.com/Yaser_Salamah_128kbps/",
		"http://1c.houseofquran.com/Muhsin_Al_Qasim_192kbps/",
		"http://1c.houseofquran.com/Nasser_Alqatami_128kbps/",
		"http://1c.houseofquran.com/warsh_husary_64kbps/",
		"http://1c.houseofquran.com/warsh/warsh_ibrahim_aldosary_128kbps/",
		"http://audio.recitequran.com/vbv/arabic/abdul-basit_abdus-samad_murattal/",
		"http://audio.recitequran.com/vbv/arabic/abdul-basit_abdus-samad_mujawwad/",
		"http://audio.recitequran.com/vbv/arabic/abdul-muhsin_al-qasim/",
		"http://audio.recitequran.com/vbv/arabic/abdullah_awwad_al-juhani/",
		"http://audio.recitequran.com/vbv/arabic/abdullah_basfar/",
		"http://audio.recitequran.com/vbv/arabic/abdullah_matroud/",
		"http://audio.recitequran.com/vbv/arabic/abdur-rahman_as-sudais/",
		"http://audio.recitequran.com/vbv/arabic/abu_bakr_ash-shatiri/",
		"http://audio.recitequran.com/vbv/arabic/ahmad_al-ajmi/",
		"http://audio.recitequran.com/vbv/arabic/ali_al-hudthayfi/",
		"http://audio.recitequran.com/vbv/arabic/ali_hajjaj_as-suwaysi/",
		"http://audio.recitequran.com/vbv/arabic/ali_jabir/",
		"http://audio.recitequran.com/vbv/arabic/hani_ar-rifai/",
		"http://audio.recitequran.com/vbv/arabic/ibrahim_al-akhdar/",
		"http://audio.recitequran.com/vbv/arabic/jazza_as-suwaylih/",
		"http://audio.recitequran.com/vbv/arabic/khalid_abdullah_al-qahtani/",
		"http://audio.recitequran.com/vbv/arabic/khalifah_at-tunayji/",
		"http://audio.recitequran.com/vbv/arabic/maher_al-muayqli/",
		"http://audio.recitequran.com/vbv/arabic/mahmoud_ali_al-banna/",
		"http://audio.recitequran.com/vbv/arabic/mahmoud_khalil_al-husari_mujawwad/",
		"http://audio.recitequran.com/vbv/arabic/mahmoud_khalil_al-husari_murattal/",
		"http://audio.recitequran.com/vbv/arabic/mahmoud_khalil_al-husari_teacher/",
		"http://audio.recitequran.com/vbv/arabic/mishary_al-afasy/",
		"http://audio.recitequran.com/vbv/arabic/muhammad_abdul-karim/",
		"http://audio.recitequran.com/vbv/arabic/muhammad_at-tablawi/",
		"http://audio.recitequran.com/vbv/arabic/muhammad_ayyoub/",
		"http://audio.recitequran.com/vbv/arabic/muhammad_jibril/",
		"http://audio.recitequran.com/vbv/arabic/muhammad_siddiq_al-minshawi_mujawwad/",
		"http://audio.recitequran.com/vbv/arabic/muhammad_siddiq_al-minshawi_murattal/",
		"http://audio.recitequran.com/vbv/arabic/muhammad_siddiq_al-minshawi_teacher/",
		"http://audio.recitequran.com/vbv/arabic/nasir_al-qatami/",
		"http://audio.recitequran.com/vbv/arabic/sad_al-ghamidi/",
		"http://audio.recitequran.com/vbv/arabic/saud_ash-shuraim/",
		"http://audio.recitequran.com/vbv/arabic/salah_al-budair/",
		"http://audio.recitequran.com/vbv/arabic/salah_bukhatir/",
		"http://audio.recitequran.com/vbv/arabic/yasir_salamah/",
		"http://tanzil.net/res/audio/abdulbasit/",
		"http://tanzil.net/res/audio/abdulbasit-mjwd/",
		"http://tanzil.net/res/audio/afasy/",
		"http://tanzil.net/res/audio/ajamy/",
		"http://tanzil.net/res/audio/akhdar/",
		"http://tanzil.net/res/audio/ghamadi/",
		"http://tanzil.net/res/audio/hudhaify/",
		"http://tanzil.net/res/audio/husary/",
		"http://tanzil.net/res/audio/husary-mjwd/",
		"http://tanzil.net/res/audio/juhany/",
		"http://tanzil.net/res/audio/matrood/",
		"http://tanzil.net/res/audio/minshawi/",
		"http://tanzil.net/res/audio/minshawi-mjwd/",
		"http://tanzil.net/res/audio/muaiqly/",
		"http://tanzil.net/res/audio/qasim/",
		"http://tanzil.net/res/audio/hani/",
		"http://tanzil.net/res/audio/sudais/",
		"http://tanzil.net/res/audio/shateri/",
		"http://tanzil.net/res/audio/shuraim/",
		"http://tanzil.net/res/audio/tablawi/",
		"http://tanzil.net/res/audio/basfar/",
		"http://tanzil.net/res/audio/basfar2/",
		"http://tanzil.net/res/audio/bukhatir/",
		"http://tanzil.net/res/audio/ayyub/",
		"http://tanzil.net/res/audio/jibreel/",
		"http://tanzil.net/res/audio/parhizgar/",

	]

	for url in urls:
		folder_t = "../audio/"+str(counter)+"/"
		os.system("mkdir -p "+folder_t)

		print "Downloading "+url

		for ayah in range(1,total_ayah+1):
			testfile = urllib.URLopener(context=ctx)
			file_name = "{0:0=3d}".format(surah)+"{0:0=3d}".format(ayah)+".mp3"
			testfile.retrieve(url+file_name,folder_t+file_name)

		counter = counter+1

def analysis(max_pad_len=512):
	global counter
	os.system("mkdir ../dataset")
	for ayah in range(1,total_ayah+1):
		mfcc_vectors = []

		for reciter in range(1,counter):
			#Analysis take
			print "[+]  progress: "+str(reciter)+"-"+"{0:0=3d}".format(ayah)
			wave, sr = librosa.load("../audio/"+str(reciter)+"/"+"{0:0=3d}".format(surah)+"{0:0=3d}".format(ayah)+".mp3.wav", mono=True, sr=None)
		    	wave = wave[::3]
		    	mfcc = librosa.feature.mfcc(wave, sr)
			print "[+] Detected pad_len : "+str(mfcc.shape[1])
		    	pad_width = max_pad_len - mfcc.shape[1]
		    	mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')

			#append to mfcc_vectors
			mfcc_vectors.append(mfcc)

		np.save("../dataset/ayat-"+str(ayah)+".npy", mfcc_vectors)


if (isReDownload):
	download_1()
	download_2()
else:
	print "Skipping download"

print "Converting all of the mp3 files to wav..."
result = [y for x in os.walk("../audio") for y in glob(os.path.join(x[0], '*.mp3'))]

for r in result:
	print "Processing: ffmpeg -i "+r+" -acodec pcm_u8 -filter:a loudnorm -ar 22050 -af 'highpass=f=200, lowpass=f=3000' -y "+r+".wav > /dev/null 2>&1"
	os.system("ffmpeg -i "+r+" -acodec pcm_u8 -filter:a loudnorm -ar 22050 -af 'highpass=f=200, lowpass=f=3000' -y "+r+".wav > /dev/null 2>&1")

analysis()
