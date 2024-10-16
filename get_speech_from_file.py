from openai import OpenAI
import os

# Ensure to set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DIR = "/Users/ttran/PyCharmProjects/NoteSummary/audio"


def get_speech_summary(transcription, temperature=0):
    system_prompt = (
        # "I will provide you a transcript of a conversation between multiple people. "
        # "I want you to restructure it and provide the summary in bullet points and md markdown format."
        """You are an expert note-taker specializing in technical concepts and historical trends. Your task is to analyze the provided podcast transcription and create a structured summary following these guidelines:
1. Create a numbered list of main topics discussed in the podcast.
2. For each main topic:
- Use a level 2 header (##) to introduce the topic.
- Provide a brief overview of the topic in 1-2 sentences.
- Create a bullet point list of subtopics, which may include:
• Key tactics or strategies
• Main points or arguments
• Historical context or background information
- If the topic focuses on a specific company's story or a particular trend, maintain as much detail as possible without over-summarizing.

3.Ensure your notes are comprehensive yet concise, capturing the essence of the discussion without unnecessary repetition.
4. Use clear and precise language, defining any technical terms or jargon when first introduced.
5. If applicable, include any notable quotes from the podcast using proper markdown formatting.
6. Maintain chronological order of topics as they appear in the podcast, unless a different logical order is more appropriate for understanding the content.
7. If the podcast mentions any numerical data, statistics, or dates, include them in your notes for accuracy.
8. At the end of your notes, provide a brief conclusion summarizing the key takeaways from the entire podcast.
Please analyze the provided podcast transcription and create a structured summary following these guidelines."""
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcription},
        ],
    )
    return response.choices[0].message.content


def read_subtitle_file(filename):
    """Read a subtitle file and return the combined text of all the lines in the file"""
    with open(filename, "r") as file:
        lines = file.readlines()

    combined_text = ""
    for line in lines:
        # Skip lines with timestamps or empty lines
        if "-->" in line or line.strip().isdigit() or not line.strip():
            continue
        combined_text += line.strip() + ". "

    return combined_text


def get_speech_and_summary(filename):
    """Obtain the transcription and summary of a speech from an audio file and save them to a file with the same name as the audio file, but with a different extension (e.g. .m4a -> .md)"""

    print(f"Processing {filename}...")
    if filename.endswith(".m4a"):
        audio_filepath = os.path.join(DIR, filename)
        trans_filepath = os.path.join(DIR, filename.replace(".m4a", ".md"))

        # if transcription file exists, skip
        if not os.path.exists(trans_filepath):
            print("Transcription file does not exist. Creating transcription file...")
            # transcribe audio file
            with open(audio_filepath, "rb") as audio_file:
                transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
                transcription = transcript["text"]

            # save string to a file
            with open(trans_filepath, "w") as f:
                f.write(transcription)
            print("Transcription saved at " + trans_filepath)
        else:
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
            transcription = None

    # if summary file exists, skip
    summary_filepath = os.path.join(
        DIR, filename.replace(".m4a", ".summary.md").replace(".srt", ".summary.md")
    )
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
    print("Done processing " + filename + "\n")


if __name__ == "__main__":
    # Process audio and subtitle files, avoiding reprocessing of already processed files
    for filename in os.listdir(DIR):
        if filename.endswith(".m4a") or filename.endswith(".srt"):
            # if filename is not found with either .md extension or .summary.md extension, then process it
            md_path = os.path.join(
                DIR, filename.replace(".m4a", ".md").replace(".srt", ".md")
            )
            summary_md_path = os.path.join(
                DIR,
                filename.replace(".m4a", ".summary.md").replace(".srt", ".summary.md"),
            )
            if not os.path.exists(md_path) or not os.path.exists(summary_md_path):
                get_speech_and_summary(filename)
