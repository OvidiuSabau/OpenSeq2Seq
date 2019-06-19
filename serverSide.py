from webTranscriptToTXT import webTranscriptToTXT
from infer2text import infer2text
from splitAndConvertMP3 import splitAndConvertMP3
from makeCSV import makeCSV
import sys
from subprocess import call
import os
from time import time
from compareWER import quickWER
from urllib.request import urlretrieve
from pydub import AudioSegment

target_dir = 'server-side-testing/'
base_config_file = 'config.py'

message = dict({
    "client": "Absolute-Berry",
    "masterId": "ac3f2458-0c6b-4fc5-ae61-8be3a4c63043-1",
    "showTitle": "The Dave Berry Breakfast Show",
    "episodeHashId": "2b481295ed34c90ec24599701265c1f34c455c491369b9549b98b4e168cfc8ba",
    "episodeUrl": "http://podcast.timlradio.co.uk/Berry/20190614122932.mp3?awCollectionId=Berry&awEpisodeId=91985?aisGetOriginalStream=true",
    "episodeTitle": "Breakfast - The Boss was stripped naked and cavity searched.",
    "language": "en-us",
    "sttProvider": "watson",
    "pubDate": 1560488700,
    "transcodeRequestId": "3c2e68bb-53d4-45eb-a5bb-297b56f75e56",
    "ffmpegFileDuration": "00:40:40.99"})

client_dir = target_dir + message['client'] + '/'
if not os.path.isdir(client_dir):
    print('** Creating {} folder **'.format(client_dir))
    call_args = ['mkdir', client_dir]
    call(call_args)

episode_dir = client_dir + message['episodeTitle']
print('** Creating {} folder **'.format(episode_dir))
call_args = ['mkdir', episode_dir]
call(call_args)

mp3_location = episode_dir + '/original.mp3'
print('** Downloading MP3 File **')
urlretrieve(message['episodeUrl'], mp3_location)

print('** Processing MP3 File **')
call_args = ['mkdir', episode_dir + '/wavs']
call(call_args)
splitAndConvertMP3(mp3_location)

print('** Creating Model Input File **')
makeCSV(episode_dir + '/wavs')

print('** Creating Config File **')
with open(base_config_file, 'r') as config_file:
    config = config_file.read()
config = config.replace('# insert path to csv here', '\'' + episode_dir + '/model_input.csv' + '\'')
with open(episode_dir + '/config.py', 'w') as config_file:
    config_file.write(config)

print('** Calling Model From Terminal **')
call_args = ['python', 'run.py', '--config_file=' + episode_dir + "/config.py", '--mode=infer',
             '--infer_output_file=' + episode_dir + '/model_output.txt']
call(call_args)

print('** Writing Transcription')
infer2text(episode_dir + '/model_output.txt')