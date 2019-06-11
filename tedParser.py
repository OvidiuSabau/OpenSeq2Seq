import os
from sys import argv
from sphfile import SPHFile
import re
import pandas as pd
import csv

def inAlphabet(word):

    alphabet = 'abcdefghijklmnopqrstuvwxyz\''
    for letter in word:
        if letter not in alphabet:
            return False
    return True

def parseEpisode(path2Audio, path2Text, targetDirectory):

    branchList = path2Text.split('/')
    lastField = branchList[len(branchList)-1]
    fileName = lastField[:-4]

    full_audio = SPHFile(path2Audio)

    with open(path2Text, 'r') as file:
        full_file = file.readlines()

    rows = []
    for i, line in enumerate(full_file):
        body = line.split(fileName)[2]
        bodySplit = body.split('<NA>')
        numbers = bodySplit[0].split()
        start = float(numbers[0])
        end = float(numbers[1])
        regex = '<unk>'
        text = re.sub(regex, '', bodySplit[1])
        text = ' '.join([x for x in text.split() if inAlphabet(x)])
        text = text.replace(' \'', '\'')
        write_path = targetDirectory + '/' + fileName + '-{}.wav'.format(i)
        full_audio.write_wav(write_path, start, end)
        size = os.path.getsize(write_path)
        rows.append((write_path, size, text))

    return rows


def parseFolders(dirAudio, dirText, targetDirectory):

    transcripts = []
    audioFiles = sorted(os.listdir(dirAudio))
    textFiles = sorted(os.listdir(dirText))
    zippedFiles = zip(audioFiles, textFiles)
    for audio, text in zippedFiles:
        transcripts += parseEpisode(dirAudio + '/' + audio, dirText + '/' + text, targetDirectory)

    with open('model_input.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['wav_filename', 'wav_filesize', 'transcript'])
        for row in transcripts:
            writer.writerow(row)

if __name__ == '__main__':
    parseFolders(argv[1], argv[2], argv[3])
