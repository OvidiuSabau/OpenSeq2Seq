from webTranscriptToTXT import webTranscriptToTXT
from infer2text import infer2text
from splitAndConvertMP3 import splitAndConvertMP3
from makeCSV import makeCSV
import sys
from subprocess import call
import os
from time import time
from compareWER import quickWER

def doItAll(dir):


    t0 = time()
    # Convert from MP3 to WAV, change channels to 1
    # change sample-rate to 16000, and split every 5 seconds


    call(['mkdir', dir + '/wavs'])

    print('\n\n ** Splitting and converting MP3')
    splitAndConvertMP3(dir + '/original.mp3')

    print('\n\n ** Reading base config file')
    # Read Base Config File
    with open('config.py', 'r') as config_file:
        config = config_file.read()

    print('\n\n ** Creating model_input.csv')
    # Create the corresponding CSV file, model_input.csv
    makeCSV(dir + '/wavs')

    print('\n\n ** Creating config file')
    # Create the config file for this particular model
    config = config.replace("# insert path to csv here", "\"" + dir + "/wavs/model_input.csv\"")
    with open(dir + "/config.py", 'w') as config_file:
        config_file.write(config)

    print('\n\n ** Calling model from terminal')
    # Call the model from terminal
    # call_args = ['python', 'run.py', '--config_file=' + dir + "/config.py", '--mode=infer', '--infer_output_file= model_output.pickle']
    call_args = ['python', 'run.py', '--config_file=' + dir + "/config.py", '--mode=infer', '--infer_output_file=' + dir + '/model_output.txt']
    call(call_args)

    infer2text(dir + '/model_output.txt')

    try:
        webTranscriptToTXT(dir + '/original.txt')
        print('Truth/Model W/ Spellcheck: ' + str(quickWER(dir + '/converted_transcript.txt', dir + '/prediction_with_spellcheck.txt')))
        print('Truth/Model W/O Spellcheck: ' + str(quickWER(dir + '/converted_transcript.txt', dir + '/prediction_no_spellcheck.txt')))
    except:
        pass

    try:
        print('Truth/Podscribe: ' + str(quickWER(dir + '/converted_transcript.txt', dir + '/podscribe.txt')))
        print('Podscribe/Model: ' + str(quickWER(dir + '/podscribe.txt', dir + '/prediction_with_spellcheck.txt')))

    except:
        pass

    # # If web transcript is provided, parse it from the NPR style and compare the WER
    # if os.path.isfile(dir + '/original.txt'):
    #     print('\n\n Calculating WER')
    #     original = webTranscriptToTXT(dir + '/original.txt')
    #     predicted = infer2text(dir + '/model_output.txt')
    #     compareWer()
    #
    # else:
    #     print('No web transcript provided')
    #     infer2text(dir + '/model_output.txt')
    print(time()-t0)

if __name__ == '__main__':
    doItAll(sys.argv[1])