import sys

from pydub import AudioSegment


def splitAndConvertMP3(path):
    sound = AudioSegment.from_mp3(file=path)
    print(path)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)
    db = sound.dBFS
    target_dBFS = -24.7
    sound = sound.apply_gain(target_dBFS-db)
    duration = int(sound.duration_seconds)
    max_duration = 12 * 1000
    min_duration = 5 * 1000
    silence_window = 200
    audio_slice_idx = 0
    i = 0
    while i < duration * 1000:

        # select max duration seconds of audio
        chunk = sound[i:i+max_duration]
        min_dBFS = 1000000
        min_dBFS_position = -1

        # Look for the location of the minimum dBFS in the duration-window
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