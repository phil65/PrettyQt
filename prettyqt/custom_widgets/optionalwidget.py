from __future__ import annotations

from prettyqt import core, widgets


class OptionalWidget(widgets.GroupBox):
    """Wraps another widget in a GroupBox with and CheckBock and makes it optional."""

    value_changed = core.Signal(object)

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
        self.widget.value_changed.connect(self._on_value_change)
        self.toggled.connect(self._on_enable_change)

    def _on_value_change(self, val):
        self.value_changed.emit(val)

    def _on_enable_change(self, val):
        self.widget.setEnabled(val)
        if val:
            self.value_changed.emit(self.widget.get_value())
        else:
            self.value_changed.emit(None)

    def __getattr__(self, value: str):
        return getattr(self.widget, value)

    @classmethod
    def setup_example(cls):
        w = widgets.CheckBox("Example")
        return cls(widget=w)

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
    widget.value_changed.connect(print)
    widget.show()
    app.exec()
