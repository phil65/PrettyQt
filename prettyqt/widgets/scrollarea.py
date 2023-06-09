from __future__ import annotations

from typing import TypeVar

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets

T = TypeVar("T", bound=QtWidgets.QWidget)


class ScrollArea(widgets.AbstractScrollAreaMixin, QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        viewport = widgets.Widget(self, object_name=f"{type(self).__name__}_viewport")
        self.setViewport(viewport)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout | list):
        self.add(other)
        return self

    def get_visible_widgets(
        self,
        typ: type[T] = QtWidgets.QWidget,
        partial_allowed: bool = True,
        margin: int = 10,
        recursive: bool = True,
    ) -> list[T]:
        widget = self.widget()
        viewport = self.viewport()
        rect = viewport.rect().adjusted(-margin, -margin, margin, margin)
        found = []
        for w in widget.find_children(typ, recursive=recursive):
            top_left = w.mapTo(viewport, w.rect().topLeft())
            bottom_right = w.mapTo(viewport, w.rect().bottomRight())
            mapped = core.Rect(top_left, bottom_right)
            if partial_allowed and rect.intersects(mapped):
                found.append(w)
            elif not partial_allowed and rect.contains(mapped):
                found.append(w)
        return found

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
