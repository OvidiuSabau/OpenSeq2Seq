import json
import os
from subprocess import call
from urllib.request import urlretrieve

import boto3

from infer2text import infer2text
from makeCSV import makeCSV
from splitAndConvertMP3 import splitAndConvertMP3

target_dir = 'server-side-testing/'
base_config_file = 'config.py'
s3_client = boto3.client('s3')
s3_bucket_name = 'adswizz-randi-jasper-dev'
sqs_queue_name = 'randi-podscribe-jasper'
sqs_resource = boto3.resource('sqs')
sqs_client = boto3.client('sqs')
queue = sqs_resource.get_queue_by_name(QueueName=sqs_queue_name)

# episode_info = dict({
#     "client": "Absolute-Berry",
#     "masterId": "ac3f2458-0c6b-4fc5-ae61-8be3a4c63043-1",
#     "showTitle": "The Dave Berry Breakfast Show",
#     "episodeHashId": "2b481295ed34c90ec24599701265c1f34c455c491369b9549b98b4e168cfc8ba",
#     "episodeUrl": "http://podcast.timlradio.co.uk/Berry/20190614122932.mp3?awCollectionId=Berry&awEpisodeId=91985?aisGetOriginalStream=true",
#     "episodeTitle": "Breakfast - The Boss was stripped naked and cavity searched.",
#     "language": "en-us",
#     "sttProvider": "watson",
#     "pubDate": 1560488700,
#     "transcodeRequestId": "3c2e68bb-53d4-45eb-a5bb-297b56f75e56",
#     "ffmpegFileDuration": "00:40:40.99"})

while True:

    print('** Waiting For Message **')
    message = queue.receive_messages()
    prevHashId = None


    # If there are only few messages in the queue, sometimes this doesn't receive any messages
    if len(message) > 0:

        if not os.path.isdir(target_dir):
            call_args = ['mkdir', target_dir]
            call(call_args)

        print('** Handling Message **')
        message = message[0]
        string_episode_info = message.body
        receipt_handle = message.receipt_handle
        episode_info = json.loads(string_episode_info)

        # Sometimes we receive the same message multiple times; We check against this
        if prevHashId == episode_info['episodeHashId']:
            continue
        prevHashId = episode_info['episodeHashId']

        client_dir = target_dir + episode_info['client'] + '/'
        if not os.path.isdir(client_dir):
            print('** Creating {} folder **'.format(client_dir))
            call_args = ['mkdir', client_dir]
            call(call_args)

        episode_dir = client_dir + episode_info['episodeTitle']
        print('** Creating {} folder **'.format(episode_dir))
        call_args = ['mkdir', episode_dir]
        call(call_args)

        mp3_location = episode_dir + '/original.mp3'
        print('** Downloading MP3 File **')
        urlretrieve(episode_info['episodeUrl'], mp3_location)

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

        print('** Writing Transcription **')
        transcript = infer2text(episode_dir + '/model_output.txt')

        print('** Uploading to Bucket **')

        transcript_dict = dict({'jasper_transcript': transcript})
        string_transcript_dict = json.dumps(transcript_dict)
        full_dict = dict({'Body': string_transcript_dict})

        system_full_dict_location = episode_dir + '/full_dict.json'

        with open(system_full_dict_location, 'w') as file:
            json.dump(full_dict, file)

        bucket_transcript_location = episode_info['client'] + '/' + episode_info['episodeHashId'] + '.json'
        s3_client.upload_file(system_full_dict_location, s3_bucket_name, bucket_transcript_location)

        sqs_client.delete_message(
            QueueUrl=queue.url,
            ReceiptHandle=receipt_handle
        )


