import os
import sys
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_audioclips

# Get the command line arguments
accredited_videos_dir = r"C:\Users\dave_\FurrVision\Compiled Videos\Accredited videos"
speech_dir = r"C:\Users\dave_\FurrVision\Compiled Videos\Speech"
output_dir = r"C:\Users\dave_\FurrVision\Compiled Videos\Accredited + Commentary videos"

# Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get the list of video files
video_files = [f for f in os.listdir(accredited_videos_dir) if f.endswith(".mp4")]

# For each video file
for video_file in video_files:
    # Get the base file name without "_credit.mp4"
    base_name = video_file.replace("_credit.mp4", "")

    # Check if the output video file already exists
    final_output_name = base_name + "_credit_speech.mp4"
    if os.path.exists(os.path.join(output_dir, final_output_name)):
        print(f"Output file for video {video_file} already exists. Skipping...")
        continue

    # Get the corresponding speech file
    speech_file = base_name + ".mp3"

    # Check if the speech file exists
    if not os.path.exists(os.path.join(speech_dir, speech_file)):
        print(f"Could not find speech file for video {video_file}. Skipping...")
        continue

    try:
        # Load the video and the speech
        video = VideoFileClip(os.path.join(accredited_videos_dir, video_file))
        speech = AudioFileClip(os.path.join(speech_dir, speech_file))

        # Set the volume for the original video audio during and after the speech
        during_speech = video.audio.subclip(0, speech.duration).volumex(0.3)  # 30% volume
        after_speech = video.audio.subclip(speech.duration).volumex(1.0)  # 100% volume

        # Concatenate the video audio back together
        video_audio = concatenate_audioclips([during_speech, after_speech])

        # Make the speech the same duration as the video
        if speech.duration > video.duration:
            speech = speech.subclip(0, video.duration)

        # Combine the video audio and the speech
        final_audio = CompositeAudioClip([video_audio, speech])

        # Set the audio of the video to be the final audio
        final_video = video.set_audio(final_audio)

        # Write the final video to a file
        final_video.write_videofile(os.path.join(output_dir, final_output_name))

    except Exception as e:
        print(f"An error occurred while processing video {video_file}: {e}")

print("Processing completed.")
