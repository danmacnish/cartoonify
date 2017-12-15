import click
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor
from app.sketch import SketchGizeh
from pathlib import Path
from os.path import join
import logging
import datetime
from app.gui import WebGui
from remi import start


dataset = DrawingDataset('./downloads/drawing_dataset', './app/label_mapping.jsonl')
imageprocessor = ImageProcessor(join('.', 'downloads', 'detection_models', 'ssd_mobilenet_v1_coco_2017_11_17',
                                          'frozen_inference_graph.pb'),
                                join('.', 'app', 'object_detection', 'data', 'mscoco_label_map.pbtxt'))
sketch = SketchGizeh()


@click.command()
@click.option('--path', default=None, type=click.Path(), help='directory to save results to')
@click.option('--camera', is_flag=True, help='use this flag to enable captures from the raspberry pi camera')
@click.option('--gui', is_flag=True, help='enables gui')
@click.option('--image', default=None, type=click.Path(), help='filepath of the image to process (use this if not enabling camera)')
def run(path, camera, gui, image):
    logging_filename = datetime.datetime.now().strftime('%Y%m%d-%H%M.log')
    if image is not None:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename=str(Path(image).parent / logging_filename))
    elif path is not None and image is None:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename=str(Path(path) / logging_filename))
    if gui:
        start(WebGui)
    #app = Workflow(dataset, imageprocessor, sketch)
    #app.setup()
    #app.run(path, camera, image)

if __name__=='__main__':
    run()
