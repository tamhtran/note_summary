# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import os

DIR = "/Users/ttran/PyCharmProjects/NoteSummary/audio"


def get_speech_summary(transcription, temperature=0):
    system_prompt = "I will provide you a transcript of a conversation between multiple people. I want you to restructure it and provide the summary in bullet points and md markdown format."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response['choices'][0]['message']['content']


def read_subtitle_file(filename):
    """Read a subtitle file and return the combined text of all the lines in the file"""
    with open(filename, 'r') as file:
        lines = file.readlines()

    combined_text = ''
    for line in lines:
        # Skip lines with timestamps or empty lines
        if '-->' in line or line.strip().isdigit() or not line.strip():
            continue
        combined_text += line.strip() + '. '

    return combined_text


def get_speech_and_summary(filename):
    """Obtain the transcription and summary of a speech from an audio file and save them to a file with the same name as the audio file, but with a different extension (e.g. .m4a -> .md)  """

    print(f"Processing {filename}...")
    if filename.endswith(".m4a"):
        audio_filepath = os.path.join(DIR, filename)
        trans_filepath = os.path.join(DIR, filename.replace(".m4a", ".md"))

        # if transcription file exists, skip
        if not os.path.exists(trans_filepath):
            print("Transcription file does not exist. Creating transcription file...")
            # transcribe audio file
            audio_file = open(audio_filepath, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            transcription = transcript.text

            # save string to a file
            with open(trans_filepath, "w") as f:
                f.write(transcription)
            print("Transcription saved at " + trans_filepath)
        else:
            # print("Transcription file already exists. Skipping transcription...")
            transcription = None

    elif filename.endswith(".srt"):
        trans_filepath = os.path.join(DIR, filename.replace(".srt", ".md"))
        # if transcription file exists, skip

        if not os.path.exists(trans_filepath):
            print("Transcription file does not exist. Creating transcription file...")
            # transcribe audio file
            transcription = read_subtitle_file(os.path.join(DIR, filename))

            # save string to a file
            with open(trans_filepath, "w") as f:
                f.write(transcription)
            print("Transcription saved at " + trans_filepath)
        else:
            # print("Transcription file already exists. Skipping transcription...")
            transcription = None

    # if summary file exists, skip
    summary_filepath = os.path.join(DIR, filename.replace(".m4a", ".summary.md").replace(".srt", ".summary.md"))
    if not os.path.exists(summary_filepath):
        print("Summary file does not exist. Creating summary file...")
        if transcription is None:
            # get transcription from trans_filepath
            with open(trans_filepath, "r") as f:
                transcription = f.read()

        # get summary from transcription
        if transcription is not None:
            speech_summary = get_speech_summary(transcription)

        # save summary to a file
        with open(summary_filepath, "w") as f:
            f.write(speech_summary)

        print("Summary saved at " + summary_filepath)
    # else:
    # print("Summary file already exists. Skipping summary...")

    print("Done processing " + filename + "\n")


if __name__ == '__main__':
    "if filename is not found with either .md extension or .summary.md extension, then process it." \
    "This is to prevent reprocessing files that have already been processed." \
    "This is useful if you want to stop the program and resume it later."

    for filename in os.listdir(DIR):
        if filename.endswith(".m4a") or filename.endswith(".srt"):
            # if filename is not found with either .md extension or .summary.md extension, then process it
            if (not os.path.exists(os.path.join(DIR, filename.replace(".m4a", ".md").replace(".srt", ".md")))) or (
            not os.path.exists(os.path.join(DIR, filename.replace(".m4a", ".summary.md").replace(".srt", ".summary.md")))):
                get_speech_and_summary(filename)
