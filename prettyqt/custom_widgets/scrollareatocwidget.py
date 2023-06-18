from __future__ import annotations

import enum
import logging

from prettyqt import constants, core, custom_models, gui, widgets
from prettyqt.utils import treeitem

logger = logging.getLogger(__name__)


class SectionWidget(widgets.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout("vertical", margin=0, spacing=0)
        self.set_margin(0)
        header = widgets.Label(self.windowTitle()).set_bold()
        header.set_point_size(header.font().pointSize() * 2)
        self.box.add(header)


class ScrollAreaTocModel(custom_models.TreeModel):
    def __init__(
        self, *args, widget_class: type[widgets.QWidget] = widgets.QWidget, **kwargs
    ):
        self._highlight_font = gui.QFont()
        self._highlight_font.setBold(True)
        self._Class = widget_class
        self._current_indexes: list[core.ModelIndex] = []
        super().__init__(*args, **kwargs)

    def set_highlighted_indexes(self, indexes: list[core.ModelIndex]):
        self._current_indexes = indexes
        self.update_all()

    def columnCount(self, parent=None):
        return 1

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        widget = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE, _:
                return widget.windowTitle()
            case constants.USER_ROLE, _:
                return widget
            case constants.FONT_ROLE, _ if index in self._current_indexes:
                # if not index.parent().isValid():
                return self._highlight_font

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        flag = constants.FindChildOption.FindDirectChildrenOnly
        children = item.obj.findChildren(self._Class, None, flag)
        children = [i for i in children if i.windowTitle()]
        return [treeitem.TreeItem(obj=i) for i in children]

    def _has_children(self, item: treeitem.TreeItem) -> bool:
        flag = constants.FindChildOption.FindDirectChildrenOnly
        children = item.obj.findChildren(self._Class, None, flag)
        children = [i for i in children if i.windowTitle()]
        return bool(children)

    def set_highlight_font(self, font: gui.QFont):
        self._highlight_font = font

    def get_highlight_font(self) -> gui.QFont:
        return self._highlight_font

    highlight_font = core.Property(gui.QFont, get_highlight_font, set_highlight_font)



class ScrollAreaTocWidget(widgets.TreeView):
    section_changed = core.Signal()

    @core.Enum
    class ScrollMode(enum.Enum):
        """Scroll modes."""

        Single = 1
        Multi = 2
        HeadersOnly = 4

    @core.Enum
    class ExpandMode(enum.Enum):
        """Expand modes."""

        Always = 1
        OnFocus = 2

    def __init__(
        self,
        scrollarea: widgets.QScrollArea,
        orientation: constants.Orientation = constants.VERTICAL,
        widget_class: type = widgets.QWidget,
        **kwargs,
    ) -> None:
        # TODO: not sure if parent should always equal scrollarea..."""
        self._WidgetClass = widget_class
        self._scroll_mode = "single"
        self._expand_mode = "always"
        self._last_visible = None
        self.scrollarea = scrollarea
        super().__init__(scrollarea, **kwargs)
        self._orientation = orientation
        self.setFixedWidth(200)
        self.h_header.hide()
        self.h_header.setStretchLastSection(True)
        self.setAlternatingRowColors(False)
        self.setRootIsDecorated(False)
        self.setAnimated(False)
        # self.setStyleSheet(
        #     """::item:hover {background: transparent; border-color:transparent}
        #     ::item:selected { border-color:transparent;
        #     border-style:outset; border-width:2px; color:black; }"""
        # )
        if orientation == constants.VERTICAL:
            scrollarea.v_scrollbar.valueChanged.connect(self._on_scroll)
        else:
            scrollarea.h_scrollbar.valueChanged.connect(self._on_scroll)
        self.set_widget(scrollarea)

    def showEvent(self, event):
        super().showEvent(event)
        self._on_scroll()

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
        self.show_root(False)
        widget.widget().installEventFilter(self)
        self.selectionModel().currentChanged.connect(self._on_current_change)
        self.selectionModel().selectionChanged.connect(self._on_selection_change)
        # if self._expand_mode == "always":
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
        indexes = self.selected_indexes()
        self.model().set_highlighted_indexes(indexes)

    def _on_scroll(self):
        model: ScrollAreaTocModel | None = self.model()
        if model is None:
            return
        visible_widgets = self.scrollarea.get_visible_widgets(typ=self._WidgetClass)
        if not visible_widgets or visible_widgets == self._last_visible:
            return
        self._last_visible = visible_widgets
        sig = self.selectionModel().currentChanged
        with self.signal_blocked(sig, self._on_current_change):
            self.select_index(None)
            if self._expand_mode != "always":
                self.collapseAll()
            match self._scroll_mode:
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

    def get_scroll_mode(self) -> str:
        return self._scroll_mode

    def set_scroll_mode(self, mode: str):
        self._scroll_mode = mode

    def get_expand_mode(self) -> str:
        return self._expand_mode

    def set_expand_mode(self, mode: str):
        self._expand_mode = mode

    scrollMode = core.Property(str, get_scroll_mode, set_scroll_mode)
    expandMode = core.Property(str, get_expand_mode, set_expand_mode)


if __name__ == "__main__":
    app = widgets.app()
    with app.debug_mode():
        window = widgets.Widget(object_name="window")
        layout = window.set_layout("horizontal")
        scrollarea = widgets.ScrollArea(object_name="scroll", parent=window)
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
        scrollarea.setWidgetResizable(True)
        window.show()
        app.main_loop()