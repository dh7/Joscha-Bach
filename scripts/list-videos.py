# This script lists all videos from JoschaBach YouTube channel.
# And write the result to a file in ../source/youtube.csv

import csv
import googleapiclient.discovery


def load_api_key(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        exit(1)


def get_channel_id(api_key, username=None, for_username=None):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    try:
        if username:
            search_response = (
                youtube.search()
                .list(part="snippet", maxResults=5, q=username, type="channel")
                .execute()
            )
        elif for_username:
            search_response = (
                youtube.channels()
                .list(part="snippet", forUsername=for_username)
                .execute()
            )
        else:
            print("You must provide either username or for_username parameter.")
            return None

        if "items" in search_response and search_response["items"]:
            return search_response["items"][0]["id"]["channelId"]
        else:
            print("Channel not found or API Error.")
            return None
    except googleapiclient.errors.HttpError as e:
        print(f"HTTP Error: {e}")
        return None
    except KeyError as e:
        print(f"Expected key not found in response: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_channel_id_from_video(api_key, video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    video_response = youtube.videos().list(part="snippet", id=video_id).execute()

    if "items" in video_response and video_response["items"]:
        return video_response["items"][0]["snippet"]["channelId"]
    else:
        print("Video not found.")
        return None


def get_playlists(api_key, channel_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    all_playlists = []
    next_page_token = None
    while True:
        playlists_response = (
            youtube.playlists()
            .list(
                part="snippet",
                channelId=channel_id,
                maxResults=50,  # Maximum allowed by API
                pageToken=next_page_token,
            )
            .execute()
        )

        for item in playlists_response.get("items", []):
            title = item["snippet"]["title"]
            playlist_id = item["id"]
            # playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
            all_playlists.append((title, playlist_id))

        next_page_token = playlists_response.get("nextPageToken")
        if next_page_token is None:
            break

    return all_playlists


def get_all_videos(api_key, channel_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    channel_response = (
        youtube.channels().list(part="contentDetails", id=channel_id).execute()
    )
    uploads_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"][
        "uploads"
    ]

    all_video_ids = []
    next_page_token = None
    while True:
        playlist_response = (
            youtube.playlistItems()
            .list(
                part="contentDetails",
                maxResults=50,
                playlistId=uploads_id,
                pageToken=next_page_token,
            )
            .execute()
        )
        all_video_ids.extend(
            [item["contentDetails"]["videoId"] for item in playlist_response["items"]]
        )
        next_page_token = playlist_response.get("nextPageToken")
        if next_page_token is None:
            break

    video_details = []
    for video_id in all_video_ids:
        video_response = youtube.videos().list(part="snippet", id=video_id).execute()
        video_title = video_response["items"][0]["snippet"]["title"]
        video_details.append({"title": video_title, "id": video_id})

    return video_details


def get_videos_from_playlist(api_key, playlist_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    all_videos = []
    next_page_token = None
    while True:
        playlistitems_response = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,  # Maximum allowed by API
                pageToken=next_page_token,
            )
            .execute()
        )

        for item in playlistitems_response.get("items", []):
            title = item["snippet"]["title"]

            video_id = item["snippet"]["resourceId"]["videoId"]

            video_url = f"https://www.youtube.com/watch?v={video_id}"
            all_videos.append((title, video_url))

        next_page_token = playlistitems_response.get("nextPageToken")
        if next_page_token is None:
            break
    return all_videos


if __name__ == "__main__":
    OUTPUT_FILE = "../sources/youtube.csv"

    API_KEY = load_api_key("secret-api-key-youtube.txt")
    CHANNEL_ID = get_channel_id_from_video(
        API_KEY, "lKQ0yaEJjok"
    )  # Joscha Bach's channel from a knowed video ID

    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Video URL"])  # Header
        playlists = get_playlists(API_KEY, CHANNEL_ID)
        for title, id in playlists:
            print("Playlist ID", id)
            video_lists = get_videos_from_playlist(API_KEY, id)
            for video in video_lists:
                csv_writer.writerow([video[1]])
                print(f"{video[1]}")
