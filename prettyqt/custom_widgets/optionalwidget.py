from typing import Optional

from qtpy import QtWidgets

from prettyqt import widgets


class OptionalWidget(widgets.GroupBox):
    def __init__(
        self,
        widget: QtWidgets.QWidget,
        title: str = "",
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(checkable=True, title=title)
        self.set_layout("vertical")
        self.box.add(widget)
        self.widget = widget
        self.toggled.connect(self.widget.setEnabled)

    def __getattr__(self, value: str):
        return self.widget.__getattribute__(value)

    @property
    def enabled(self) -> bool:
        return self.isChecked()

    @enabled.setter
    def enabled(self, state: bool):
        self.setChecked(state)

    def get_value(self):
        if self.isChecked():
            return self.widget.get_value()
        return None


if __name__ == "__main__":
    app = widgets.app()
    img = widgets.RadioButton("test")
    widget = OptionalWidget(img, "Test")
    widget.show()
    app.main_loop()
    print(widget.enabled)
