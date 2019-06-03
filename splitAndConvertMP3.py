import os
import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence

def splitAndConvertMP3(path):
    sound = AudioSegment.from_mp3(path)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)
    db = sound.dBFS
    chunks = split_on_silence(sound, min_silence_len=575, silence_thresh= db - abs(db/3), keep_silence=350)
    print(len(chunks))
    for i, chunk in enumerate(chunks):
        newPath = path[0:-12] + str(i) + '.wav'
        chunk.export(newPath, format='wav')


if __name__ == '__main__':
    splitAndConvertMP3(sys.argv[1])