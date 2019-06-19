from pydub import AudioSegment
from os import listdir
from sys import argv
import csv
import pandas as pd

def getTotalLength(dir):

    n = 0
    for file in listdir(dir):
        n += AudioSegment.from_wav(dir + '/' + file).duration_seconds

    print(n)


def splitCSV(path):
    shuffled_df = pd.read_csv(path).sample(frac=1)
    n_test_rows = int(shuffled_df.shape[0] / 10)
    shuffled_df[:n_test_rows].to_csv('test.csv', index=False)
    shuffled_df[n_test_rows:].to_csv('train.csv', index=False)


if __name__ == '__main__':
    splitCSV(argv[1])