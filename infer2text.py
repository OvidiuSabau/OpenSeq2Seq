import sys
import re
from autocorrect import spell

def infer2text(path):


    with open(path, 'r') as textfile:
        file = textfile.readlines()[1:]
        file = [x[x.find('.wav,')+5:] for x in file]
        file = [x.replace('\n', '') for x in file]
        file = ' '.join([x for x in file])

    with open(path[:-16] + 'prediction_no_spellcheck.txt', 'w') as textfile:
        textfile.write(file)

        file = file.split()
        file = ' '.join([spell(word) for word in file])

    with open(path[:-16] + 'prediction_with_spellcheck.txt', 'w') as textfile:
        textfile.write(file)

    return file
if __name__ == '__main__':
    infer2text(sys.argv[1])