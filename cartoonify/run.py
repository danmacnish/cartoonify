from __future__ import division
import click
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor, tensorflow_model_name, model_path
from app.sketch import SketchGizeh
from pathlib import Path
from os.path import join
import logging
import datetime
from app.gui import WebGui
from remi import start
import importlib
import sys
import time


root = Path(__file__).parent

# init objects
dataset = DrawingDataset(str(root / 'downloads/drawing_dataset'), str(root / 'app/label_mapping.jsonl'))
imageprocessor = ImageProcessor(str(model_path),
                                str(root / 'app' / 'object_detection' / 'data' / 'mscoco_label_map.pbtxt'),
                                tensorflow_model_name)

# configure logging
logging_filename = datetime.datetime.now().strftime('%Y%m%d-%H%M.log')
logging_path = Path(__file__).parent / 'logs'
if not logging_path.exists():
    logging_path.mkdir()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename=str(Path(__file__).parent / 'logs' / logging_filename))


@click.command()
@click.option('--camera', is_flag=True, help='use this flag to enable captures from the raspberry pi camera')
@click.option('--gui', is_flag=True, help='enables gui')
@click.option('--raspi-headless', is_flag=True, help='run on raspi with camera and GPIO but without gui')
@click.option('--batch-process', is_flag=True, help='process all jpg images in a directory')
@click.option('--raspi-gpio', is_flag=True, help='use gpio to trigger capture & process')
def run(camera, gui, raspi_headless, batch_process, raspi_gpio):
    if gui:
        print('starting gui...')
        start(WebGui, address='0.0.0.0', websocket_port=8082, port=8081, host_name='raspberrypi.local', start_browser=False)
    else:
        try:
            if camera or raspi_headless:
                picam = importlib.import_module('picamera')
                cam = picam.PiCamera()
                cam.rotation=90
            else:
                cam = None
            app = Workflow(dataset, imageprocessor, cam)
            app.setup(setup_gpio=raspi_gpio)
        except ImportError as e:
            print('picamera module missing, please install using:\n     sudo apt-get update \n'
                  '     sudo apt-get install python-picamera')
            logging.exception(e)
            sys.exit()
        while True:
            if raspi_headless
                while True:
                    # gpio is configured with a callback on capture pin, so we enter infinite loop
                    pass
            if camera:
                if click.confirm('would you like to capture an image?'):
                    path = root / 'images' / 'image.jpg'
                    if not path.parent.exists():
                        path.parent.mkdir()
                    app.capture(str(path))
                else:
                    app.close()
                    break
            if batch_process:
                path = Path(input("enter the path to the directory to process:"))
                for file in path.glob('*.jpg'):
                    print('processing {}'.format(str(file)))
                    app.process(str(file), top_x=4)
                    app.save_results()
                    app.count += 1
                print('finished processing files, closing app.')
                app.close()
                sys.exit()
            else:
                path = Path(input("enter the filepath of the image to process:"))
            if str(path) != '.' or 'exit':
                app.process(str(path), top_x=4)
                app.save_results()
            else:
                app.close()
                sys.exit()

if __name__=='__main__':
    run()
    sys.exit()
