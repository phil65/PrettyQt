from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from deprecated import deprecated
from typing_extensions import Self

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, get_repr, prettyprinter


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


class LayoutMixin(core.ObjectMixin, widgets.LayoutItemMixin, prettyprinter.PrettyPrinter):
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
                return widget if (widget := item.widget()) is not None else item.layout()
            case str():
                if (item := self.find_child(typ=QtCore.QObject, name=index)) is not None:
                    return item
                raise IndexError(index)
            case _:
                raise IndexError(index)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def __delitem__(self, item: int | QtWidgets.QLayoutItem):
        if isinstance(item, int):
            item = self.itemAt(item)
        self.removeItem(item)
        item.deleteLater()

    def __len__(self) -> int:
        return self.count()

    def __repr__(self):
        return get_repr(self)

    def __iter__(self) -> Iterator[QtWidgets.QWidget | QtWidgets.QLayout | None]:
        return iter(self[i] for i in range(self.count()))

    def __contains__(self, item: QtWidgets.QWidget | QtWidgets.QLayoutItem):
        return self.indexOf(item) >= 0

    def __enter__(self):
        if self._next_container is not None:
            self._next_container.__enter__()
            self._stack.append(self._next_container)
            self._next_container = None
        return self

    def __exit__(self, *_):
        if self._stack:
            item = self._stack.pop()
            item.__exit__()

    def __iadd__(self, item, *args, **kwargs):
        self.add(item, *args, **kwargs)
        return self

    # def __getattr__(self, name):
    #     return getattr(self._layout, name)

    # def __call__(self):
    #     return self._layout

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"sizeConstraint": SIZE_CONSTRAINT}
        return maps

    def add(self, item, *args, **kwargs):
        if isinstance(item, QtWidgets.QWidget):
            self._layout.addWidget(item, *args, **kwargs)
        elif isinstance(item, QtWidgets.QLayout):
            self._layout.addLayout(item, *args, **kwargs)
            # widget = Widgets.Widget()
            # widget.set_layout(item)
            # self._layout.addWidget(item, *args, **kwargs)
        elif isinstance(item, list):
            for i in item:
                self._layout.add(i, *args, **kwargs)

        return item

    @property
    def _layout(self):
        return self._stack[-1] if self._stack else self

    @classmethod
    def create(
        cls,
        parent: QtWidgets.QWidget | QtWidgets.QLayout | None = None,
        stretch: int | None = None,
        margin: int | None = None,
        align: constants.AlignmentStr | None = None,
        **kwargs,
    ) -> Self:
        """Create a Layout attached to given parent. Insert widget if needed."""
        match parent:
            case QtWidgets.QMainWindow():
                widget = widgets.Widget(parent=parent)
                parent.setCentralWidget(widget)
                new = cls(widget, **kwargs)
            case QtWidgets.QScrollArea():
                widget = widgets.Widget(parent=parent)
                parent.setWidget(widget)
                new = cls(widget, **kwargs)
            case QtWidgets.QSplitter():
                widget = widgets.Widget(parent=parent)
                parent.addWidget(widget)
                new = cls(widget, **kwargs)
            case None | QtWidgets.QWidget():
                new = cls(parent, **kwargs)
            case QtWidgets.QLayout():
                new = cls(**kwargs)
                if stretch:
                    parent.addLayout(new, stretch)
                else:
                    parent.addLayout(new)

        if margin is not None:
            new.set_margin(margin)
        if align is not None:
            new.set_alignment(align)

        new._stack = []
        new._next_container = None
        return new

    def get_sub_layout(self, layout: str, *args, **kwargs) -> Self:
        match layout:
            case "horizontal":
                Class = widgets.HBoxLayout
            case "vertical":
                Class = widgets.VBoxLayout
            case "grid":
                Class = widgets.GridLayout
            case "form":
                Class = widgets.FormLayout
            case "stacked":
                Class = widgets.StackedLayout
            case "flow":
                from prettyqt import custom_widgets

                Class = custom_widgets.FlowLayout
            case "splitter":
                Class = widgets.Splitter
            case "scroll":
                Class = widgets.ScrollArea
            case _:
                raise ValueError("Invalid Layout")
        self._next_container = Class.create(self._layout, *args, **kwargs)
        return self

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
            case tuple():
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
    app.main_loop()
