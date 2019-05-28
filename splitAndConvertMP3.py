import os
import sys
from pydub import AudioSegment

def splitAndConvertMP3(path, interval):
    interval = int(interval)
    sound = AudioSegment.from_mp3(path)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)

    length = sound.duration_seconds
    for i in range(0, (int(length)-1) * 1000, interval * 1000):

        newPath = path[0:-12] + str(i//1000) + '.wav'
        sound[i:i + interval * 1000].export(newPath, format='wav', )


if __name__ == '__main__':
    splitAndConvertMP3(sys.argv[1])