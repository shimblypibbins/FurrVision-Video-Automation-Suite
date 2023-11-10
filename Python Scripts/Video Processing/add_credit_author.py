import os
import sys
import json
import moviepy.config as mp_config
from moviepy.editor import VideoFileClip, TextClip, ImageClip, CompositeVideoClip

mp_config.change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

# Get the input and output directories from the command line arguments
video_repository_path = r"C:\Users\dave_\FurrVision\Video Repository"
accredited_videos_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Accredited videos"

video_info_file_path = os.path.join(video_repository_path, "video_info.txt")
reddit_icon_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Icons\reddit_icon.png"

with open(video_info_file_path, "r") as f:
    lines = f.readlines()

video_info = []
for i in range(0, len(lines), 4):
    video_id = lines[i].split(" ")[-1].strip()
    author_username = lines[i + 1].split(" ")[-1].strip()
    post_url = lines[i + 2].split(" ")[-1].strip()
    video_info.append({"video_id": video_id, "author_username": author_username, "post_url": post_url})

for info in video_info:
    video_id = info["video_id"]
    input_video_path = os.path.join(video_repository_path, f"{video_id}.mp4")
    output_video_path = os.path.join(accredited_videos_path, f"{video_id}_credit.mp4")

    # Check if the output video already exists
    if os.path.exists(output_video_path):
        print(f"Video {video_id} has already been processed. Skipping...")
        continue

    author_username = info["author_username"]

    video = VideoFileClip(input_video_path)

    # Position the credits relative to the frame of the video (including the black bars)
    credit_x = video.margin().w * 0.05  # 5% from the left of the frame
    credit_y = video.margin().h * 0.05  # 5% from the top of the frame

    text_clip = (TextClip(f"u/{author_username}", fontsize=20, color="white", bg_color="#FF4301", font="Verdana")
                 .set_duration(video.duration)
                 .set_position((credit_x, credit_y)))

    reddit_icon = (ImageClip(reddit_icon_path)
                   .set_duration(video.duration)
                   .resize(height=25)
                   .set_position((credit_x, credit_y)))

    # Use the margin() method to ensure that the credits are positioned relative to the frame of the video
    final_video = CompositeVideoClip([video.margin(), reddit_icon, text_clip])
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
