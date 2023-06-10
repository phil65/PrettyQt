from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from deprecated import deprecated
from typing_extensions import Self

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


SIZE_CONSTRAINT = bidict(
    default=QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint,
    fixed=QtWidgets.QLayout.SizeConstraint.SetFixedSize,
    minimum=QtWidgets.QLayout.SizeConstraint.SetMinimumSize,
    maximum=QtWidgets.QLayout.SizeConstraint.SetMaximumSize,
    min_and_max=QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize,
    none=QtWidgets.QLayout.SizeConstraint.SetNoConstraint,
)

SizeConstraintStr = Literal[
    "default", "fixed", "minimum", "maximum", "min_and_max", "none"
]

LayoutTypeStr = Literal["horizontal", "vertical", "grid", "form", "stacked", "flow"]


class LayoutMixin(core.ObjectMixin, widgets.LayoutItemMixin):
    def __init__(self, *args, margin=None, **kwargs):
        self._next_container = None
        self._stack = []
        super().__init__(*args, **kwargs)
        if margin is not None:
            self.set_margin(margin)

    def __getitem__(self, index: str | int) -> QtWidgets.QWidget | QtWidgets.QLayout:
        match index:
            case int():
                item = self.itemAt(index)
                return item.widget() or item.layout()
            case str():
                if (item := self.find_child(typ=QtCore.QObject, name=index)) is not None:
                    return item
                raise IndexError(index)
            case _:
                raise IndexError(index)

    def __setitem__(self, key, value):
        if self._container != self:
            self._container.__setitem__(key, value)

    def __delitem__(self, item: int | QtWidgets.QLayoutItem):
        if isinstance(item, int):
            item = self.itemAt(item)
        self.removeItem(item)
        item.deleteLater()

    def __len__(self) -> int:
        return self.count()

    def __iter__(self) -> Iterator[QtWidgets.QWidget | QtWidgets.QLayout | None]:
        return iter(self[i] for i in range(self.count()))

    def __contains__(self, item: QtWidgets.QWidget | QtWidgets.QLayoutItem):
        return self.indexOf(item) >= 0

    def __iadd__(self, item, *args, **kwargs):
        self.add(item, *args, **kwargs)
        return self

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"sizeConstraint": SIZE_CONSTRAINT}
        return maps

    def add(self, item, *args, **kwargs):
        match item:
            case QtWidgets.QWidget():
                self._container.addWidget(item, *args, **kwargs)
            case QtWidgets.QLayout():
                self._container.addLayout(item, *args, **kwargs)
            case list():
                for i in item:
                    self._container.add(i, *args, **kwargs)
        return item

    def __enter__(self):
        def enter(item):
            if item._next_container is not None:
                enter(item._next_container)
                item._stack.append(item._next_container)
                item._next_container = None
            return item

        return enter(self)

    def __exit__(self, *_):
        def exit(item):
            if item._stack:
                item = item._stack.pop()
                exit(item)

        exit(self)

    @property
    def _container(self):
        return self._stack[-1] if self._stack else self

    def get_sub_layout(
        self,
        layout: str,
        orientation: constants.OrientationStr | None = None,
        stretch: int | None = None,
        **kwargs,
    ) -> Self:
        from prettyqt import custom_widgets

        CONTEXT_LAYOUTS = dict(
            horizontal=widgets.HBoxLayout,
            vertical=widgets.VBoxLayout,
            grid=widgets.GridLayout,
            form=widgets.FormLayout,
            stacked=widgets.StackedLayout,
            flow=custom_widgets.FlowLayout,
            splitter=widgets.Splitter,
            scroll=widgets.ScrollArea,
        )
        Klass = CONTEXT_LAYOUTS[layout]
        match self._container:
            case QtWidgets.QWidget() if layout == "scroll":
                scroller = Klass(parent=self._container)
                scroller.setWidgetResizable(True)
                widget = widgets.Widget()
                scroller.set_widget(widget)
                new = widget.set_layout(orientation, **kwargs)
            case QtWidgets.QLayout() if layout == "scroll":
                scroller = Klass(parent=self._container)
                scroller.setWidgetResizable(True)
                widget = widgets.Widget()
                scroller.set_widget(widget)
                new = widget.set_layout(orientation, **kwargs)
                self._container.add(new)
            case QtWidgets.QWidget() if layout == "splitter":
                new = Klass(orientation=orientation, parent=self._container, **kwargs)
            case QtWidgets.QLayout() if layout == "splitter":
                new = Klass(orientation=orientation, **kwargs)
                self._container.add(new)
            case QtWidgets.QMainWindow():
                widget = widgets.Widget(parent=self._container)
                self._container.setCentralWidget(widget)
                new = Klass(widget, **kwargs)
            case QtWidgets.QScrollArea():
                widget = widgets.Widget(parent=self._container)
                self._container.setWidget(widget)
                self._container.setWidgetResizable(True)
                new = widget.set_layout("vertical", **kwargs)
            case QtWidgets.QSplitter():
                widget = widgets.Widget(parent=self._container)
                self._container.addWidget(widget)
                new = Klass(widget, **kwargs)
            case None | QtWidgets.QWidget():
                new = Klass(self._container, **kwargs)
            case QtWidgets.QLayout():
                new = Klass(**kwargs)
                if stretch:
                    self._container.add(new, stretch)
                else:
                    self._container.add(new)
        new._stack = []
        new._next_container = None
        self._next_container = new
        return self

    def item_at(self, pos_or_index: int | core.Point) -> widgets.QLayoutItem:
        match pos_or_index:
            case int():
                return super().itemAt(pos_or_index)
            case QtCore.QPoint():
                for i in range(self.count()):
                    item = self.itemAt(i)
                    if item.geometry().contains(pos_or_index):
                        return item
            case _:
                raise ValueError(pos_or_index)

    def clear(self):
        for i in reversed(range(self.count())):
            self.takeAt(i)

    def get_children(self) -> list[QtWidgets.QWidget | QtWidgets.QLayout]:
        return list(self)

    def set_margin(self, margin: tuple[int, int, int, int] | int | None):
        match margin:
            case None:
                self.unsetContentsMargins()
            case int():
                self.setContentsMargins(margin, margin, margin, margin)
            case (int(), int(), int(), int()):
                self.setContentsMargins(*margin)
            case _:
                raise ValueError(margin)

    def set_spacing(self, pixels: int):
        self.setSpacing(pixels)

    @deprecated(reason="Use set_size_constraint instead")
    def set_size_mode(self, mode: SizeConstraintStr):
        self.set_size_constraint(mode)

    def set_size_constraint(self, mode: SizeConstraintStr):
        """Set the size mode of the layout.

        Args:
            mode: size mode for the layout

        Raises:
            InvalidParamError: size mode does not exist
        """
        if mode not in SIZE_CONSTRAINT:
            raise InvalidParamError(mode, SIZE_CONSTRAINT)
        self.setSizeConstraint(SIZE_CONSTRAINT[mode])

    @deprecated(reason="Use set_size_constraint instead")
    def get_size_mode(self) -> SizeConstraintStr:
        return self.get_size_constraint()

    def get_size_constraint(self) -> SizeConstraintStr:
        """Return current size mode.

        Returns:
            size mode
        """
        return SIZE_CONSTRAINT.inverse[self.sizeConstraint()]

    def set_alignment(
        self,
        alignment: constants.AlignmentStr,
        item: QtWidgets.QWidget | QtWidgets.QLayout | None = None,
    ) -> bool:
        """Set the alignment for widget / layout to alignment.

        Returns true if w is found in this layout (not including child layouts).

        Args:
            alignment: alignment for the layout
            item: set alignment for specific child only

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in constants.ALIGNMENTS:
            raise InvalidParamError(alignment, constants.ALIGNMENTS)
        if item is not None:
            return self.setAlignment(item, constants.ALIGNMENTS[alignment])
        else:
            return self.setAlignment(constants.ALIGNMENTS[alignment])

    # def add(self, *items: QtWidgets.QWidget | QtWidgets.QLayout):
    #     for i in items:
    #         match i:
    #             case QtWidgets.QWidget():
    #                 self.addWidget(i)
    #             case QtWidgets.QLayout():
    #                 w = widgets.Widget()
    #                 w.set_layout(i)
    #                 self.addWidget(w)
    #             case _:
    #                 raise TypeError("add_item only supports widgets and layouts")


class Layout(LayoutMixin, QtWidgets.QLayout):
    pass


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()
    widget = debugging.example_widget()

    widget.show()
    with app.debug_mode():
        app.main_loop()
