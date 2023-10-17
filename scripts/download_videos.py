# This script downloads videos from YouTube using pytube
# It reads a CSV file with the URLs of the videos to download

import csv
from pytube import YouTube


def download_video(url, path):
    yt = YouTube(url)
    video_stream = yt.streams.get_highest_resolution()
    video_stream.download(output_path=path)


def read_csv_and_download(filename, path="~/Downloads"):
    with open(filename, "r", newline="", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header
        for row in csvreader:
            try:
                print(f"Downloading {row[0]}")
                download_video(
                    row[0], path
                )  # Assuming URL is in the first column of the CSV
            except Exception as e:
                print(f"Error downloading {row[0]}: {e}")


if __name__ == "__main__":
    csv_filename = "../sources/youtube.csv"
    read_csv_and_download(csv_filename, path="../data/videos/")
