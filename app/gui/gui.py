import remi.gui as gui
from remi import App
from app.workflow import Workflow


class WebGui(App):

    def __init__(self, *args):
        super().__init__(*args)

    def main(self):
        container = gui.VBox(width=200, height=200)
        self.lbl = gui.Label('Hello world!')
        self.bt = gui.Button('Press me!')

        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self.on_button_pressed)

        # appending a widget to another, the first argument is a string key
        container.append(self.lbl)
        container.append(self.bt)

        # returning the root widget
        return container

    # listener function
    def on_button_pressed(self, widget):
        self.lbl.set_text('Button pressed!')
        self.bt.set_text('Hi!')
