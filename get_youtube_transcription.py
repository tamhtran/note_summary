import re
from youtube_transcript_api import YouTubeTranscriptApi
import get_speech_from_file
import os
import requests
import json

DIR = "/Users/ttran/PyCharmProjects/NoteSummary/audio/youtube"


def get_video_id(url):
    """Obtain the video id from a youtube url"""
    return re.search(r'v=([a-zA-Z0-9-]+)', url).group(1)


def get_transcription_from_video(video_id):
    """Obtain the transcription of a video from its video id"""
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcription = ""
    for line in transcript:
        transcription += line['text'] + " "
    return transcription


def get_title_and_author(video_id):
    """Gets the title and author of a YouTube video from a YouTube URL."""

    # Get the API key from the environment variable.
    api_key = os.environ['YOUTUBE_API_KEY']

    # Make a request to the YouTube API.
    response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}')

    # Get the JSON response from the API.
    json_response = response.json()

    title = json_response['items'][0]['snippet']['title']
    author = json_response['items'][0]['snippet']['channelTitle']

    return title, author


def remove_invalid_characters(filename):
    """Removes all characters that cannot be used in a file name from the given string."""

    # Get a list of all characters that cannot be used in a file name.
    invalid_characters = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', ' ']

    # Create a regex that matches any of the invalid characters.
    invalid_characters_regex = r'[' + ''.join(invalid_characters) + ']'

    # Replace all invalid characters with an empty string.
    filename = re.sub(invalid_characters_regex, '_', filename)

    return filename


def get_speech_and_summary(filename):
    """Obtain the transcription and summary of a speech from an audio file and save them to a file with the same name as the audio file, but with a different extension (e.g. .m4a -> .md)  """

    print(f"Processing {filename}...")
    trans_filepath = os.path.join(DIR, filename + ".md")

    # if transcription file exists, skip
    if not os.path.exists(trans_filepath):
        print("Transcription file does not exist. Creating transcription file...")
        transcription = get_transcription_from_video(video_id)

        # save string to a file
        with open(trans_filepath, "w") as f:
            f.write(transcription)
        print("Transcription saved at " + trans_filepath)
    else:
        # print("Transcription file already exists. Skipping transcription...")
        transcription = None

    # if summary file exists, skip
    summary_filepath = os.path.join(DIR, filename + ".summary.md")
    if not os.path.exists(summary_filepath):
        print("Summary file does not exist. Creating summary file...")
        if transcription is None:
            # get transcription from trans_filepath
            with open(trans_filepath, "r") as f:
                transcription = f.read()

        # get summary from transcription
        if transcription is not None:
            speech_summary = get_speech_from_file.get_speech_summary(transcription)

        # save summary to a file
        with open(summary_filepath, "w") as f:
            f.write(speech_summary)

        print("Summary saved at " + summary_filepath)
    # else:
        # print("Summary file already exists. Skipping summary...")

    print("Done processing " + filename + "\n")


if __name__ == '__main__':
    video_id = get_video_id('https://www.youtube.com/watch?v=XcwY-HRktRA')
    print(f'video_id: {video_id}')

    title, author = get_title_and_author(video_id)
    print(f'Title: {title}')
    print(f'Author: {author}')

    filename = remove_invalid_characters(f'{title} - {author}')
    print(f'filename: {filename}')
    get_speech_and_summary(filename)




