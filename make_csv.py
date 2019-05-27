import os
import csv
import sys

def mp3ToCSV(dir):
    with open(dir + '/podcast.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['wav_filename', 'wav_filesize'])
        for file in sorted(os.listdir(dir)):
            if file[0:6] == "output":
                if os.path.getsize(dir + '/' + file) > 200:
                    writer.writerow([dir + "/" + file, os.path.getsize(dir + "/" + file)])

if __name__ == '__main__':
    mp3ToCSV(sys.argv[1])