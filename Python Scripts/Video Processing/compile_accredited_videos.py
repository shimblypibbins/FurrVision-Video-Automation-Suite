import os
import gc
import subprocess
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips
from moviepy.video.fx.all import resize, margin
import numpy as np


def read_video_info(video_info_path):
    video_info = {}
    with open(video_info_path, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            post_id = lines[i].strip().split()[-1]
            username = lines[i + 1].strip().split()[-1]
            post_url = lines[i + 2].strip().split()[-1]
            video_info[post_id] = (username, post_url)  # Remove the _credit.mp4 suffix
    return video_info

def read_compiled_video_counter(counter_file):
    if not os.path.exists(counter_file):
        return 1
    with open(counter_file, "r") as f:
        return int(f.read().strip())

def write_compiled_video_counter(counter_file, counter_value):
    with open(counter_file, "w") as f:
        f.write(str(counter_value))

def read_processed_videos():
    if not os.path.exists(processed_videos_file):
        return set()
    with open(processed_videos_file, "r") as f:
        return set(line.strip() for line in f.readlines())

def write_processed_videos(processed_videos_set):
    with open(processed_videos_file, "w") as f:
        for video_name in processed_videos_set:
            f.write(video_name + "\n")

def concatenate_videos(clip_list, output_path):
    resized_clips = []
    target_height = 1080

    for clip in clip_list:
        resized_clip = resize(clip, height=target_height)
        left_margin = max((1920 - resized_clip.w + (1920 - resized_clip.w) % 2) // 2, 0)
        right_margin = max(1920 - resized_clip.w - left_margin, 0)

        
        def pad_frame(get_frame, t):
            frame = get_frame(t)
            padded_frame = np.pad(frame, ((0, 0), (left_margin, right_margin), (0, 0)), mode='constant', constant_values=0)
            return padded_frame
        
        resized_clip = resized_clip.fl(lambda gf, t: pad_frame(gf, t))
        resized_clips.append(resized_clip)

    final_clip = concatenate_videoclips(resized_clips, method="compose")
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

accredited_with_commentary_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Accredited + Commentary videos"
compiled_videos_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Compilations"
intro_video_path = r"C:\Users\dave_\FurrVision\Logos\furrvision_intro_video.mp4"
processed_videos_file = r"C:\Users\dave_\FurrVision\Compiled Videos\processed_videos.txt"
video_info_path = r"C:\Users\dave_\FurrVision\Video Repository\video_info.txt"
video_descriptions_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Compilations\Compilation Video Descriptions"
counter_file = r"C:\Users\dave_\FurrVision\Compiled Videos\compiled_video_counter.txt"

video_info_map = read_video_info(video_info_path)
processed_videos = read_processed_videos()
video_files = [f for f in os.listdir(accredited_with_commentary_path) if f.endswith(".mp4") and f not in processed_videos]

intro_clip = VideoFileClip(intro_video_path)

current_duration = 0
min_duration = 5 * 60  # 5 minutes in seconds
clips_to_concatenate = [intro_clip]

for video_file in video_files:
    video_path = os.path.join(accredited_with_commentary_path, video_file)
    video_clip = VideoFileClip(video_path)
    current_duration += video_clip.duration

    clips_to_concatenate.append(video_clip)

    if current_duration >= min_duration:
        compiled_video_counter = read_compiled_video_counter(counter_file)
        final_video_filename = f"compiled_video_{compiled_video_counter}.mp4"
        final_video_path = os.path.join(compiled_videos_path, final_video_filename)
        write_compiled_video_counter(counter_file, compiled_video_counter + 1)

        concatenate_videos(clips_to_concatenate, final_video_path)

        # Write video descriptions
        with open(os.path.join(video_descriptions_path, final_video_filename.replace(".mp4", ".txt")), "w") as f:
            for clip in clips_to_concatenate[1:]:
                username, post_url = video_info_map[os.path.basename(clip.filename).replace("_credit_speech.mp4", "")]
                f.write(f"{username}\n")
                f.write(f"{post_url}\n\n")

        # Mark the videos as processed
        for clip in clips_to_concatenate[1:]:
            processed_videos.add(os.path.basename(clip.filename))
        write_processed_videos(processed_videos)

        current_duration = 0
        clips_to_concatenate = [intro_clip]