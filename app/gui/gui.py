import remi.gui as gui
from remi import start, App
import sys
import PIL.Image
import io
import time
from pathlib import Path
from app.workflow import Workflow
from app.drawing_dataset import DrawingDataset
from app.image_processor import ImageProcessor
from app.sketch import SketchGizeh


class PILImageViewerWidget(gui.Image):
    def __init__(self, **kwargs):
        super().__init__('/res/logo.png', **kwargs)
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
    def __init__(self, *args):
        super().__init__(*args)

    def idle(self):
        # idle function called every update cycle
        pass

    def main(self):
        root = Path(__file__).parent / '..' / '..'
        dataset = DrawingDataset(str(root / 'downloads/drawing_dataset'), str(root / 'app/label_mapping.jsonl'))
        imageprocessor = ImageProcessor(
            str(root / 'downloads/detection_models/ssd_mobilenet_v1_coco_2017_11_17/frozen_inference_graph.pb'),
            str(root / 'app' / 'object_detection' / 'data' / 'mscoco_label_map.pbtxt'))
        cam = None
        self.app = Workflow(dataset, imageprocessor, cam)
        self.app.setup()
        return self.construct_ui()

    def construct_ui(self):
        main_container = gui.VBox()
        main_container.style['top'] = "0px"
        main_container.style['display'] = "flex"
        main_container.style['overflow'] = "auto"
        main_container.style['width'] = "100%"
        main_container.style['flex-direction'] = "column"
        main_container.style['position'] = "absolute"
        main_container.style['justify-content'] = "space-around"
        main_container.style['margin'] = "0px"
        main_container.style['align-items'] = "center"
        main_container.style['left'] = "0px"
        main_container.style['height'] = "100%"
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
        main_container.append(hbox_snap, 'hbox_snap')
        width = 200
        height = 200
        self.image_original = PILImageViewerWidget(width=width, height=height)
        main_container.append(self.image_original, 'image_original')
        self.image_result = PILImageViewerWidget(width=width, height=height)
        main_container.append(self.image_result, 'image_result')
        self.image_tagged = PILImageViewerWidget(width=width, height=height)
        main_container.append(self.image_tagged, 'image_tagged')

        button_close.set_on_click_listener(self.on_close_pressed)
        button_snap.set_on_click_listener(self.on_snap_pressed)

        return main_container

    def on_close_pressed(self, *_):
        self.close()  #closes the application

    def on_snap_pressed(self, *_):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select an image file', False, '.')
        self.fileselectionDialog.set_on_confirm_value_listener(
            self.on_image_file_selected)
        self.fileselectionDialog.set_on_cancel_dialog_listener(
            self.on_dialog_cancel)
        # here is shown the dialog as root widget
        self.fileselectionDialog.show(self)

    def on_image_file_selected(self, widget, file_list):
        if len(file_list) < 1:
            return
        self.app.process(file_list[0])
        annotated, cartoon = self.app.save_results()
        self.image_original.load(file_list[0])
        self.image_tagged.load(str(annotated))
        self.image_result.load(str(cartoon))
        self.set_root_widget(self.mainContainer)

    def on_dialog_cancel(self, widget):
        self.set_root_widget(self.mainContainer)