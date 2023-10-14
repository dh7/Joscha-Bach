import os
import googleapiclient.discovery

def load_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        exit(1)

def get_channel_id(api_key, username=None, for_username=None):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    try:
        if username:
            search_response = youtube.search().list(
                part="snippet",
                maxResults=5,
                q=username,
                type="channel"
            ).execute()
        elif for_username:
            search_response = youtube.channels().list(
                part="snippet",
                forUsername=for_username
            ).execute()
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
    
    video_response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()
    
    if "items" in video_response and video_response["items"]:
        return video_response["items"][0]["snippet"]["channelId"]
    else:
        print("Video not found.")
        return None


def get_all_videos(api_key, channel_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    uploads_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    all_video_ids = []
    next_page_token = None
    while True:
        playlist_response = youtube.playlistItems().list(
            part="contentDetails",
            maxResults=50,
            playlistId=uploads_id,
            pageToken=next_page_token
        ).execute()
        all_video_ids.extend([item['contentDetails']['videoId'] for item in playlist_response['items']])
        next_page_token = playlist_response.get('nextPageToken')
        if next_page_token is None:
            break
    
    video_details = []
    for video_id in all_video_ids:
        video_response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()
        video_title = video_response['items'][0]['snippet']['title']
        video_details.append({'title': video_title, 'id': video_id})
    
    return video_details

if __name__ == "__main__":
    API_KEY = load_api_key("secret-api-key-youtube.txt")
    print (API_KEY)
    # CHANNEL_ID = get_channel_id(API_KEY, for_username="JoschaBach") 
    CHANNEL_ID = get_channel_id_from_video(API_KEY, "lKQ0yaEJjok")
    print (CHANNEL_ID)
    
    videos = get_all_videos(API_KEY, CHANNEL_ID)
    
    for idx, video in enumerate(videos, 1):
        print(f"{idx}. {video['title']} (https://www.youtube.com/watch?v={video['id']})")

