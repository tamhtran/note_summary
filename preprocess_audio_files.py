import os
import shutil
from pydub import AudioSegment


ORIGINAL_AUDIO_DIR = "/Users/ttran/Downloads"
NEW_AUDIO_DIR = "/Users/ttran/PyCharmProjects/NoteSummary/audio"

# Move all audio files from ORIGINAL_AUDIO_DIR to NEW_AUDIO_DIR
# Note: this is a one-time operation


def print_file_size(filename):
    # print file size in mb
    print(f"File size of {filename}: {os.path.getsize(filename) / 1000000} MB")


def split_m4a_file(file_path):
    MAX_SIZE_MB = 25
    MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024  # Convert MB to Bytes

    # Check file size
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size / 1024 / 1024:.2f} MB")

    if file_size > MAX_SIZE_BYTES:
        audio = AudioSegment.from_file(file_path, format='m4a')
        duration = len(audio)  # Duration in milliseconds
        part_duration = (MAX_SIZE_BYTES / file_size) * duration  # Split ratio

        start = 0
        part_num = 1

        while start < duration:
            end = min(start + part_duration, duration)
            part = audio[start:end]

            # Construct new filename
            base, ext = os.path.splitext(file_path)
            new_filename = f"{base}_part{part_num}{ext}"

            # Export part
            # part.export(new_filename, format='m4a')
            part.export(new_filename, format='ipod', codec='aac')
            print(f"Part {part_num} saved as {new_filename}")

            start = end
            part_num += 1
    else:
        print("File size is within the limit, no splitting required.")


if __name__ == '__main__':
    # 1. move all audio files from ORIGINAL_AUDIO_DIR to NEW_AUDIO_DIR
    # 2. split if necessary
    for filename in os.listdir(ORIGINAL_AUDIO_DIR):
        if filename.endswith(".m4a"):
            shutil.move(os.path.join(ORIGINAL_AUDIO_DIR, filename), os.path.join(NEW_AUDIO_DIR, filename))
            print(f"Moved {filename} to {NEW_AUDIO_DIR}")
            split_m4a_file(os.path.join(NEW_AUDIO_DIR, filename))
            print()