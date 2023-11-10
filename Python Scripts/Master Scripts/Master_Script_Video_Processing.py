import os
import subprocess

# Define the directories
scripts_directory = r"C:\Users\dave_\FurrVision\Python Scripts\Video Processing"
video_repository_path = r"C:\Users\dave_\FurrVision\Video Repository"
accredited_videos_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Accredited videos"
commentary_dir = r"C:\Users\dave_\FurrVision\Compiled Videos\Commentary"
speech_files_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Speech"
accredited_commentary_videos_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Accredited + Commentary videos"
accredited_commentary_cta_videos_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Accredited + Commentary + CTA videos"
compiled_videos_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Compilations"
comments_dir = r"C:\Users\dave_\FurrVision\Compiled Videos\Comments"

# List of your scripts
scripts = [
    ["python", os.path.join(scripts_directory, "scrape_subreddit_videos.py"), "AnimalsBeingBros", "5000", "top"],
    ["python", os.path.join(scripts_directory, "add_credit_author.py")],
    ["python", os.path.join(scripts_directory, "generate_commentary.py")],
    ["python", os.path.join(scripts_directory, "generate_speech.py")],
    ["python", os.path.join(scripts_directory, "add_speech.py")],
    ["python", os.path.join(scripts_directory, "add_CTA.py")],
    ["python", os.path.join(scripts_directory, "compile_accredited_videos.py")]
]

# Run each script
for script in scripts:
    try:
        print(f"Running {script[1]}...")
        subprocess.run(script, check=True)
        print(f"Successfully ran {script[1]}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script[1]}. Stopping the rest of the scripts.")
        print(f"Error details: {e}")
        break
