from dataclasses import dataclass
from cv2.dnn import NMSBoxes

# predictions are just a convenient wrapper for object classifications
@dataclass
class Prediction:
    confidence: float
    label: str
    x: int
    y: int
    w: int
    h : int

    # in order to interface with NMSBoxes, we need to turn predictions to boxes
    def toBox(self):
        return [self.x, self.y, self.w, self.h]

    # break out to box, confidence, label tuple
    def toNMSTuple(self):
        return self.toBox(), self.confidence, self.label

# convert a list of predictions to a tuple of box-list, conf-list, and label-list
def predictionsToNMSLists(predictions):
    boxes, confidences, labels = [], [], []
    for prediction in predictions:
        box, confidence, label = prediction.toNMSTuple()
        boxes.append(box)
        confidences.append(confidence)
        labels.append(label)
    return boxes, confidences, labels

# given indices from NMS output, convert lists back to predictions
def NMSListsToPredictions(ids, boxes, confidences, labels):
    predictions = []
    for i in ids.flatten():
        x, y, w, h = boxes[i]
        confidence = confidences[i]
        label = labels[i]
        prediction = Prediction(x=x, y=y, w=w, h=h, confidence=confidence, label=label)
        predictions.append(prediction)
    return predictions

def NMS(predictions, confidence, threshold):
    boxes, confidences, labels = predictionsToNMSLists(predictions)
    ids = NMSBoxes(boxes, confidences, confidence, threshold)
    return NMSListsToPredictions(ids, boxes, confidences, labels)