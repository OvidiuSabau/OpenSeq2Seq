import os
import sys
import re

def webTranscriptToTXT(path):

    with open(path, 'r') as file:
        text = file.read()

    explanations_regex = '\(.*\)'
    name_regex = '.*\:'
    text = re.sub(explanations_regex, '', text)
    text = re.sub(name_regex, '', text)

    with open(path[0:-12] + 'converted_transcript.txt', 'w') as file:
        file.write(text)

if __name__ == '__main__':
    webTranscriptToTXT(sys.argv[1])