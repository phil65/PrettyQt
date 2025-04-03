from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Self, overload

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict, datatypes, listdelegators


if TYPE_CHECKING:
    from collections.abc import Iterator


# @contxtlib.contextmanager
# def get_sub_layout(
#     self,
#     sub_container: str,
#     parent: widgets.Widget | widgets.QLayout,
#     orientation: constants.OrientationStr | None = None,
#     stretch: int | None = None,
#     **kwargs,
# ):
#     match sub_container:
#         case "scroll":
#             scroller = widgets.ScrollArea(parent=parent)
#             scroller.setWidgetResizable(True)
#             widget = widgets.Widget(scroller)
#             scroller.set_widget(widget)
#             return widget.set_layout(orientation, **kwargs)
#         case "splitter":
#             return widgets.Splitter(orientation=orientation, parent=parent, **kwargs)
#         case "groupbox":
#             frame = widgets.GroupBox(parent=parent, **kwargs)
#             return frame.set_layout(orientation or "horizontal")
#         case "mainwindow":
#             return widgets.MainWindow(parent=parent)
#         case _:
#             from prettyqt import custom_widgets
#             ctx_layouts = dict(
#                 horizontal=widgets.HBoxLayout,
#                 vertical=widgets.VBoxLayout,
#                 grid=widgets.GridLayout,
#                 form=widgets.FormLayout,
#                 stacked=widgets.StackedLayout,
#                 flow=custom_widgets.FlowLayout,
#                 border=custom_widgets.BorderLayout,
#             )
#             Klass = ctx_layouts[sub_container]
#             layout = Klass(**kwargs)
#             widget = widgets.Widget(parent=parent)
#             widget.set_layout(layout)
#             return layout


