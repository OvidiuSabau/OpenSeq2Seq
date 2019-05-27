import sys
import re

def infer2text(path):
    with open(path, 'r') as textfile:
        file = textfile.read().replace('\n', '')
        regexPattern = ' |data/podcast/output...\.wav'
        file = re.split(regexPattern, file)
    final = ' '.join([x for x in file])
    with open('prediction.txt', 'w') as textfile:
        textfile.write(final)
if __name__ == '__main__':
    infer2text(sys.argv[1])