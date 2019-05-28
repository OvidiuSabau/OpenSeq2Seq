import os
import csv
import sys

def makeCSV(dir):
    with open(dir + '/model_input.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['wav_filename', 'wav_filesize'])
        for file in sorted(os.listdir(dir)):
            if file[-4:] == ".wav" and not 'original.wav' in file:
                if os.path.getsize(dir + '/' + file) > 200:
                    writer.writerow([dir + "/" + file, os.path.getsize(dir + "/" + file)])

if __name__ == '__main__':
    makeCSV(sys.argv[1])