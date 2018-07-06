import numpy as np
import os
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
from PIL import Image
from app.object_detection import label_map_util
# from app.object_detection import visualization_utils as vis_util
import logging
from pathlib import Path
import click


root = Path(__file__).parent
tensorflow_model_name = 'ssd_mobilenet_v1_coco_2017_11_17'
model_path = root / '..' / '..' / 'downloads' / 'detection_models' / tensorflow_model_name / 'frozen_inference_graph.pb'

class ImageProcessor(object):
    """performs object detection on an image
    """

    def __init__(self, path_to_model, path_to_labels, model_name):
        self._model_name = model_name
        # Path to frozen detection graph. This is the actual model that is used for the object detection.
        self._path_to_model = path_to_model
        # strings used to add correct label for each box.
        self._path_to_labels = path_to_labels
        self._download_url = 'http://download.tensorflow.org/models/object_detection/'
        self._num_classes = 90
        self._detection_graph = None
        self._labels = dict()
        self._image = None
        self._boxes = None
        self._classes = None
        self._scores = None
        self._num = None
        self._logger = None
        self._session = None
        self.image_tensor = None
        self.detection_boxes = None
        self.detection_scores = None
        self.detection_classes = None
        self.num_detections = None

    def setup(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        if not Path(self._path_to_model).exists():
            if click.confirm('no object detection model available, would you like to download the model? '
                             'download will take approx 100mb of space'):
                self.download_model(self._download_url, self._model_name + '.tar.gz')
        self.load_model(self._path_to_model)
        self._labels = self.load_labels(self._path_to_labels)
        # run a detection once, because first model run is always slow
        self.detect(np.ones((150, 150, 3), dtype=np.uint8))

    def download_model(self, url, filename):
        """download a model file from the url and unzip it
        """
        self._logger.info('downloading model: {}'.format(filename))
        opener = urllib.request.URLopener()
        opener.retrieve(url + filename, filename)
        tar_file = tarfile.open(filename)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(file, path=str(Path(self._path_to_model).parents[1]))

    def load_model(self, path):
        """load saved model from protobuf file
        """
        if not Path(path).exists():
            raise IOError('model file missing: {}'.format(str(path)))
        with tf.gfile.GFile(path, 'rb') as fid:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(fid.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name='')
        self._detection_graph = graph
        self._session = tf.Session(graph=self._detection_graph)
        # Definite input and output Tensors for detection_graph
        self.image_tensor = self._detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self._detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self._detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self._detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self._detection_graph.get_tensor_by_name('num_detections:0')

    def load_labels(self, path):
        """load labels from .pb file, and map to a dict with integers, e.g. 1=aeroplane
        """
        label_map = label_map_util.load_labelmap(path)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self._num_classes,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        return category_index

    def load_image_into_numpy_array(self, path, scale=1.0):
        """load image into NxNx3 numpy array
        """
        image = Image.open(path)
        image = image.resize(tuple(int(scale * dim) for dim in image.size))
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

    def detect(self, image):
        """detect objects in the image
        """
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        (self._boxes, self._scores, self._classes, num) = self._session.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        return self._boxes, self._scores, self._classes, self._num

    def annotate_image(self, image, boxes, classes, scores, threshold=0.5):
        """draws boxes around the detected objects and labels them

        :return: annotated image
        """
        annotated_image = image.copy()
        # vis_util.visualize_boxes_and_labels_on_image_array(
        #     annotated_image,
        #     np.squeeze(boxes),
        #     np.squeeze(classes).astype(np.int32),
        #     np.squeeze(scores),
        #     self._labels,
        #     use_normalized_coordinates=True,
        #     line_thickness=8,
        #     min_score_thresh=threshold)
        return annotated_image

    @property
    def labels(self):
        return self._labels

    def close(self):
        self._session.close()
