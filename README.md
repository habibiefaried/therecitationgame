# Description
Quranic sound recognizer to detect any wrong recitation using Deep Learning technique

# Telegram Bot
Available on telegram with username @the_recitation_bot

Link: https://telegram.me/the_recitation_bot

# Technology Spec
* Database: Mongo
* Algorithm: Convolutional Neural Network
* Containerization: Docker CE
* Orchestration: Docker Swarm

# Secrets
Don't forget to set secrets
* ../secrets/telegramtoken
* ../secrets/mongouser
* ../secrets/mongopass
* ../secrets/mongohost

# Requirements
* pip install -r requirements (delete tensorflow part if you use tensorflow-gpu)
* apt-get install python-tk 
* Install ffmpeg

# Useful CMDs
* Run tensorboard: tensorboard --logdir=/tmp/logs/ --port=80 --host=0.0.0.0
* or on mac: python /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/tensorboard/main.py --logdir=/tmp/logs/ --port=8080 --host=0.0.0.0
* Run mp3 convertion: ffmpeg -i file.mp3 -acodec pcm_u8 -filter:a loudnorm -ar 22050 -y file.wav
* Run ogg convertion: ffmpeg -i file.ogg -filter:a loudnorm -ar 22050 -y file.wav

# Git related
### Stashing only 1 file (i use this for generated model)
* $ git add .
* $ git reset <target file>
* $ git stash save --keep-index

# DB Design
It's json structured contains 2 schema

### user
* telegram_id
* username
* current_verse
* current_ayah
* stage_level
* score

### stage_available
* stage_number
* verse_number
* total_ayah

# Todo
* Ganti max_pad_len
