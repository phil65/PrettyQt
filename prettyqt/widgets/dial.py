from __future__ import annotations

from prettyqt import core, widgets


class Dial(widgets.AbstractSliderMixin, widgets.QDial):
    value_changed = core.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.on_value_change)


if __name__ == "__main__":
    app = widgets.app()
    slider = Dial()
    slider.setRange(0, 100)
    slider.show()
    app.exec()
