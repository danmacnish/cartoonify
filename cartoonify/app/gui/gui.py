import remi.gui as gui
from remi import App
import PIL.Image
import io
import time
from pathlib import Path
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor, tensorflow_model_name, model_path
import importlib
import logging
import sys


class PILImageViewerWidget(gui.Image):
    def __init__(self, **kwargs):
        super(PILImageViewerWidget, self).__init__('/res/logo.png', **kwargs)
        self._buf = None

    def load(self, file_path_name):
        pil_image = PIL.Image.open(file_path_name)
        self._buf = io.BytesIO()
        pil_image.save(self._buf, format='png')
        self.refresh()

    def refresh(self):
        i = int(time.time() * 1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self), i)

    def get_image_data(self, update_index):
        if self._buf is None:
            return None
        self._buf.seek(0)
        headers = {'Content-type': 'image/png'}
        return [self._buf.read(), headers]


class WebGui(App):
    """
    gui for the app
    """

    def __init__(self, *args):
        super(WebGui, self).__init__(*args)

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
            root = Path(__file__).parent / '..' / '..'
            self._dataset = DrawingDataset(str(root / 'downloads/drawing_dataset'), str(root / 'app/label_mapping.jsonl'))
            self._imageprocessor = ImageProcessor(
                str(model_path),
                str(root / 'app' / 'object_detection' / 'data' / 'mscoco_label_map.pbtxt'),
                tensorflow_model_name)
            self.app = Workflow(self._dataset, self._imageprocessor, self._cam)
            self.app.setup()
            self.setup_gpio()
            return self.construct_ui()

    def setup_gpio(self):
        try:
            pin = 4
            gpio = importlib.import_module('RPi.GPIO')
            gpio.setmode(gpio.BCM)
            gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_UP)
            gpio.add_event_detect(pin, gpio.FALLING, callback=self.on_snap_pressed, bouncetime=200)
        except ImportError as e:
            self._logger.exception(e)
            print('raspi gpio module not found, continuing...')

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
        hbox_snap.style['width'] = "70%"
        hbox_snap.style['flex-direction'] = "row"
        hbox_snap.style['position'] = "static"
        hbox_snap.style['justify-content'] = "space-around"
        hbox_snap.style['-webkit-order'] = "4348867584"
        hbox_snap.style['margin'] = "0px"
        hbox_snap.style['align-items'] = "center"
        hbox_snap.style['top'] = "125px"
        hbox_snap.style['height'] = "150px"
        button_snap = gui.Button('snap')
        button_snap.style['margin'] = "0px"
        button_snap.style['overflow'] = "auto"
        button_snap.style['width'] = "200px"
        button_snap.style['height'] = "30px"
        hbox_snap.append(button_snap, 'button_snap')
        button_open = gui.Button('open image from file')
        button_open.style['margin'] = "0px"
        button_open.style['overflow'] = "auto"
        button_open.style['width'] = "200px"
        button_open.style['height'] = "30px"
        hbox_snap.append(button_open, 'button_open')
        vbox_settings = gui.VBox()
        vbox_settings.style['order'] = "4349486136"
        vbox_settings.style['display'] = "flex"
        vbox_settings.style['overflow'] = "auto"
        vbox_settings.style['width'] = "250px"
        vbox_settings.style['flex-direction'] = "column"
        vbox_settings.style['position'] = "static"
        vbox_settings.style['justify-content'] = "space-around"
        vbox_settings.style['-webkit-order'] = "4349486136"
        vbox_settings.style['margin'] = "0px"
        vbox_settings.style['align-items'] = "center"
        vbox_settings.style['top'] = "149.734375px"
        vbox_settings.style['height'] = "80px"
        checkbox_display_original = gui.CheckBoxLabel(' Display original image', False, '')
        checkbox_display_original.style['order'] = "4348263224"
        checkbox_display_original.style['-webkit-order'] = "4348263224"
        checkbox_display_original.style['display'] = "block"
        checkbox_display_original.style['margin'] = "0px"
        checkbox_display_original.style['align-items'] = "center"
        checkbox_display_original.style['overflow'] = "auto"
        checkbox_display_original.style['width'] = "200px"
        checkbox_display_original.style['top'] = "135.734375px"
        checkbox_display_original.style['position'] = "static"
        checkbox_display_original.style['height'] = "30px"
        vbox_settings.append(checkbox_display_original, 'checkbox_display_original')
        checkbox_display_tagged = gui.CheckBoxLabel(' Display tagged image', False, '')
        checkbox_display_tagged.style['order'] = "4355939912"
        checkbox_display_tagged.style['-webkit-order'] = "4355939912"
        checkbox_display_tagged.style['display'] = "block"
        checkbox_display_tagged.style['margin'] = "0px"
        checkbox_display_tagged.style['overflow'] = "auto"
        checkbox_display_tagged.style['width'] = "200px"
        checkbox_display_tagged.style['top'] = "135px"
        checkbox_display_tagged.style['position'] = "static"
        checkbox_display_tagged.style['height'] = "30px"
        vbox_settings.append(checkbox_display_tagged, 'checkbox_display_tagged')
        hbox_snap.append(vbox_settings, 'vbox_settings')
        button_close = gui.Button('close')
        button_close.style['background-color'] = 'red'
        button_close.style['width'] = "200px"
        button_close.style['height'] = '30px'
        hbox_snap.append(button_close, 'button_close')
        self.main_container.append(hbox_snap, 'hbox_snap')
        width = 200
        height = 200
        self.image_original = PILImageViewerWidget(width=width, height=height)
        self.main_container.append(self.image_original, 'image_original')
        self.image_result = PILImageViewerWidget(width=width, height=height)
        self.main_container.append(self.image_result, 'image_result')
        self.image_label = gui.Label('', width=400, height=30, margin='10px')
        self.image_label.style['align-items'] = "center"
        self.main_container.append(self.image_label, 'image_label')

        button_close.set_on_click_listener(self.on_close_pressed)
        button_snap.set_on_click_listener(self.on_snap_pressed)
        button_open.set_on_click_listener(self.on_open_pressed)

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