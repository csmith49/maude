from darknet import loadConfigDir, modelFromConfig, imageFromFile, videoFromDevice
from assertion import modelAssertion, check, ModelAssertionFailure, add, falsify
from assertion.utility import labels
from logging import getLogger
from time import time
from argparse import ArgumentParser

parser = ArgumentParser("live")
parser.add_argument("-m", "--model", default="../models/yolo")
parser.add_argument("-c", "--confidence", default=0.7, type=float)
args = parser.parse_args()

logger = getLogger("darknet")

# simple flicker implementation
# note we're getting exactly three frames
@modelAssertion(window=3)
def threeFlicker(context):
    f1, f2, f3 = context
    # check the intersection of f1 and f3
    for label in labels(f1) & labels(f3):
        if label not in labels(f2):
            falsify("3-Flicker on label {}".format(label))

# apparition checking
@modelAssertion(window=3)
def apparition(context):
    f1, f2, f3 = context
    for label in labels(f2):
        if label not in labels(f1) and label not in labels(f3):
            falsify("Apparition of {} appearing".format(label))

# now actually do something

print("Initializing...")
print(args.model)
cfg = loadConfigDir(args.model)
model = modelFromConfig(cfg)

print("Model loaded. Starting video device...")
video = videoFromDevice()

from cv2 import waitKey, imshow

for frame in video:
    # let's do some timing too
    start = time()
    predictions = model.annotateImage(frame, 0.5, 0.5, minConfidence=args.confidence)
    frame.show(wait=False)
    stop = time()

    # how long did that take, and what kind of FPS are we getting?
    duration = stop - start
    fps = int(1 / duration)
    logger.info("[PERFORMANCE] Frame took %f seconds (%d FPS)", duration, fps)

    # add the predictions to the assertion checker and check
    add(predictions)
    check()

    if waitKey(1) & 0xFF == ord('q'):
        break