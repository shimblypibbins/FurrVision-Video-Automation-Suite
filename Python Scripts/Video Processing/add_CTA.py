import os
from moviepy.editor import *
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

font_path = r"C:\Users\dave_\FurrVision\Fonts\AmaticSC-Bold.ttf"
video_folder = "C:/Users/dave_/FurrVision/Compiled Videos/Accredited + Commentary videos/"
output_folder = r"C:\Users\dave_\FurrVision\Compiled Videos\Accredited + Commentary + CTA videos"
text_content = "Discover more on our YouTube channel! \n youtube.com/@FurrVisionOfficial"

def add_text_overlay(input_video, output_video, text_content):
    clip = VideoFileClip(input_video)

    text = TextClip(
        text_content,
        fontsize=22,
        color="#FF8E3E",
        font=font_path,
    )

    background = ColorClip(size=(text.w, text.h), color=(245, 233, 212), duration=5).set_opacity(0.5)

    text_on_background = CompositeVideoClip([background, text.set_position("center")], size=(text.w, text.h))
    text_on_background = text_on_background.set_position(('center', 'bottom'), relative=True).set_duration(5)

    text_on_background = text_on_background.set_start(clip.duration - 5)

    final = CompositeVideoClip([clip, text_on_background])
    final.write_videofile(output_video, codec="libx264", audio_codec="aac")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for video_file in os.listdir(video_folder):
    if video_file.endswith(".mp4"):
        input_video = os.path.join(video_folder, video_file)
        output_video_name = os.path.splitext(video_file)[0] + "_CTA" + os.path.splitext(video_file)[1]
        output_video = os.path.join(output_folder, output_video_name)

        # Check if the output video with _CTA suffix already exists in the output folder
        if not os.path.exists(output_video):
            add_text_overlay(input_video, output_video, text_content)
