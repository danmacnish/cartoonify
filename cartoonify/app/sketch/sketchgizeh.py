import numpy as np
import sys
import gizeh as gz
import random


class SketchGizeh(object):

    def __init__(self):
        self._surface = None

    def setup(self, width=1200, height=900, bg_color=(1, 1, 1)):
        self._width = width
        self._height = height
        self._surface = gz.Surface(width=width, height=height, bg_color=bg_color)

    def draw(self, strokes, scale=1.0, pos=[0, 0], stroke_width=6, color=[0, 0, 0]):
        """iterate through a list of strokes, drawing them on the canvas
        pos is normalised coprdinates in range (0,1)
        """
        try:
            for val in pos:
                if val < 0 or val > 1 or not isinstance(val, float):
                    raise ValueError('position coordinates should be float between (0,1)')
            scale *= np.mean([self._width, self._height]) / 255
            pos[0] = pos[0] * self._width - (scale * (255 / 2))
            pos[1] = pos[1] * self._height - (scale * (255 / 2))
            lines = self._convert_quickdraw_strokes_to_gizeh_group(strokes, color, stroke_width=stroke_width / scale)
            lines = lines.scale(scale).translate(xy=pos)
            lines.draw(self._surface)
        except ValueError as e:
            print(repr(e))

    def draw_person(self, dataset, scale=1.0, position=[0, 0], stroke_width=6):
        body_parts = {'face': [0, 0], 't-shirt': [0, 250], 'pants': [0, 480]}  # dict of parts + translation
        gz_body_parts = []
        for name, pos in body_parts.items():
            strokes = dataset.get_drawing(name, random.randint(1, 1000))
            strokes_gz = self._convert_quickdraw_strokes_to_gizeh_group(strokes, stroke_width=stroke_width / scale)
            strokes_gz = strokes_gz.translate(pos)
            gz_body_parts.append(strokes_gz)
        scale *= np.mean([self._width, self._height]) / 750
        pos[0] = position[0] * self._width - (scale * (255 / 2))
        pos[1] = position[1] * self._height - (scale * (750 / 2))
        gz_body_parts = gz.Group(gz_body_parts).scale(scale).translate(xy=pos)
        gz_body_parts.draw(self._surface)

    def _convert_quickdraw_strokes_to_gizeh_group(self, strokes, color=[0, 0, 0], stroke_width=5):
        lines_list = []
        for stroke in strokes:
            x, y = stroke
            points = list(zip(x, y))
            line = gz.polyline(points=points, stroke=color, stroke_width=stroke_width)
            lines_list.append(line)
        return gz.Group(lines_list)

    def draw_object_recognition_results(self, boxes, classes, scores, labels, dataset, threshold=0.5):
        """draw results of object recognition

        :return: list of objects drawn to the canvas
        """
        drawn_objects = []  # list of the objects drawn
        for i in range(boxes.shape[0]):
            if scores is None or scores[i] >= threshold:
                box = tuple(boxes[i].tolist())
                if classes[i] in labels.keys():
                    class_name = labels[classes[i]]['name']
                    drawn_objects.append(class_name)
                else:
                    raise ValueError('no label for index {}'.format(i))
                ymin, xmin, ymax, xmax = box
                centre = [np.mean([xmin, xmax]), np.mean([ymin, ymax])]
                size = np.mean([xmax - xmin, ymax - ymin])
                if class_name == 'person':
                    self.draw_person(dataset, scale=ymax - ymin, position=centre)
                else:
                    drawing = dataset.get_drawing(class_name, random.randint(1, 1000))
                    self.draw(drawing, scale=size, pos=centre)
        return drawn_objects

    def get_npimage(self):
        return self._surface.get_npimage()

    def save_png(self, path):
        self._surface.write_to_png(str(path))