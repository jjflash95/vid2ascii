import os
import sys
import getopt
import cv2
from PIL import Image
from frame_to_char import convert, get_available_res
from time import time, strftime, gmtime


REQUIRED = ['video', 'folder']

opts, args = getopt.getopt(
    sys.argv[1:], "", ["video=", "folder=",
                       "res_split=", "available_res_splits="]
)
args = {val[0].strip('--'): val[1] for val in opts}


def save(asciiframe, path, cframe, frames):
    with open('%s/%s.txt' % (path, str(cframe).zfill(len(str(frames)))), 'w') as f:
        f.write(asciiframe)

for arg in REQUIRED:
    if arg not in args:
        exit(arg)

video = args.get('video')
folder = args.get('folder')

if not os.path.isdir(folder):
    try:
        os.mkdir(folder)
    except Exception as e:
        exit('could not make folder %s' % folder)

vidcap = cv2.VideoCapture(video)
frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = vidcap.get(cv2.CAP_PROP_FPS)

cframe = 0

success, image = vidcap.read()

split = int(args.get('res_split', 0))

if "available_res_splits" in args.keys():
    frame = Image.fromarray(image).convert('RGB')
    rsplit = get_available_res(frame)
    print("available resolution splits: %s for %dx%dp video" % (rsplit, *frame.size))
    if not args.get('res_split'):
        split = rsplit[0]


while success:
    start = time()
    image = Image.fromarray(image).convert('RGB')
    sframe = str(cframe).zfill(len(str(frames)))
    save(convert(image, split), folder, sframe, frames)

    success, image = vidcap.read()
    cframe += 1
    framesec = 1 / (time() - start)
    etasec = (frames - cframe) / framesec
    print('%s of %d frames at %.2f frames/sec, eta: %s' % (
        sframe,
        frames,
        framesec,
        strftime("%H:%M:%S", gmtime(etasec))),
        end='\r')
