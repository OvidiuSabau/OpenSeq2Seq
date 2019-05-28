import sys
import re

def infer2text(path):
    with open(path, 'r') as textfile:
        file = textfile.readlines()[1:]
        file = [x[x.find('.wav,')+5:] for x in file]
        file = [x.replace('\n', '') for x in file]
    final = ''
    for x in file:
        final += x + ' '

    with open(path[:-16] + 'final_prediction.txt', 'w') as textfile:
        textfile.write(final)

    return final

if __name__ == '__main__':
    infer2text(sys.argv[1])