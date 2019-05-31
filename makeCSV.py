import os
import csv
import sys

def makeCSV(dir):
    with open(dir + '/model_input.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['wav_filename', 'wav_filesize'])
        files = os.listdir(dir)
        step = 0
        i = 1
        while not step:
            if os.path.isfile(path= dir + '/' + str(i) + '.wav'):
                step = i
            i += 1
        last = 0
        for file in files:
            try:
                n = int(file[:-4])
                if n > last:
                    last = n
            except:
                pass

        for i in range(0, last + step, step):
            writer.writerow([dir + "/" + str(i) + '.wav', os.path.getsize(dir + "/" + str(i) + '.wav')])


if __name__ == '__main__':
    makeCSV(sys.argv[1])