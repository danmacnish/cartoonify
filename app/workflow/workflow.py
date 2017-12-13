from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor
from app.sketch import SketchGizeh
import png
import numpy as np
from pathlib import Path
import importlib
import logging


class Workflow():
    """controls execution of app
    """

    def __init__(self, dataset, imageprocessor, sketch):
        self._dataset = dataset
        self._image_processor = imageprocessor
        self._sketcher = sketch
        self._logger = logging.getLogger(self.__class__.__name__)

    def setup(self):
        print('loading cartoon dataset...')
        self._dataset.setup()
        self._sketcher.setup()
        print('loading tensorflow model...')
        self._image_processor.setup()

    def run(self, path, camera_enabled, image_path):
        """processes an image. If no path supplied, then capture from camera

        :param path: directory to save results to
        :param bool camera_enabled: whether to use raspi camera or not
        :param image_path: image to process, if camera is disabled
        :return:
        """
        print('processing image...')
        try:
            if not camera_enabled:
                if image_path is None:
                    raise ValueError('you must supply a path to the --image flag if --camera is not emabled')
                img = self._image_processor.load_image_into_numpy_array(image_path)
                boxes, scores, classes, num = self._image_processor.detect(img)
                annotated_img = self._image_processor.annotate_image(img, boxes, classes, scores)
                self._sketcher.draw_object_recognition_results(np.squeeze(boxes),
                                       np.squeeze(classes).astype(np.int32),
                                       np.squeeze(scores),
                                       self._image_processor.labels,
                                       self._dataset)
                self._save_3d_numpy_array_as_png(annotated_img, Path(image_path).with_name('annotated.png'))
                self._save_3d_numpy_array_as_png(self._sketcher.get_npimage(), Path(image_path).with_name('cartoon.png'))
            else:
                picamera = importlib.import_module('picamera')
                cam = picamera.PiCamera()
                cam.capture(str(Path(path) / 'image.jpg'))
        except ImportError as e:
            print('picamera module missing, please install using:\nsudo apt-get update \n'
                  'sudo apt-get install python-picamera')
            self._logger.exception(e)
        except ValueError as e:
            print(repr(e))
            self._logger.exception(e)

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
