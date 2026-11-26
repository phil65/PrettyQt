from typing import TypeVar, cast

from prettyqt import core, widgets
from prettyqt.utils import listdelegators


T = TypeVar("T", bound=widgets.QWidget, default=widgets.QWidget)


class ScrollArea(widgets.AbstractScrollAreaMixin, widgets.QScrollArea):
    """Scrolling view onto another widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        viewport = widgets.Widget(self, object_name=f"{type(self).__name__}_viewport")
        self.setViewport(viewport)

    def __add__(self, other: widgets.QWidget | widgets.QLayout | list):
        self.add(other)
        return self

    def get_visible_widgets(
        self,
        typ: type[T] = widgets.QWidget,  # ty: ignore[invalid-parameter-default]
        partial_allowed: bool = True,
        margin: int = 10,
        recursive: bool = True,
    ) -> listdelegators.ListDelegator[T]:
        """Return all widgets which are visible in the viewport.

        Results can be filtered by type and whether widget is fully or partially visible.
        A positive margin increases the area to search for widgets, a negative margin
        decreases it.
        """
        if (widget := self.widget()) is None:
            return listdelegators.ListDelegator([])
        widget = cast("widgets.Widget", widget)  # set via prettyqt
        viewport = self.viewport()
        rect = viewport.rect().adjusted(-margin, -margin, margin, margin)
        found = []
        for w in widget.find_children(typ, recursive=recursive):
            top_left = w.mapTo(viewport, w.rect().topLeft())
            bottom_right = w.mapTo(viewport, w.rect().bottomRight())
            mapped = core.Rect(top_left, bottom_right)
            if (partial_allowed and rect.intersects(mapped)) or (
                not partial_allowed and rect.contains(mapped)
            ):
                found.append(w)
        return listdelegators.ListDelegator(found)

    def _get_layout(self) -> widgets.LayoutMixin:
        """Layout of the scrolled widget (set_layout() installs prettyqt layouts)."""
        if (widget := self.widget()) is None or (layout := widget.layout()) is None:
            msg = "ScrollArea has no widget with a layout"
            raise RuntimeError(msg)
        return cast("widgets.LayoutMixin", layout)

    def get_children(
        self,
    ) -> listdelegators.ListDelegator[widgets.QWidget | widgets.QLayout]:
        return self._get_layout().get_children()

    def set_widget(self, widget: widgets.QWidget):
        self.setWidget(widget)

    def add_widget(self, *args, **kwargs):
        self._get_layout().addWidget(*args, **kwargs)

    def add_layout(self, *args, **kwargs):
        layout = self._get_layout()
        if not isinstance(layout, widgets.QBoxLayout | widgets.QGridLayout):
            raise TypeError(layout)
        layout.addLayout(*args, **kwargs)

    def add(
        self,
        item: widgets.QWidget | widgets.QLayout | list,
        stretch: int | None = None,
    ):
        match item:
            case widgets.QWidget():
                self.add_widget(item)
            case widgets.QLayout():
                widget = widgets.Widget(self)
                widget.set_layout(item)
                self.add_widget(widget)
            case list():
                for i in item:
                    self.add(i, stretch)
                return item
        layout = self._get_layout()
        if stretch and isinstance(layout, widgets.QBoxLayout):
            layout.setStretch(layout.count() - 1, stretch)
        return item


if __name__ == "__main__":
    app = widgets.app()
    area = ScrollArea()
    widget = widgets.Widget()
    widget.set_layout("vertical")
    area.set_widget(widget)
    for i in range(50):
        w = widgets.RadioButton(str(i))
        area.setWidgetResizable(True)
        area.add_widget(w)
        area.ensureWidgetVisible(w)
    area.show()
    a = area.v_scrollbar.fx["value"].animate(0, 300, reverse=True, single_shot=False)
    app.sleep(2)
    a.stop()
    app.exec()
