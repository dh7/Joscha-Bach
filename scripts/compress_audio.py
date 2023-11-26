import subprocess
import os


def convert_webm_to_mp3(input_path, output_path, bitrate="64k"):
    cmd = ["ffmpeg", "-i", input_path, "-b:a", bitrate, output_path]

    subprocess.run(cmd, check=True)


def convert_all_in_folder(folder, bitrate="64k"):
    for filename in os.listdir(folder):
        if filename.endswith(".mp4"):
            print(f"Converting {filename}")
            webm_path = os.path.join(folder, filename)
            mp3_path = os.path.join(folder, filename.replace(".mp4", ".mp3"))
            convert_webm_to_mp3(webm_path, mp3_path, bitrate=bitrate)


if __name__ == "__main__":
    folder_path = "../data/audio/"
    convert_all_in_folder(folder_path, bitrate="32k")
