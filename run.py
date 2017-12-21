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
import importlib
import sys

root = Path(__file__).parent

# init objects
dataset = DrawingDataset(str(root / 'downloads/drawing_dataset'), str(root / 'app/label_mapping.jsonl'))
imageprocessor = ImageProcessor(str(root / 'downloads/detection_models/ssd_mobilenet_v1_coco_2017_11_17/frozen_inference_graph.pb'),
                                str(root / 'app' / 'object_detection' / 'data' / 'mscoco_label_map.pbtxt'))
sketch = SketchGizeh()

# configure logging
logging_filename = datetime.datetime.now().strftime('%Y%m%d-%H%M.log')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename=str(Path(__file__).parent / 'logs' / logging_filename))


@click.command()
@click.option('--path', default=None, type=click.Path(), help='directory to save results to')
@click.option('--camera', is_flag=True, help='use this flag to enable captures from the raspberry pi camera')
@click.option('--gui', is_flag=True, help='enables gui')
def run(path, camera, gui):

    try:
        if camera:
            picam = importlib.import_module('picamera')
            cam = picam.PiCamera()
        else:
            cam = None
    except ImportError as e:
        print('picamera module missing, please install using:\nsudo apt-get update \n'
              'sudo apt-get install python-picamera')
        logging.exception(e)
    if gui:
        print('starting gui...')
        start(WebGui, address='0.0.0.0', start_browser=True)
    else:
        while True:
            app = Workflow(dataset, imageprocessor, sketch, cam)
            app.setup()
            path = Path(input("enter the filepath of the image to process:"))
            app.process(str(path))
            app.save_results()
            if not click.confirm('do you want to process another image?'):
                break

if __name__=='__main__':
    run()
    sys.exit()
