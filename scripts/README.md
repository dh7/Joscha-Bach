# These scripts download the data from publicly available sources.

Before running these scripts, you need to prepare your environment.

```
echo "your-yt-api-key" > secret-api-key-youtube.txt
pip install --upgrade google-api-python-client
pip install pytube
```

list-videos.py download the video URLs from Joscha Channel, and save them into ../sources/youtube.csv
