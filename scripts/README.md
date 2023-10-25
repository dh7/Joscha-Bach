# These scripts download the data from publicly available sources.

Before running these scripts, you need to prepare your environment.

```
echo "your-yt-api-key.txt" > secret-api-key-youtube.txt
echo "your-hf-token.txt > secret-hf-token.txt
pip install --upgrade google-api-python-client
pip install pytube # for downloading the video and audio
pip install gradio_client # for wisper transcription
pip install pyannote.audio # for segmentation
```

list-videos.py download the video URLs from Joscha Channel, and save them into ../sources/youtube.csv
download_audio.py to download the audiofiles
download_video.py to download the video from YT
compress_audio.py to save some space on disk
transcribe.py to extract text from videos
