from typing import Callable, Optional

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QPushButton.__bases__ = (widgets.AbstractButton,)


class PushButton(QtWidgets.QPushButton):

    value_changed = core.Signal(bool)

    def __init__(
        self,
        label: Optional[str] = None,
        parent: Optional[QtWidgets.QWidget] = None,
        callback: Optional[Callable] = None,
    ):
        super().__init__(label, parent)
        if callback:
            self.clicked.connect(callback)
        self.toggled.connect(self.value_changed)

    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value: bool):
        self.setChecked(value)

    @property
    def is_on(self) -> bool:
        return self.isChecked()

    @is_on.setter
    def is_on(self, state: bool):
        self.setChecked(state)


if __name__ == "__main__":
    app = widgets.app()
    widget = PushButton("This is a test")
    widget.show()
    app.main_loop()
