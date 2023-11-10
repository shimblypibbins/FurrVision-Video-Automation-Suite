import praw
import requests
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import sys

# Replace with your Reddit API credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
user_agent = "YOUR_USER_AGENT"

# Create a Reddit instance with your authentication information
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Subreddit and number of posts to scrape
subreddit_name = sys.argv[1]  # Get the subreddit name from the command line arguments
post_limit = int(sys.argv[2])  # Get the post limit from the command line arguments
post_sort = sys.argv[3]  # Get the post sort from the command line arguments

# Get the video posts from the subreddit of your choice
subreddit = reddit.subreddit(subreddit_name)
if post_sort == 'top':
    posts = subreddit.top(limit=post_limit, time_filter='all')
elif post_sort == 'hot':
    posts = subreddit.hot(limit=post_limit)
elif post_sort == 'rising':
    posts = subreddit.rising(limit=post_limit)
else:
    print(f"Invalid post sort: {post_sort}. Please use 'top','hot' or 'rising'.")
    sys.exit(1)

# Set output directories
output_dir = r"C:\Users\dave_\FurrVision\Video Repository"
comments_dir = r"C:\Users\dave_\FurrVision\Compiled Videos\Comments"


def add_letterboxing(clip, target_aspect_ratio=16 / 9):
    width, height = clip.size
    aspect_ratio = width / height

    if aspect_ratio == target_aspect_ratio:
        return clip

    if aspect_ratio > target_aspect_ratio:
        new_height = int(width / target_aspect_ratio)
        padding = (new_height - height) // 2
        return clip.margin(top=padding, bottom=padding, color=(0, 0, 0))

    new_width = int(height * target_aspect_ratio)
    padding = (new_width - width) // 2
    return clip.margin(left=padding, right=padding, color=(0, 0, 0))

# Open the video info file
with open(f"{output_dir}/video_info.txt", "a") as info_file:
    # Loop through the posts and scrape the videos
    for post in posts:
        # Check if the post is a video
        if post.is_video:
            # Check if the video has already been downloaded
            if os.path.exists(f"{output_dir}/{post.id}.mp4"):
                print(f"Video {post.id} already exists. Skipping...")
                continue

            # Get the video and audio URLs
            video_url = post.media["reddit_video"]["fallback_url"]
            audio_url = video_url.split("DASH_")[0] + "DASH_audio.mp4"

            try:
                # Download the video
                video_response = requests.get(video_url)
                video_response.raise_for_status()

                # Download the audio
                audio_response = requests.get(audio_url)
                audio_response.raise_for_status()

                # Save video and audio temporarily
                with open(f"{output_dir}/{post.id}_video.mp4", "wb") as f:
                    f.write(video_response.content)

                with open(f"{output_dir}/{post.id}_audio.mp4", "wb") as f:
                    f.write(audio_response.content)

                # Merge video and audio
                video_clip = VideoFileClip(f"{output_dir}/{post.id}_video.mp4")
                audio_clip = AudioFileClip(f"{output_dir}/{post.id}_audio.mp4")
                final_clip = video_clip.set_audio(audio_clip)

                # Add letterboxing
                letterboxed_clip = add_letterboxing(final_clip)

                # Save the merged video
                letterboxed_clip.write_videofile(f"{output_dir}/{post.id}.mp4")

                # NEW: save the top comments
                with open(f"{comments_dir}/{post.id}_comments.txt", "w", encoding="utf-8") as comments_file:
                    comments_file.write(f"Title: {post.title}\n")  # Write the post title at the top of the file
                    post.comments.replace_more(limit=0)  # get top comments
                    for comment in post.comments.list()[:3]:  # adjust number for how many comments you want
                        comments_file.write(comment.body + "\n")


                # Save the post information in the video info file
                info_file.write(f"Post ID: {post.id}\n")
                info_file.write(f"Username: {post.author}\n")
                info_file.write(f"Post URL: https://www.reddit.com{post.permalink}\n")
                info_file.write("\n")
                info_file.flush()  # Add this line to flush the file buffer

                # Remove temporary video and audio files
                os.remove(f"{output_dir}/{post.id}_video.mp4")
                os.remove(f"{output_dir}/{post.id}_audio.mp4")

            except Exception as e:
                print(f"Error occurred while downloading video {post.id}. Video source URL: {video_url}")
                print(f"Error message: {e}")

            else:
                print(f"Downloaded video {post.id}. Video source URL: {video_url}")

print("Video scraping completed.")

