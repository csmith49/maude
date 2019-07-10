from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT

from os.path import abspath
from .image import Image

class Video:
    # assume we're passed a handle - maybe from a file, maybe a camera
    def __init__(self, handle):
        self._handle = handle

    # destructor just makes sure to release the handle
    def __del__(self):
        self._handle.release()

    # try and get the frame count
    @property
    def frameCount(self):
        try:
            return self._handle.get(CAP_PROP_FRAME_COUNT)
        except:
            return None

    # we'll treat a video as a generator
    def __iter__(self):
        return self
    
    def __next__(self):
        grabbed, frame = self._handle.read()
        if grabbed:
            return Image(frame)
        else:
            raise StopIteration()

# making video handles
def videoFromFile(videoPath):
    path = abspath(videoPath)
    handle = VideoCapture(path)
    return Video(handle)

def videoFromDevice(deviceIndex=0):
    handle = VideoCapture(deviceIndex)
    return Video(handle)