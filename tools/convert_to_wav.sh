#!/bin/bash
for filename in dataset/audio/*/*.mp3; do
	echo "ffmpeg -i $filename -acodec pcm_u8 -ar 22050 $filename.wav"
	ffmpeg -i $filename -acodec pcm_u8 -ar 22050 $filename.wav &>/dev/null
done