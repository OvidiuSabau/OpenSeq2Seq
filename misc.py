from pydub import AudioSegment
from os import listdir
from sys import argv
import csv
import pandas as pd
import boto3


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

def processMozzilaCSV(dir, csvFile):
    path2CSV = dir + csvFile
    # df = pd.read_csv(path2CSV, encoding='utf-8')
    with open(path2CSV, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[0], end='\n\n')
    # # two_columns = original_df[['path', 'sentence']]
    # print(two_columns.shape)


def testGetObject():
    s3_bucket_name = 'adswizz-randi-jasper-dev'
    s3_file = 'test/22222222222222222222222.json'
    s3_client = boto3.client('s3')
    s3_client.download_file(s3_bucket_name, s3_file, 's3_file.json')

if __name__ == '__main__':
    # processMozzilaCSV(argv[1], argv[2])
    testGetObject()
