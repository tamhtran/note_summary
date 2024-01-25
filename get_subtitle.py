def read_subtitle_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    combined_text = ''
    for line in lines:
        # Skip lines with timestamps or empty lines
        if '-->' in line or line.strip().isdigit() or not line.strip():
            continue
        combined_text += line.strip() + ' '

    return combined_text

if __name__ == '__main__':
    filename = '/Users/ttran/Documents/GA tech/ML4T/CS7646_Lectures/Decision_Trees_subtitles/367 - Decision Trees Part 1.srt'  # Replace this with your subtitle filename
    combined_text = read_subtitle_file(filename)
    print("Combined text:", combined_text)
