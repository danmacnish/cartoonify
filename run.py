import click
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor
from app.sketch import SketchGizeh
from pathlib import Path
from os.path import join

dataset = DrawingDataset('./downloads/drawing_dataset', './app/label_mapping.jsonl')
imageprocessor = ImageProcessor(join('.', 'downloads', 'detection_models', 'ssd_mobilenet_v1_coco_2017_11_17',
                                          'frozen_inference_graph.pb'),
                                join('.', 'app', 'object_detection', 'data', 'mscoco_label_map.pbtxt'))
sketch = SketchGizeh()


@click.command()
@click.option('--path', default=None, help='filepath of the image to process.')
def run(path):
    app = Workflow(dataset, imageprocessor, sketch)
    app.run(path)

if __name__=='__main__':
    run()
