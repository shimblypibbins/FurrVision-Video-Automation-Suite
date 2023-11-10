import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason, CancellationReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig

try:
    # Get the command line arguments
    commentary_dir = r"C:\Users\dave_\FurrVision\Compiled Videos\Commentary"
    speech_files_path = r"C:\Users\dave_\FurrVision\Compiled Videos\Speech"

    # Create the directory for saving the speech files if it doesn't exist
    os.makedirs(speech_files_path, exist_ok=True)

    # Set up the speech config with your Azure Text to Speech key and region
    speech_config = SpeechConfig(subscription="abe97cd5318a41149c514640ebf09f83", region="uksouth")

    # Get the list of commentary files
    commentary_files = [f for f in os.listdir(commentary_dir) if f.endswith(".txt")]

    # Generate an audio file for each commentary file
    for commentary_file in commentary_files:
        # Define the path to save the audio file
        audio_output_path = os.path.join(speech_files_path, commentary_file.replace("_commentary.txt", ".mp3"))

        # Check if the speech file already exists, and if so, print a message and skip to the next file
        if os.path.exists(audio_output_path):
            print(f"Speech file for {commentary_file} already exists. Skipping...")
            continue

        # Read the commentary from the file
        with open(os.path.join(commentary_dir, commentary_file), "r", encoding="utf-8") as f:
            commentary = f.read().strip()

        # Set up the SSML string
        ssml_string = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='en-US'>
            <voice name='en-US-JennyNeural'>
                <mstts:express-as style='friendly'>
                    <prosody rate="15%">
                        {commentary}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """

        # Define the audio output config
        audio_output = AudioOutputConfig(filename=audio_output_path)

        # Create a speech synthesizer with specific audio output
        speech_synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

        # Synthesize the text to speech
        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        # Check the result
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized to [{audio_output_path}] successfully.")
        elif result.reason == ResultReason.Canceled:
            cancellation = result.cancellation_details
            if cancellation.reason == CancellationReason.Error:
                print("Error details: {}".format(cancellation.error_details))
            else:
                print(f"Speech synthesis was canceled: {cancellation.reason}.")
        else:
            print(f"Speech synthesis did not complete successfully: {result.reason}.")
except Exception as e:
    print(f"An error occurred: {e}")
