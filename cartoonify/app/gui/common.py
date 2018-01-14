import remi.gui as gui
import PIL.Image
import io
import time


class PILImageViewerWidget(gui.Image):
    """gui widget that dynamically loads an image
    """
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