SIZE_CONSTRAINT = bidict(
    default=widgets.QLayout.SizeConstraint.SetDefaultConstraint,
    fixed=widgets.QLayout.SizeConstraint.SetFixedSize,
    minimum=widgets.QLayout.SizeConstraint.SetMinimumSize,
    maximum=widgets.QLayout.SizeConstraint.SetMaximumSize,
    min_and_max=widgets.QLayout.SizeConstraint.SetMinAndMaxSize,
    none=widgets.QLayout.SizeConstraint.SetNoConstraint,
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

    @overload
    def __getitem__(
        self, index: slice
    ) -> listdelegators.ListDelegator[widgets.QWidget | widgets.QLayout]: ...

    @overload
    def __getitem__(self, index: int | str) -> widgets.QWidget | widgets.QLayout: ...

    def __getitem__(
        self, index: str | int | slice
    ) -> (
        widgets.QWidget
        | widgets.QLayout
        | listdelegators.ListDelegator[widgets.QWidget | widgets.QLayout]
    ):
        match index:
            case int():
                if index < 0:
                    index += self.count()
                if index < 0 or index >= self.count():
                    raise IndexError(index)
                item = self.itemAt(index)
                return i if (i := item.widget()) is not None else item.layout()
            case str():
                if (item := self.find_child(typ=core.QObject, name=index)) is not None:
                    return item
                raise KeyError(index)
            case slice():
                stop = index.stop or self.count()
                rng = range(index.start or 0, stop, index.step or 1)
                widgets = [self[i] for i in rng]
                return listdelegators.ListDelegator(widgets, parent=self)
            case _:
                raise TypeError(index)

    def __setitem__(self, key, value):
        if self._container != self:
            self._container.__setitem__(key, value)

    def __delitem__(self, item: int | widgets.QLayoutItem):
        if isinstance(item, int):
            item = self.itemAt(item)
        self.removeItem(item)
        item.deleteLater()

    def __len__(self) -> int:
        return self.count()

    def __iter__(self) -> Iterator[widgets.QWidget | widgets.QLayout | None]:
        return iter(self[i] for i in range(self.count()))

    def __contains__(self, item: widgets.QWidget | widgets.QLayoutItem):
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
            case widgets.QWidget():
                self._container.addWidget(item, *args, **kwargs)
            case widgets.QLayout():
                self._container.addLayout(item, *args, **kwargs)
            case widgets.QLayoutItem():
                self._container.addItem(item, *args, **kwargs)
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
        def exit(item):  # noqa: A001
            if item._stack:
                item = item._stack.pop()
                exit(item)

        exit(self)

    @property
    def _container(self):
        return self._stack[-1] if self._stack else self

    def add_widget(self, widget: widgets.QWidget):
        self.addWidget(widget)

    def get_sub_layout(
        self,
        layout: str,
        orientation: constants.OrientationStr | None = None,
        stretch: int | None = None,
        **kwargs,
    ) -> Self:
        from prettyqt import custom_widgets

        ctx_layouts = dict(
            horizontal=widgets.HBoxLayout,
            vertical=widgets.VBoxLayout,
            grid=widgets.GridLayout,
            form=widgets.FormLayout,
            stacked=widgets.StackedLayout,
            flow=custom_widgets.FlowLayout,
            splitter=widgets.Splitter,
            scroll=widgets.ScrollArea,
            frame=widgets.GroupBox,
        )
        kls = ctx_layouts[layout]
        match self._container:
            case widgets.QWidget() if layout == "scroll":
                scroller = kls(parent=self._container)
                scroller.setWidgetResizable(True)
                widget = widgets.Widget()
                scroller.set_widget(widget)
                new = widget.set_layout(orientation, **kwargs)
            case widgets.QLayout() if layout == "scroll":
                scroller = kls(parent=self._container)
                scroller.setWidgetResizable(True)
                widget = widgets.Widget()
                scroller.set_widget(widget)
                new = widget.set_layout(orientation, **kwargs)
                self._container.add(new)
            case widgets.QWidget() if layout == "splitter":
                new = kls(orientation=orientation, parent=self._container, **kwargs)
            case widgets.QLayout() if layout == "splitter":
                new = kls(orientation=orientation, **kwargs)
                self._container.add(new)
            case widgets.QWidget() if layout == "frame":
                frame = kls(parent=self._container, **kwargs)
                widget = widgets.Widget()
                new = widget.set_layout(orientation or "horizontal")
                frame.set_layout(new)
            case widgets.QLayout() if layout == "frame":
                frame = kls(**kwargs)
                widget = widgets.Widget()
                new = widget.set_layout(orientation or "horizontal")
                frame.set_layout(new)
                self._container.add(new)
            case widgets.QMainWindow():
                widget = widgets.Widget(parent=self._container)
                self._container.setCentralWidget(widget)
                new = kls(widget, **kwargs)
            case widgets.QScrollArea():
                widget = widgets.Widget(parent=self._container)
                self._container.setWidget(widget)
                self._container.setWidgetResizable(True)
                new = widget.set_layout("vertical", **kwargs)
            case widgets.QSplitter():
                widget = widgets.Widget(parent=self._container)
                self._container.addWidget(widget)
                new = kls(widget, **kwargs)
            case None | widgets.QWidget():
                new = kls(self._container, **kwargs)
            case widgets.QLayout():
                new = kls(**kwargs)
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
            case core.QPoint():
                for i in range(self.count()):
                    item = self.itemAt(i)
                    if item.geometry().contains(pos_or_index):
                        return item
                return None
            case _:
                raise ValueError(pos_or_index)

    def clear(self):
        for i in reversed(range(self.count())):
            self.takeAt(i)

    # def takeAt(self, index: int):
    #     if index < 0:
    #         index = self.count() + index
    #     return super().takeAt(index)

    def get_items(self):
        return [self.itemAt(i) for i in range(self.count())]

    def get_children(
        self,
    ) -> listdelegators.ListDelegator[widgets.QWidget | widgets.QLayout]:
        return listdelegators.ListDelegator(self)

    def set_margin(self, margin: datatypes.MarginsType | None):
        match margin:
            case None:
                self.unsetContentsMargins()
            case _:
                margin = datatypes.to_margins(margin)
                self.setContentsMargins(margin)

    def set_spacing(self, pixels: int):
        self.setSpacing(pixels)

    def set_size_constraint(
        self, mode: SizeConstraintStr | widgets.QLayout.SizeConstraint
    ):
        """Set the size mode of the layout.

        Args:
            mode: size mode for the layout
        """
        self.setSizeConstraint(SIZE_CONSTRAINT.get_enum_value(mode))

    def get_size_constraint(self) -> SizeConstraintStr:
        """Return current size mode.

        Returns:
            size mode
        """
        return SIZE_CONSTRAINT.inverse[self.sizeConstraint()]

    def set_alignment(
        self,
        alignment: constants.AlignmentStr | constants.AlignmentFlag,
        item: widgets.QWidget | widgets.QLayout | None = None,
    ) -> bool:
        """Set the alignment for widget / layout to alignment.

        Returns true if w is found in this layout (not including child layouts).

        Args:
            alignment: alignment for the layout
            item: set alignment for specific child only
        """
        if item is not None:
            return self.setAlignment(item, constants.ALIGNMENTS.get_enum_value(alignment))
        return self.setAlignment(constants.ALIGNMENTS.get_enum_value(alignment))

    # def add(self, *items: widgets.QWidget | widgets.QLayout):
    #     for i in items:
    #         match i:
    #             case widgets.QWidget():
    #                 self.addWidget(i)
    #             case widgets.QLayout():
    #                 w = widgets.Widget()
    #                 w.set_layout(i)
    #                 self.addWidget(w)
    #             case _:
    #                 raise TypeError("add_item only supports widgets and layouts")


class Layout(LayoutMixin, widgets.QLayout):
    """The base class of geometry managers."""


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()
    widget = debugging.example_widget()

    widget.show()
    with app.debug_mode():
        app.exec()
