# MAuDe

Model Assertions for object Detection networks.

## Models

You'll have to provide models yourself, as the weight files are pretty big. Take a look at [YOLO](https://www.pjreddie.com/darknet/yolo/) for a model and how to install it.

Models are stored in a directory containing a configuration file `config.toml`. Each configuration file has 3 entries, all of which are paths to files: `name` references the name file, which is a label index, `cfg`, which hosts the network configuration, and `weights`, which has the network weights. An example file for YOLO v3 is given below:

```toml
names="coco.names"
cfg="yolov3.cfg"
weights="yolov3.weights"
```

This is a flat configuration, e.g. we expect `coco.names` to appear in the same directory.

## Resources

We're based on [OpenCV](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html), although we use [YOLO](https://www.pjreddie.com/darknet/yolo/) as our object detection model.
