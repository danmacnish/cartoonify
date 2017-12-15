import remi.gui as gui
from remi.gui import *
from remi import start, App


class WebGui(App):
    def __init__(self, *args, **kwargs):
        if not 'editing_mode' in kwargs.keys():
            super().__init__(*args)

    def idle(self):
        # idle function called every update cycle
        pass

    def main(self):
        return self.construct_ui(self)

    @staticmethod
    def construct_ui(self):
        vbox = VBox()
        vbox.attributes['editor_newclass'] = "False"
        vbox.attributes['editor_varname'] = "vbox"
        vbox.attributes['class'] = "VBox"
        vbox.attributes['editor_tag_type'] = "widget"
        vbox.attributes['editor_baseclass'] = "VBox"
        vbox.attributes['editor_constructor'] = "()"
        vbox.style['top'] = "0px"
        vbox.style['display'] = "flex"
        vbox.style['overflow'] = "auto"
        vbox.style['width'] = "100%"
        vbox.style['flex-direction'] = "column"
        vbox.style['position'] = "absolute"
        vbox.style['justify-content'] = "space-around"
        vbox.style['margin'] = "0px"
        vbox.style['align-items'] = "center"
        vbox.style['left'] = "0px"
        vbox.style['height'] = "100%"
        hbox_snap = HBox()
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
        button_snap = Button('button_snap')
        button_snap.style['order'] = "4354708536"
        button_snap.style['-webkit-order'] = "4354708536"
        button_snap.style['display'] = "block"
        button_snap.style['margin'] = "0px"
        button_snap.style['overflow'] = "auto"
        button_snap.style['width'] = "200px"
        button_snap.style['height'] = '100px'
        button_snap.style['top'] = "-590px"
        button_snap.style['position'] = "static"
        button_snap.style['height'] = "30px"
        hbox_snap.append(button_snap, 'button_snap')
        vbox_settings = VBox()
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
        checkbox_display_original = CheckBoxLabel(' Display original image', False, '')
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
        checkbox_display_tagged = CheckBoxLabel(' Display tagged image', False, '')
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
        vbox.append(hbox_snap, 'hbox_snap')
        image_original = Image('original.jpg')
        image_original.style['order'] = "4348343576"
        image_original.style['-webkit-order'] = "4348343576"
        image_original.style['display'] = "block"
        image_original.style['margin'] = "0px"
        image_original.style['overflow'] = "auto"
        image_original.style['width'] = "100px"
        image_original.style['top'] = "816.453125px"
        image_original.style['position'] = "static"
        image_original.style['height'] = "100px"
        vbox.append(image_original, 'image_original')
        image_result = Image('result.jpg')
        image_result.style['order'] = "4350481800"
        image_result.style['-webkit-order'] = "4350481800"
        image_result.style['display'] = "block"
        image_result.style['margin'] = "0px"
        image_result.style['overflow'] = "auto"
        image_result.style['width'] = "100px"
        image_result.style['top'] = "738.453125px"
        image_result.style['position'] = "static"
        image_result.style['height'] = "100px"
        vbox.append(image_result, 'image_result')
        image_tagged = Image('image_tagged.jpg')
        image_tagged.style['order'] = "4358304320"
        image_tagged.style['-webkit-order'] = "4358304320"
        image_tagged.style['display'] = "block"
        image_tagged.style['margin'] = "0px"
        image_tagged.style['overflow'] = "auto"
        image_tagged.style['width'] = "100px"
        image_tagged.style['top'] = "846.453125px"
        image_tagged.style['position'] = "static"
        image_tagged.style['height'] = "100px"
        vbox.append(image_tagged, 'image_tagged')

        self.vbox = vbox
        return self.vbox
