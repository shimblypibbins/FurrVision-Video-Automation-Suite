import os
import openai
import nltk  
import sys


# Set your OpenAI key
openai.api_key = 'YOUR_API_KEY'

# Define the directory containing the comments files
comments_dir = r"C:\Users\dave_\FurrVision\Compiled Videos\Comments"

# Define the directory to store the commentary files
commentary_dir = r"C:\Users\dave_\FurrVision\Compiled Videos\Commentary"

# Ensure the commentary directory exists
os.makedirs(commentary_dir, exist_ok=True)

# Get the list of comments files
comments_files = [f for f in os.listdir(comments_dir) if f.endswith(".txt")]

# Process each comments file
for comments_file in comments_files:
    # Define the name of the commentary file
    commentary_file = comments_file.replace("_comments.txt", "_commentary.txt")

    # Check if the commentary file already exists, and if so, skip to the next file
    if os.path.exists(os.path.join(commentary_dir, commentary_file)):
        continue

    # Read the title and comments
    with open(os.path.join(comments_dir, comments_file), "r", encoding="utf-8") as f:
        title_and_comments = f.read()
    title, comments = title_and_comments.split("\n", 1)

    # Define the prompt
    prompt = f"""
    You have been given the title and comments of a video. The title is '{title}' and the comments include '{comments}'. As an AI language model, your job is to generate a single, engaging, and complete sentence as a commentary. The sentence should incorporate the title seamlessly, and you are not allowed to not start the sentence without doing so directly with a verb, encouraging the viewer to take action (use the context of the title and comments to choose your verb choice and be creative in your verb choice.). Aim to highlight the unique, humorous, or heartwarming aspects of the video, and ensure variety in the sentence structures and openings to keep things interesting. Make sure your sentence ends with a period ('.'). Avoid repetitive introductions like 'You'll want to see' or 'You'll be captivated'. Let's get creative and make the viewer eager to watch the video! Ready? Go!
    """

    # Generate the commentary
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ],
        max_tokens=60  # Increase max_tokens if necessary
    )

    commentary = response['choices'][0]['message']['content']
    
    # Use NLTK's sentence tokenizer to split the commentary into sentences
    sentences = nltk.tokenize.sent_tokenize(commentary)

    # Take the first sentence only
    first_sentence = sentences[0]
    
    # Print out the commentary
    print("Generated commentary for " + comments_file + ": " + first_sentence)

    # Write the commentary to a file
    with open(os.path.join(commentary_dir, commentary_file), "w", encoding="utf-8") as f:
        f.write(first_sentence)
