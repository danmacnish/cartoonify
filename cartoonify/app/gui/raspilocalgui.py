import remi.gui as gui
from remi import App
from .common import PILImageViewerWidget
from pathlib import Path
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor, tensorflow_model_name, model_path
import importlib
import logging


class RaspiLocalGui(App):
    """
    gui for the app
    """

    def __init__(self, *args):
        super(RaspiLocalGui, self).__init__(*args)
        self._cam = None

    def idle(self):
        # idle function called every update cycle
        pass

    def main(self):
        try:
            picam = importlib.import_module('picamera')
            self._cam = picam.PiCamera()
        except ImportError:
            self._cam = None
            msg = 'picamera module missing, please install using:\n     sudo apt-get update \n' \
                  '     sudo apt-get install python-picamera'
            print(msg)
            logging.info(msg)
        finally:
            print('loading gui...')
            root = Path(__file__).parent / '..' / '..'
            self._dataset = DrawingDataset(str(root / 'downloads/drawing_dataset'), str(root / 'app/label_mapping.jsonl'))
            self._imageprocessor = ImageProcessor(
                str(model_path),
                str(root / 'app' / 'object_detection' / 'data' / 'mscoco_label_map.pbtxt'),
                tensorflow_model_name)
            self.app = Workflow(self._dataset, self._imageprocessor, self._cam)
            self.app.setup()
            return self.construct_ui()

    def construct_ui(self):
        self.main_container = gui.VBox()
        self.main_container.style['top'] = "0px"
        self.main_container.style['display'] = "flex"
        self.main_container.style['overflow'] = "auto"
        self.main_container.style['width'] = "100%"
        self.main_container.style['flex-direction'] = "column"
        self.main_container.style['position'] = "absolute"
        self.main_container.style['justify-content'] = "space-around"
        self.main_container.style['margin'] = "0px"
        self.main_container.style['align-items'] = "center"
        self.main_container.style['left'] = "0px"
        self.main_container.style['height'] = "100%"
        hbox_snap = gui.HBox()
        hbox_snap.style['left'] = "0px"
        hbox_snap.style['order'] = "4348867584"
        hbox_snap.style['display'] = "flex"
        hbox_snap.style['overflow'] = "auto"
        hbox_snap.style['width'] = "90%"
        hbox_snap.style['flex-direction'] = "row"
        hbox_snap.style['position'] = "static"
        hbox_snap.style['justify-content'] = "space-around"
        hbox_snap.style['-webkit-order'] = "4348867584"
        hbox_snap.style['margin'] = "0px"
        hbox_snap.style['align-items'] = "center"
        hbox_snap.style['top'] = "2%"
        hbox_snap.style['height'] = "15%"
        button_snap = gui.Button('snap')
        button_snap.style['margin'] = "0px"
        button_snap.style['overflow'] = "auto"
        button_snap.style['width'] = "30%"
        button_snap.style['height'] = "15%"
        hbox_snap.append(button_snap, 'button_snap')
        button_close = gui.Button('close')
        button_close.style['background-color'] = 'red'
        button_close.style['width'] = "30%"
        button_close.style['height'] = '15%'
        hbox_snap.append(button_close, 'button_close')
        self.main_container.append(hbox_snap, 'hbox_snap')
        width = 320
        height = 240
        self.image_result = PILImageViewerWidget(width=width, height=height)
        self.main_container.append(self.image_result, 'image_result')
        self.image_label = gui.Label('', width=320, height=30, margin='5px')
        self.image_label.style['align-items'] = "center"
        self.main_container.append(self.image_label, 'image_label')

        button_close.set_on_click_listener(self.on_close_pressed)
        button_snap.set_on_click_listener(self.on_snap_pressed)

        return self.main_container

    def on_close_pressed(self, *_):
        self.app.close()
        self.close()  #closes the application
        # sys.exit()

    def on_snap_pressed(self, *_):
        path = Path(__file__).parent / '..' / '..' / 'images' / 'image.jpg'
        if not path.parent.exists():
            path.parent.mkdir()
        self.app.capture(str(path))
        self.process_image(None, [path])

    def on_open_pressed(self, *_):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select an image file', False, '.')
        self.fileselectionDialog.set_on_confirm_value_listener(
            self.process_image)
        self.fileselectionDialog.set_on_cancel_dialog_listener(
            self.on_dialog_cancel)
        # here is shown the dialog as root widget
        self.fileselectionDialog.show(self)

    def process_image(self, widget, file_list):
        if len(file_list) != 1:
            return
        self.app.process(file_list[0])
        annotated, cartoon = self.app.save_results()
        self.image_original.load(file_list[0])
        self.image_result.load(str(cartoon))
        self.image_label.set_text(', '.join(self.app.image_labels))
        self.set_root_widget(self.main_container)

    def on_dialog_cancel(self, widget):
        self.set_root_widget(self.main_container)