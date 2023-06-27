from __future__ import annotations

from prettyqt import widgets


class OptionalWidget(widgets.GroupBox):
    def __init__(
        self,
        widget: widgets.QWidget,
        title: str = "",
        parent: widgets.QWidget | None = None,
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
        return self.widget.get_value() if self.isChecked() else None


if __name__ == "__main__":
    app = widgets.app()
    img = widgets.RadioButton("test")
    widget = OptionalWidget(img, "Test")
    widget.show()
    app.exec()
