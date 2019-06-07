import os
import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence
from sox import Transformer

def splitAndConvertMP3(path):
    sound = AudioSegment.from_mp3(file=path)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)
    db = sound.dBFS
    target_dBFS = -24.7
    sound = sound.apply_gain(target_dBFS-db)
    # quarter_second_silence = AudioSegment.silent(duration=250, frame_rate=16000)
    # # silence_db = quarter_second_silence.dBFS
    # target_silence_dBFS = --38
    # # quarter_second_silence.apply_gain(target_silence_dBFS -1 - silence_db)

    # chunks = split_on_silence(sound, min_silence_len=400, silence_thresh=target_silence_dBFS, keep_silence=220)
    # current_batch_duration = 0
    # current_batch_sounds = quarter_second_silence
    # current_batch_id = 0
    # for chunk in chunks:
    #     temp = current_batch_sounds  + chunk
    #     if temp.duration_seconds > 12:
    #         newPath = path[0:-12] + 'wavs/' + str(current_batch_id) + '.wav'
    #         current_batch_sounds.export(newPath, format='wav')
    #         current_batch_sounds = chunk
    #         current_batch_id += 1
    #     else:
    #         current_batch_sounds = temp

    duration = int(sound.duration_seconds)
    max_duration = 12 * 1000
    min_duration = 5 * 1000
    silence_window = 200
    audio_slice_idx = 0
    i = 0
    while i < duration * 1000:

        # select 16 seconds of audio
        chunk = sound[i:i+max_duration]
        min_dBFS = 1000000
        min_dBFS_position = -1

        # Look for the location of the minimum dBFS in the 16 second window
        for j in range(0, max_duration, silence_window):
            t_db = chunk[j:j+silence_window].dBFS
            if t_db < min_dBFS and j > min_duration:
                min_dBFS = t_db
                min_dBFS_position = j

        newPath = path[0:-12] + 'wavs/' + str(audio_slice_idx) + '.wav'
        audio_slice = sound[i:i + min_dBFS_position + silence_window]
        audio_slice.export(newPath, format='wav')
        # print(audio_slice.duration_seconds)
        audio_slice_idx += 1

        # if audio_slice_idx % 100 == 0:
        #     print(i)

        i += min_dBFS_position + silence_window


if __name__ == '__main__':
    splitAndConvertMP3(sys.argv[1])