from cv2 import imread, imshow, waitKey, FONT_HERSHEY_SIMPLEX, rectangle, putText
from cv2.dnn import blobFromImage
from os.path import abspath

# images just wrap cv2 images, and give more convenient representations
class Image:
    def __init__(self, image):
        self._image = image
        self.height, self.width = self._image.shape[:2]
    
    # convert to blob so we can pass to model
    def toBlob(self):
        return blobFromImage(self._image, 1 / 255.0, (416, 416), swapRB=True, crop=False)

    # displays the image until a key is pressed
    def show(self, wait=True):
        imshow("MA", self._image)
        if wait:
            waitKey(0)

    # draw a prediction in the image
    def drawPrediction(self, prediction, color):
        # draw rectangle
        x, y, w, h = prediction.toBox()
        rectangle(self._image, (x, y), (x + w, y + h), color, 2)
        # draw label
        text = "{}: {:.4f}".format(prediction.label, prediction.confidence)
        putText(self._image, text, (x, y - 5), FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def imageFromFile(imagePath):
    path = abspath(imagePath)
    image = imread(path)
    return Image(image)