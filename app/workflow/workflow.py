from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor
from app.sketch import SketchGizeh
import png
import numpy as np
from pathlib import Path


class Workflow():
    """controls execution of app
    """

    def __init__(self, dataset, imageprocessor, sketch):
        self._dataset = dataset
        self._image_processor = imageprocessor
        self._sketcher = sketch

    def setup(self):
        self._dataset.setup()
        self._sketcher.setup()
        self._image_processor.setup()

    def run(self, path=None):
        """processes an image. If no path supplied, then capture from camera

        :param path: path to an image
        :return:
        """
        if path:
            img = self._image_processor.load_image_into_numpy_array(path)
            boxes, scores, classes, num = self._image_processor.detect(img)
            annotated_img = self._image_processor.annotate_image(img, boxes, classes, scores)
            self._sketcher.draw_object_recognition_results(np.squeeze(boxes),
                                   np.squeeze(classes).astype(np.int32),
                                   np.squeeze(scores),
                                   self._image_processor.labels,
                                   self._dataset)
            self._save_3d_numpy_array_as_png(annotated_img, Path(path).with_name('annotated.png'))
            self._save_3d_numpy_array_as_png(self._sketcher.get_npimage(), Path(path).with_name('cartoon.png'))
        else:
            print('camera capture not implemented yet')

    def _save_3d_numpy_array_as_png(self, img, path):
        """saves a NxNx3 8 bit numpy array as a png image

        :param img: N.N.3 numpy array
        :param path: path to save image to, e.g. './img/img.png
        :return:
        """
        if len(img.shape) != 3 or img.dtype is not np.dtype('uint8'):
            raise TypeError('image must be NxNx3 array')
        with open(str(path), 'wb') as f:
            writer = png.Writer(img.shape[1], img.shape[0], greyscale=False, bitdepth=8)
            writer.write(f, np.reshape(img, (-1, img.shape[1] * img.shape[2])))
