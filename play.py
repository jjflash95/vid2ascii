import os
import sys
import getopt
import time


REQUIRED = ['folder']


def sorted_files(path):
    files = os.listdir(folder)
    files = [file.replace('.txt', '') for file in files]
    sorted(files, key=lambda x: (x[0], int(x[1:])))
    return ["%s.txt" % file for file in files]


opts, args = getopt.getopt(sys.argv[1:], "", ["folder=", "fps="])

args = {val[0].strip('--'): val[1] for val in opts}

for arg in REQUIRED:
    if arg not in args:
        exit("%s missing." % arg)

folder = args.get('folder')
fps = int(args.get('fps'))
framesec = 1 / fps

files = sorted_files(folder)

f = open("%s/%s" % (folder, files[0]), 'r')
count = 0
for file in files[1:]:
    start = time.time()
    count += 1
    text = f.read()
    f.close()
    sys.stdout.write(text)
    sys.stdout.write('playing at %d fps, frame: %s\n' %
                     (fps, file.replace('.txt', '')))

    f = open("%s/%s" % (folder, file), 'r')

    while time.time() - start < framesec:
        pass
    os.system('cls' if os.name == 'nt' else "printf '\e[2J\e[3J\e[H'")
    sys.stdout.flush()
