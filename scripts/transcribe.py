# This script reads a CSV file with YouTube URLs and transcribes the audio
# it uses the HF API to transcribe the audio
# https://huggingface.co/spaces/sanchit-gandhi/whisper-jax

import csv
from gradio_client import Client
import re

client = Client("https://sanchit-gandhi-whisper-jax.hf.space/")

def extract_video_id_from_url(url):
    # Regular expression to match a YouTube URL
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    
    match = re.match(youtube_regex, url)
    if not match:
        return None

    return match.group(6)


def read_csv_and_transcribe(filename, path="~/Downloads"):
    with open(filename, "r", newline="", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header
        for row in csvreader:
            try:
                # Assuming URL is in the first column of the CSV
                id = extract_video_id_from_url(row[0])
                print(f"Transcribing ID:{id}")
                result = client.predict(
                    row[0],  # str in 'YouTube URL' Textbox component
                    "transcribe",  # str in 'Task' Radio component
                    False,  # bool in 'Return timestamps' Checkbox component
                    api_name="/predict_2",
                )
                # save output to a text file
                with open(f"{path}{id}.txt", "w") as file:
                    file.write(str(result))

            except Exception as e:
                print(f"Error Transcribing {row[0]}: {type(e).__name__}, {e}")

if __name__ == "__main__":
    csv_filename = "../sources/youtube.csv"
    read_csv_and_transcribe(csv_filename, path="../data/transcriptions/")
