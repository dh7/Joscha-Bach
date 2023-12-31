import json
import replicate


def remove_words_from_json(json_data):
    """
    Remove the 'words' key from each segment in the provided JSON data.

    :param json_data: The JSON data as a dictionary.
    :return: The modified JSON data without the 'words' keys.
    """
    if "segments" in json_data:
        for segment in json_data["segments"]:
            if "words" in segment:
                del segment["words"]
    return json_data


def concatenate_consecutive_speakers(json_data):
    """
    Concatenate segments when the same speaker appears consecutively.

    :param json_data: The JSON data as a dictionary.
    :return: Updated JSON data with concatenated segments for consecutive same speakers.
    """
    if "segments" not in json_data:
        return json_data

    new_segments = []
    current_segment = None

    for segment in json_data["segments"]:
        if current_segment is None:
            current_segment = segment
        elif current_segment["speaker"] == segment["speaker"]:
            # Extend the current segment
            current_segment["end"] = segment["end"]
            current_segment["text"] += " " + segment["text"]
        else:
            new_segments.append(current_segment)
            current_segment = segment

    # Add the last segment if it exists
    if current_segment is not None:
        new_segments.append(current_segment)

    return {"segments": new_segments}


def json_to_formatted_string(json_data):
    """
    Converts a JSON structure with 'segments' containing 'speaker' and 'text'
    into a formatted string where each line starts with the speaker's name followed by the text.
    """
    formatted_text = []
    for segment in json_data.get("segments", []):
        speaker = segment.get("speaker", "Unknown")
        text = segment.get("text", "")
        formatted_text.append(f"{speaker}: {text}")

    # create a multi-line string containing the formatted text
    multi_line_string = """
""".join(
        formatted_text
    )
    return multi_line_string


output = replicate.run(
    "thomasmol/whisper-diarization:4fe3d4a4c584781e7e4a4c27855cd82aac3bf1daa7b8dda5c4844201e051768c",
    input={
        "file": "https://replicate.delivery/pbxt/JcL0ttZLlbchC0tL9ZtB20phzeXCSuMm0EJNdLYElgILoZci/AI%20should%20be%20open-sourced.mp3",
        "prompt": "Mark and Lex talking about AI.",
        "file_url": "",
        "num_speakers": 2,
        "group_segments": True,
        "offset_seconds": 0,
    },
)


with open("output.json", "w") as f:
    json.dump(output, f)

result = remove_words_from_json(output)
result_clean = concatenate_consecutive_speakers(result)
result_text = json_to_formatted_string(result_clean)

with open("result_text.txt", "w") as f:
    f.write(result_text)
