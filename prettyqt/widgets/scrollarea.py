from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


class ScrollArea(widgets.AbstractScrollAreaMixin, QtWidgets.QScrollArea):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout | list):
        self.add(other)
        return self

    def get_children(self) -> list[QtWidgets.QWidget]:
        return self.widget().layout().get_children()

    def set_widget(self, widget: QtWidgets.QWidget):
        self.setWidget(widget)

    def add_widget(self, *args, **kwargs):
        self.widget().layout().addWidget(*args, **kwargs)

    def add_layout(self, *args, **kwargs):
        self.widget().layout().addLayout(*args, **kwargs)

    def add(
        self,
        item: QtWidgets.QWidget | QtWidgets.QLayout | list,
        stretch: float | None = None,
    ):
        match item:
            case QtWidgets.QWidget():
                self.add_widget(item)
                if stretch:
                    self.widget().layout().setStretchFactor(self.count() - 1, stretch)
            case QtWidgets.QLayout():
                widget = widgets.Widget(self)
                widget.set_layout(item)
                self.add_widget(widget)
                if stretch:
                    self.setStretchFactor(self.count() - 1, stretch)
            case list():
                for i in item:
                    self.add(i, stretch)
        return item


if __name__ == "__main__":
    app = widgets.app()
    area = ScrollArea()
    for i in range(50):
        w = widgets.RadioButton(str(i))
        area.setWidgetResizable(True)
        area.add_widget(w)
        area.ensureWidgetVisible(w)
    area.show()
    app.main_loop()
