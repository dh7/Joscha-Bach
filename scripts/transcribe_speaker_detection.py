# This script reads a CSV file with YouTube URLs and transcribes the audio
# it uses the HF API to transcribe the audio
# https://huggingface.co/spaces/sanchit-gandhi/whisper-jax

import csv
import time
from gradio_client import Client
import re

def test():
    import requests

    response = requests.post("https://dh7net-faster-whisper-webui.hf.space/run/predict", json={
        "data": [
            "tiny",
            "Afrikaans",
            "hello world",
            {"name":"zip.zip","data":"data:@file/octet-stream;base64,UEsFBgAAAAAAAAAAAAAAAAAAAAAAAA=="},
            {"name":"audio.wav","data":"data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="},
            "transcribe",
            "none",
            5,
            30,
            False,
            False,
            False,
            2,
        ]
    }).json()

    data = response["data"]

def load_HF_token(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        exit(1)

def transcribe(audio_file, output_transcription_file):
    client = Client("https://dh7net-faster-whisper-webui.hf.space/",
                    hf_token=load_HF_token("secret-hf-token.txt"))
    print(f"Transcribing File:{audio_file}")
    file = open(audio_file, "rb")
    job = client.submit(
        "medium", # represents selected choice of 'Model' Dropdown component
        "English", # represents selected choice of 'Language' Dropdown component
        "", # represents text string of 'URL (YouTube, etc.)' Textbox component
        audio_file, # represents object with file name and base64 data of 'Upload Files' File component
        None, # represents audio data as object with filename and base64 string of 'Microphone Input' Audio component
        "transcribe", # represents selected choice of 'Task' Dropdown component
        "silero-vad", # represents selected choice of 'VAD' Dropdown component
        5, # represents numeric value of 'VAD - Merge Window (s)' Number component
        30, # represents numeric value of 'VAD - Max Merge Size (s)' Number component
        False, # represents checked status of 'Word Timestamps' Checkbox component
        False, # represents checked status of 'Word Timestamps - Highlight Words' Checkbox component
        True, # represents checked status of 'Diarization' Checkbox component
        2, # represents numeric value of 'Diarization - Speakers' Number component
        api_name="/predict",
    )
    while not job.done():
        print('Waiting for job to complete...')
        time.sleep(0.1)
    result = job.outputs()
    # save output to a text file
    with open(output_transcription_file, "w") as file:
        file.write(str(result))

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
    transcribe("audio.wav", "output.txt")
    # csv_filename = "../sources/youtube.csv"
    # read_csv_and_transcribe(csv_filename, path="../data/transcriptions/")
