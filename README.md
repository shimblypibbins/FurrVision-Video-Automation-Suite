# FurrVision: Video Automation Suite

## Description
FurrVision is an automated video processing suite designed to streamline the creation and compilation of social media videos. It utilizes a series of Python scripts to automate various tasks, such as downloading videos, accrediting authors, generating commentary, synthesizing speech, adding CTAs, and compiling the final video outputs for platforms like YouTube.

## Features
- **Video Downloading**: Automatically downloads videos from specified subreddits or sources.
- **Accreditation**: Adds author credits to downloaded videos.
- **Commentary Generation**: Generates commentary based on the video content.
- **Speech Synthesis**: Converts generated commentary text to speech.
- **CTA Inclusion**: Adds calls to action in videos to increase viewer engagement.
- **Video Compilation**: Compiles the processed videos for upload to social media channels.

## Prerequisites
Before running the scripts, ensure you have Python installed on your system. You also need to install the necessary dependencies which can be found in the `requirements.txt` file.

## Installation
Clone the repository to your local machine using the following command:
## Installation

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/shimblypibbins/FurrVision-Video-Automation-Suite
cd FurrVision-Video-Automation-Suite
pip install -r requirements.txt
```


## Usage

To run the full suite of scripts:

```python
python master_script.py
```
You can also run each script individually as needed:
```
python download_videos.py [arguments]
python add_credit_author.py
python generate_commentary.py
python generate_speech.py
python add_speech.py
python add_CTA.py
python compile_accredited_videos.py
```

## Configuration
Edit the master_script.py to set the paths and parameters for your video processing workflow.

## Contributing
Contributions to FurrVision are welcome. Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the LICENSE - see the LICENSE.md file for details.

## Contact
For support or collaboration, please contact [david.c.p.laing@gmail.com] or open an issue in the repository.

Note
Make sure you replace [your-repo-link], [repository-name], [LICENSE], and [your-email] with your actual repository link, the name of the repository, the type of license you're using, and your contact email, respectively.
