# only import from cv2 what we need - need opencv > 3.4
from cv2 import imread
from cv2.dnn import readNetFromDarknet, blobFromImage, NMSBoxes

# some minor matrix stuff
from numpy import argmax, array
from numpy.random import randint

# and we'll be constructing predictions
from .prediction import Prediction, NMS

# a simple utility
def randomColor():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

# models wrap dnn models
class Model:
    def __init__(self, cfgPath, weightsPath, names):
        self._model = readNetFromDarknet(cfgPath, weightsPath)
        self._names = names

        self._colors = {name : randomColor() for name in self._names}

        # extract output layer names
        layerNames = self._model.getLayerNames()
        self._layerNames = [layerNames[i[0] - 1] for i in self._model.getUnconnectedOutLayers()]

    # classification is straightforward - just run the model
    def predictionsFromImage(self, image, minConfidence=0):
        blob = image.toBlob()
        self._model.setInput(blob)

        # the actual running - if you want timing info, wrap it here
        layerOutputs = self._model.forward(self._layerNames)

        # iterate over all output layers and accumulate the predictions
        predictions = []
        for output in layerOutputs:
            for detection in output:
                # pull out label and confidence
                scores = detection[5:]
                labelIndex = argmax(scores)
                confidence = scores[labelIndex]
                label = self._names[labelIndex]

                # if we're confident enough, store the prediction
                if confidence >= minConfidence:
                    # compute integer box description
                    box = detection[0:4] * array([image.width, image.height, image.width, image.height])
                    (cx, cy, w, h) = box.astype("int")
                    # returned x and y are actually the center, so let's convert
                    x = int(cx - (w / 2))
                    y = int(cy - (h / 2))

                    # construct and store
                    prediction = Prediction(x=x, y=y, w=w, h=h, confidence=confidence, label=label)
                    predictions.append(prediction)
        
        # and finally, return
        return predictions

    # given an image, annotate it
    def annotateImage(self, image, confidence, threshold, minConfidence=0):
        predictions = self.predictionsFromImage(image, minConfidence)
        # predictions = NMS(predictions, confidence, threshold)
        for prediction in predictions:
            image.drawPrediction(prediction, self.labelColor(prediction.label))
        return predictions

    # get label colors
    def labelColor(self, label):
        return self._colors[label]

# unwrap the configuration object
def modelFromConfig(config):
    return Model(config.cfgPath, config.weightsPath, config.names)