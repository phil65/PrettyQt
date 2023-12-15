from __future__ import annotations

import enum
import logging
from typing import Literal

from prettyqt import constants, core, gui, itemmodels, widgets
from prettyqt.utils import bidict


logger = logging.getLogger(__name__)


class SectionWidget(widgets.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout("vertical", margin=0, spacing=0)
        self.set_margin(0)
        header = widgets.Label(self.windowTitle()).set_bold()
        header.set_point_size(header.font().pointSize() * 2)
        self.box.add(header)
        for i in range(5):
            subitem = widgets.CheckBox(f"sub item {i}")
            self.box.add(subitem)


class ScrollAreaTocModel(itemmodels.TreeModel):
    def __init__(
        self, *args, widget_class: type[widgets.QWidget] = widgets.QWidget, **kwargs
    ):
        self._highlight_font = gui.QFont()
        self._highlight_font.setBold(True)
        self._Class = widget_class
        self._current_widgets: list[widgets.QWidget] = []
        self._header_property = "windowTitle"
        super().__init__(*args, **kwargs)

    def set_highlighted_widgets(self, widgets: list[widgets.QWidget]):
        self._current_widgets = widgets
        self.update_all()

    def columnCount(self, parent=None):
        return 1

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        widget = self.data_by_index(index).obj
        match role:
            case constants.DISPLAY_ROLE if widget in self._current_widgets:
                return f"> {widget.property(self.header_property)}"
            case constants.DISPLAY_ROLE:
                return widget.property(self.header_property)
            case constants.DECORATION_ROLE:
                return widget.windowIcon()
            case constants.USER_ROLE:
                return widget
            case constants.FONT_ROLE if widget in self._current_widgets:
                # if not index.parent().isValid():
                return self._highlight_font

    def _fetch_object_children(
        self, item: ScrollAreaTocModel.TreeItem
    ) -> list[ScrollAreaTocModel.TreeItem]:
        flag = constants.FindChildOption.FindDirectChildrenOnly
        children = item.obj.findChildren(self._Class, None, flag)
        children = [i for i in children if i.property(self.header_property)]
        return [self.TreeItem(obj=i) for i in children]

    def _has_children(self, item: ScrollAreaTocModel.TreeItem) -> bool:
        flag = constants.FindChildOption.FindDirectChildrenOnly
        children = item.obj.findChildren(self._Class, None, flag)
        children = [i for i in children if i.property(self.header_property)]
        return bool(children)

    def set_highlight_font(self, font: gui.QFont):
        self._highlight_font = font

    def get_highlight_font(self) -> gui.QFont:
        return self._highlight_font

    def set_header_property(self, prop: str):
        self._header_property = prop

    def get_header_property(self) -> str:
        return self._header_property

    highlight_font = core.Property(
        gui.QFont,
        get_highlight_font,
        set_highlight_font,
        doc="Font to use for highlighting",
    )
    header_property = core.Property(
        str,
        get_header_property,
        set_header_property,
        doc="Property to use for the list labels",
    )


class ScrollMode(enum.Enum):
    Single = 1
    Multi = 2
    HeadersOnly = 4


ScrollModeStr = Literal["single", "multi", "headers_only"]

SCROLL_MODE: bidict[ScrollModeStr, ScrollMode] = bidict(
    single=ScrollMode.Single, multi=ScrollMode.Multi, headers_only=ScrollMode.HeadersOnly
)


class ScrollAreaTocWidget(widgets.TreeView):
    section_changed = core.Signal()

    ScrollMode = ScrollMode
    core.Enum(ScrollMode)

    def __init__(
        self,
        scrollarea: widgets.QScrollArea,
        orientation: (
            constants.Orientation | constants.OrientationStr
        ) = constants.VERTICAL,
        widget_class: type = widgets.QWidget,
        **kwargs,
    ) -> None:
        """A TreeView which can show a Table-of-contents list based on a given ScrollArea.

        With default settings, it will scan the widgets contained in the scrollArea for
         a windowTitle.
        These widgets will be shown in the TreeView, and the TreeView selection will be
        synced to what is currently visible in the ScrollArea.
        This basically emulates the behaviour of many websites
        (like the [Qt Website][https://doc.qt.io/qt-6/supported-platforms.html])
        or from VS code settings.

        You can set up the Toc Tree by passing a ScrollArea instance:

        ```py
        widget = widgets.Widget()
        layout = widget.set_layout("horizontal")
        scrollarea = widgets.ScrollArea()
        # add some widgets to the ScrollArea here
        # ...
        toc = ScrollAreaTocWidget(scrollarea)
        layout.add(toc)
        layout.add(scrollarea)
        ```

        The Toc tree can be configured to use other properties for populating
        than windowTitle.
        You can also set a widget class filter if you only want a specific widget
        class to be shown.

        The widget supports 3 different scroll modes:

        1) Single: Only one row in the Tree will be highlighted. (the one which equals
        the topmost one from the scrollArea)
        2) Multi: All rows which equal to visible widgets in the ScrollArea will be shown.
        3) HeadersOnly: like Single, but only highlights top-level widgets from the
                        ScrollArea.

        There are also two different expand modes to choose from:

        1) ExpandAll: All subsections are always expanded.
        2) on_focus: Only the section containing the focused item is expanded.

        This widget is used by [ConfigWidget](ConfigWidget.md).
        """
        # TODO: not sure if parent should always equal scrollarea..."""
        self._WidgetClass = widget_class
        self._scroll_mode = ScrollMode.Single
        self._always_expanded = False
        self._last_visible = None
        self.scrollarea = scrollarea
        super().__init__(scrollarea, **kwargs)
        self._orientation = constants.ORIENTATION.get_enum_value(orientation)
        self.setFixedWidth(200)
        self.h_header.hide()
        self.h_header.setStretchLastSection(True)
        self.setAlternatingRowColors(False)
        self.setRootIsDecorated(False)
        # self.setStyleSheet(
        #     """::item:hover {background: transparent; border-color:transparent}
        #     ::item:selected { border-color:transparent;
        #     border-style:outset; border-width:2px; color:black; }"""
        # )
        if self._orientation == constants.VERTICAL:
            scrollarea.v_scrollbar.valueChanged.connect(self._on_scroll)
        else:
            scrollarea.h_scrollbar.valueChanged.connect(self._on_scroll)
        self.set_widget(scrollarea)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"scrollMode": SCROLL_MODE}
        return maps

    def showEvent(self, event):
        super().showEvent(event)
        self._on_scroll()

    # @classmethod
    # def setup_example(cls):
    #     scrollarea = widgets.ScrollArea()
    #     w = widgets.Widget()
    #     scrollarea.set_widget(w)
    #     return cls(scrollarea)

    def set_widget(self, widget: widgets.QScrollArea):
        """Set the ScrollArea widget to follow."""
        if widget.widget() is None:
            raise RuntimeError("No widget set on ScrollArea.")
        self.scrollarea = widget
        model = ScrollAreaTocModel(
            widget.widget(),
            show_root=True,
            parent=self.scrollarea,
            widget_class=self._WidgetClass,
        )
        self.set_model(model)
        self.proxy = self.proxifier.set_sort_filter_proxy(
            recursive_filtering_enabled=True
        )
        self.proxy.set_filter_case_sensitive(False)
        self.show_root(False)
        widget.widget().installEventFilter(self)
        self.selectionModel().currentRowChanged.connect(self._on_current_change)
        self.selectionModel().selectionChanged.connect(self._on_selection_change)
        # if self._always_expanded:
        self.expandAll()

    def _on_current_change(self, new, old):
        if self.model() is None:
            return
        is_vertical = self._orientation == constants.VERTICAL
        area = self.scrollarea
        scrollbar = area.v_scrollbar if is_vertical else area.h_scrollbar
        with self.signal_blocked(scrollbar.valueChanged, self._on_scroll):
            widget = self.model().data(new, role=constants.USER_ROLE)
            area.scroll_to_bottom()
            area.ensureWidgetVisible(widget, 10, 10)

    def _on_selection_change(self, new, old):
        if self.model() is None:
            return
        widgets = [i.data(constants.USER_ROLE) for i in self.selected_indexes()]
        self.get_model(skip_proxies=True).set_highlighted_widgets(widgets)

    def _on_scroll(self):
        model: ScrollAreaTocModel | None = self.model()
        if model is None:
            return
        visible_widgets = self.scrollarea.get_visible_widgets(typ=self._WidgetClass)
        if not visible_widgets or visible_widgets == self._last_visible:
            return
        self._last_visible = visible_widgets
        sig = self.selectionModel().currentRowChanged
        with self.signal_blocked(sig, self._on_current_change):
            self.select_index(None)
            if not self._always_expanded:
                self.collapseAll()
            match self.get_scroll_mode():
                case "multi":
                    indexes = model.search_tree(visible_widgets, constants.USER_ROLE)
                    for index in indexes:
                        children = model.get_child_indexes(index)
                        # only select if all children selected.
                        # if all(c in indexes for c in children):

                        # highlight when no children or when first child is visible.
                        if not children or children[0] in indexes:
                            self.select_index(index, clear=False)
                        self.set_expanded(indexes)
                        self.scroll_to(indexes[0])
                        self.scroll_to(indexes[-1])
                case "headers_only":
                    if indexes := model.search_tree(
                        visible_widgets,
                        role=constants.USER_ROLE,
                        max_results=1,
                    ):
                        self.set_current_index(indexes[0])
                        self.scroll_to(indexes[0])
                case "single":
                    if indexes := model.search_tree(visible_widgets, constants.USER_ROLE):
                        viewport = self.scrollarea.viewport()
                        # sort indexes by closest distance to top
                        indexes.sort(
                            key=lambda x: abs(
                                x.data(constants.USER_ROLE)
                                .map_to(viewport, x.data(constants.USER_ROLE).rect())
                                .top()
                            ),
                        )
                        self.collapseAll()
                        self.model().fetchMore(indexes[0])
                        self.set_current_index(indexes[0])
                        self.scroll_to(indexes[0])
                case _:
                    raise ValueError(self._scroll_mode)
        # model.set_highlighted_indexes(indexes)

    def wheelEvent(self, e):
        self.scrollarea.wheelEvent(e)

    def eventFilter(self, source: core.QObject, event: core.QEvent) -> bool:
        match event.type():
            case core.Event.Type.ChildAdded:
                self._on_scroll()
        return False

    def _scrollMode(self) -> ScrollMode:
        return self._scroll_mode

    def get_scroll_mode(self) -> ScrollModeStr:
        return SCROLL_MODE.inverse[self._scrollMode()]

    def set_scroll_mode(self, mode: ScrollMode | ScrollModeStr):
        self._scroll_mode = SCROLL_MODE.get_enum_value(mode)

    def is_always_expanded(self) -> bool:
        return self._always_expanded

    def set_always_expanded(self, always_expanded: bool):
        self._always_expanded = always_expanded

    scrollMode = core.Property(
        enum.Enum,
        _scrollMode,
        set_scroll_mode,
        doc="Scrolling mode",
    )
    always_expanded = core.Property(
        bool,
        is_always_expanded,
        set_always_expanded,
        doc="Whether the tree is always expanded.",
    )


if __name__ == "__main__":
    app = widgets.app()
    with app.debug_mode():
        window = widgets.Widget(object_name="window")
        layout = window.set_layout("horizontal")
        scrollarea = widgets.ScrollArea(
            object_name="scroll", parent=window, widget_resizable=True
        )
        widget = widgets.Widget(object_name="scrollarea_widget")
        scrollarea.setWidget(widget)
        toc_widget = ScrollAreaTocWidget(
            scrollarea,
            scroll_mode="headers_only",
            widget_class=SectionWidget,
        )
        layout.add(toc_widget)
        scroll_layout = widget.set_layout("vertical")
        layout.add(scrollarea)
        for i in range(10):
            section = SectionWidget(window_title=f"test{i}")
            section.box.add(SectionWidget(window_title=f"{i}nested"))
            section.box.add(SectionWidget(window_title=f"{i*10}nested"))
            scroll_layout.add(section)
        window.show()
        app.exec()
