import os
import sys
from pydub import AudioSegment

def splitAndConvertMP3(path):
    sound = AudioSegment.from_mp3(path)
    length = sound.duration_seconds
    for i in range(0, (int(length)-1) * 1000, 5000):

        newPath = path[0:-12] + str(i//1000) + '.wav'
        sound[i:i+5000].export(newPath, format='wav')


if __name__ == '__main__':
    splitAndConvertMP3(sys.argv[1])