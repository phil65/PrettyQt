from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QRadioButton.__bases__ = (widgets.AbstractButton,)


class RadioButton(QtWidgets.QRadioButton):

    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = RadioButton("This is a test")
    widget.set_icon("mdi.timer")
    widget.show()
    app.main_loop()
