import os
import requests
from requests_oauthlib import OAuth1

# Define your Twitter API credentials
API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

# Define the Twitter API endpoints
MEDIA_UPLOAD_URL = 'https://upload.twitter.com/1.1/media/upload.json'
TWEET_CREATE_URL = 'https://api.twitter.com/2/tweets'  # Updated to v2 endpoint

# Create an OAuth1 session
auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Define the path to your videos
video_path = r'C:\Users\dave_\FurrVision\Compiled Videos\Accredited + Commentary + CTA videos'

# Define the path to the posted videos file
posted_videos_file = r'C:\Users\dave_\FurrVision\Compiled Videos\posted_videos_twitter.txt'

# Define the path to your commentary files
commentary_path = r'C:\Users\dave_\FurrVision\Compiled Videos\Commentary'

# Create the posted videos file if it doesn't exist
if not os.path.exists(posted_videos_file):
    with open(posted_videos_file, 'w') as f:
        pass

# Get list of posted videos
with open(posted_videos_file, 'r') as f:
    posted_videos = f.read().splitlines()

# Get list of all videos
all_videos = os.listdir(video_path)

# Find a video that hasn't been posted yet
for video in all_videos:
    if video not in posted_videos and not video.endswith('.txt'):
        # Get the corresponding commentary file
        video_name, video_ext = os.path.splitext(video)
        video_name = video_name.replace('_credit_speech_CTA', '')  # Remove "_credit_speech_CTA_" from video name
        commentary_file = os.path.join(commentary_path, video_name + '_commentary.txt')

        # Read the first sentence of the commentary
        with open(commentary_file, 'r') as f:
            status = f.read().strip()

        upload_successful = False

        try:
            # Post the video using v1.1 media upload endpoint
            video_file = os.path.join(video_path, video)
            files = {'media': open(video_file, 'rb')}
            response = requests.post(MEDIA_UPLOAD_URL, auth=auth, files=files)
            response.raise_for_status()
            media_id = response.json()['media_id_string']  # Get the media ID
            upload_successful = True
        except Exception as e:
            print(f"Error: {type(e).__name__}, {e}")

        if upload_successful:
            try:
                # Create a tweet using v2 Tweet create endpoint and the media ID
                data = {
                    "text": status,
                    "attachments": {
                        "media_keys": [media_id]  # Updated to use "media_keys" instead of "media_ids"
                    }
                }
                response = requests.post(TWEET_CREATE_URL, auth=auth, json=data)
                response.raise_for_status()
                print(f"Tweet created: {response.json()['data']['id']}")
            except Exception as e:
                print(f"Error: {type(e).__name__}, {e}")

            # Add the video to the list of posted videos
            with open(posted_videos_file, 'a') as f:
                f.write(video + '\n')

            # Stop the loop after posting one video
            break
