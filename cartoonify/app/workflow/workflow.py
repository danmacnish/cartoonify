from __future__ import division
import png
import numpy as np
from pathlib import Path
import logging
from app.sketch import SketchGizeh
from app.gpio import Gpio


class Workflow(object):
    """controls execution of app
    """

    def __init__(self, dataset, imageprocessor, camera):
        self._path = Path('')
        self._image_path = Path('')
        self._dataset = dataset
        self._image_processor = imageprocessor
        self._sketcher = None
        self._gpio = Gpio()
        self._cam = camera
        self._logger = logging.getLogger(self.__class__.__name__)
        self._image = None
        self._annotated_image = None
        self._image_labels = []
        self._count = 0

    def setup(self, setup_gpio=True):
        print('loading cartoon dataset...')
        self._dataset.setup()
        print('Done')
        self._sketcher = SketchGizeh()
        self._sketcher.setup()
        print('loading tensorflow model...')
        self._image_processor.setup()
        print('Done')
        if setup_gpio:
            self._gpio.setup(capture_callback=self.run)
        self._path = Path(__file__).parent / '..' / '..' / 'images'
        if not self._path.exists():
            self._path.mkdir()
        self._count = len(list(self._path.glob('image*.png')))
        if self._cam is not None:
            self._cam.resolution = (640, 480)

    def run(self):
        """capture an image, process it, and save to file

        :return:
        """
        self._logger.info('capturing and processing image.')
        self._gpio.status_pin(True)
        self._count += 1
        path = self._path / ('image' + str(self._count) + '.jpg')
        self.capture(path)
        self.process(path)
        annotated, cartoon = self.save_results()
        self._gpio.status_pin(False)

    def capture(self, path):
        if self._cam is not None:
            self._cam.capture(str(path))
        else:
            raise AttributeError("app wasn't started with --camera flag, so you can't use the camera to capture images.")
        return path

    def process(self, image_path, threshold=0.3):
        """processes an image. If no path supplied, then capture from camera

        :param float threshold: threshold for object detection (0.0 to 1.0)
        :param path: directory to save results to
        :param bool camera_enabled: whether to use raspi camera or not
        :param image_path: image to process, if camera is disabled
        :return:
        """
        print('processing image...')
        try:
            self._image_path = Path(image_path)
            img = self._image_processor.load_image_into_numpy_array(image_path)
            # load a scaled version of the image into memory
            img_scaled = self._image_processor.load_image_into_numpy_array(image_path, scale=300 / max(img.shape))
            boxes, scores, classes, num = self._image_processor.detect(img_scaled)
            # annotate the original image
            self._annotated_image = self._image_processor.annotate_image(img, boxes, classes, scores, threshold=threshold)
            self._sketcher = SketchGizeh()
            self._sketcher.setup()
            self._image_labels = self._sketcher.draw_object_recognition_results(np.squeeze(boxes),
                                   np.squeeze(classes).astype(np.int32),
                                   np.squeeze(scores),
                                   self._image_processor.labels,
                                   self._dataset,
                                   threshold=threshold)
        except ValueError as e:
            print(repr(e))
            self._logger.exception(e)

    def save_results(self):
        """save result images as png and list of detected objects as txt

        :return tuple: (path to annotated image, path to cartoon image)
        """
        annotated_path = self._image_path
        cartoon_path = self._image_path.with_name('cartoon' + str(self._count) + '.png')
        labels_path = self._image_path.with_name('labels' + str(self._count) + '.txt')
        with open(labels_path, 'w') as f:
            f.writelines(self.image_labels)
        # self._save_3d_numpy_array_as_png(self._annotated_image, annotated_path)
        self._sketcher.save_png(cartoon_path)
        return annotated_path, cartoon_path

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

    def close(self):
        self._image_processor.close()
        self._gpio.close()

    @property
    def image_labels(self):
        return self._image_labels
