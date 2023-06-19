"""Object browser GUI in Qt."""


from __future__ import annotations

import logging

from prettyqt import constants, core, custom_models, gui, widgets
from prettyqt.custom_models.pythonobjecttreemodel import (
    CommentsColumn,
    DocStringColumn,
    FileColumn,
    SourceCodeColumn,
    PathColumn,
    PrettyPrintColumn,
    ReprColumn,
    StrColumn,
)


DEFAULT_ATTR_DETAILS = [
    PathColumn,
    StrColumn,
    ReprColumn,
    PrettyPrintColumn,
    DocStringColumn,
    CommentsColumn,
    FileColumn,
    SourceCodeColumn,
]

logger = logging.getLogger(__name__)



class ObjectBrowserTreeProxyModel(core.SortFilterProxyModel):
    """Proxy model that overrides the sorting and can filter out items."""

    def __init__(
        self, show_callable_attrs: bool = True, show_special_attrs: bool = True, **kwargs
    ):
        super().__init__(**kwargs)

        self._show_callables = show_callable_attrs
        self._show_special_attrs = show_special_attrs

    def data_by_index(self, proxy_index: core.ModelIndex):
        index = self.mapToSource(proxy_index)
        return self.get_source_model().data_by_index(index)

    def filterAcceptsRow(self, source_row: int, source_parent_index: core.ModelIndex):
        """Return true if the item should be included in the model."""
        parent_item = self.get_source_model().data_by_index(source_parent_index)
        tree_item = parent_item.child(source_row)
        is_callable_attr = tree_item.is_attribute and callable(tree_item.obj)
        return (self._show_special_attrs or not tree_item.is_special_attribute) and (
            self._show_callables or not is_callable_attr
        )

    def get_show_callables(self) -> bool:
        return self._show_callables

    def set_show_callables(self, show_callables: bool):
        """Show/hide show_callables which have a __call__ attribute."""
        self._show_callables = show_callables
        self.invalidateRowsFilter()

    def get_show_special_attrs(self) -> bool:
        return self._show_special_attrs

    def set_show_special_attrs(self, show_special_attrs: bool):
        """Show/hide special attributes which begin with an underscore."""
        self._show_special_attrs = show_special_attrs
        self.invalidateRowsFilter()


class ObjectBrowser(widgets.MainWindow):
    """Object browser main application window."""

    def __init__(self, obj, stack=None, name: str = ""):
        super().__init__()
        self.set_title("Object browser")
        self.set_icon("mdi.language-python")
        self._auto_refresh = False
        self._refresh_rate = 2
        show_callable_attrs = True
        show_special_attrs = True
        self._tree_model = custom_models.PythonObjectTreeModel(obj)
        self._attr_details = [
            Klass(model=self._tree_model) for Klass in DEFAULT_ATTR_DETAILS
        ]
        # proxy = self._tree_model.proxifier.modify(
        #     fn=lambda x: SPECIAL_ATTR_FONT,
        #     role=constants.FONT_ROLE,
        #     selector=lambda x: x.startswith("__") and x.endswith("__"),
        #     selector_role=constants.DISPLAY_ROLE
        # )

        self._proxy_tree_model = ObjectBrowserTreeProxyModel(
            show_callable_attrs=show_callable_attrs,
            show_special_attrs=show_special_attrs,
            dynamic_sort_filter=True,
        )

        self._proxy_tree_model.setSourceModel(self._tree_model)
        # self._proxy_tree_model.setSortRole(constants.SORT_ROLE)
        # self._proxy_tree_model.setSortCaseSensitivity(Qt.CaseInsensitive)

        self.toggle_callable_action = gui.Action(
            text="Show callable attributes",
            parent=self,
            checkable=True,
            shortcut="Alt+C",
            status_tip="Shows/hides callable attributes (functions, methods, etc.)",
        )
        self.toggle_callable_action.toggled.connect(
            self._proxy_tree_model.set_show_callables
        )

        # Show/hide special attributes
        self.toggle_special_attribute_action = gui.Action(
            text="Show __special__ attributes",
            parent=self,
            checkable=True,
            shortcut="Alt+S",
            status_tip="Shows or hides __special__ attributes",
        )
        self.toggle_special_attribute_action.toggled.connect(
            self._proxy_tree_model.set_show_special_attrs
        )

        # Toggle auto-refresh on/off
        self.toggle_auto_refresh_action = gui.Action(
            text="Auto-refresh",
            parent=self,
            checkable=True,
            status_tip=f"Auto refresh every {self._refresh_rate} seconds",
        )
        self.toggle_auto_refresh_action.toggled.connect(self.toggle_auto_refresh)

        # Add another refresh action with a different shortcut. An action must be added to
        # a visible widget for it to receive events. It is added to the main windows to
        # prevent it from being displayed again in the menu

        self.refresh_action_f5 = self.add_action(
            text="&Refresh2", shortcut="F5", triggered=self._tree_model.refresh_tree
        )
        self.central_splitter = widgets.Splitter(
            parent=self, orientation=constants.VERTICAL
        )
        self.setCentralWidget(self.central_splitter)

        # Tree widget
        self.obj_tree = widgets.TreeView(
            root_is_decorated=True, selection_behavior="rows"
        )
        self.obj_tree.set_model(self._proxy_tree_model)

        # Stretch last column?
        # It doesn't play nice when columns are hidden and then shown again.
        self.obj_tree.h_header.set_id("table_header")
        self.obj_tree.h_header.setSectionsMovable(True)
        self.obj_tree.h_header.setStretchLastSection(False)
        self.central_splitter.addWidget(self.obj_tree)

        # Bottom pane
        bottom_pane_widget = widgets.Widget()
        bottom_pane_widget.set_layout("horizontal", spacing=0, margin=5)
        self.central_splitter.addWidget(bottom_pane_widget)

        group_box = widgets.GroupBox("Details")
        bottom_pane_widget.box.addWidget(group_box)

        group_box.set_layout("horizontal", margin=2)

        # Radio buttons
        radio_widget = widgets.Widget()
        radio_widget.set_layout("vertical", margin=0)

        self.button_group = widgets.ButtonGroup(
            self, button_clicked=self._change_details_field
        )
        for button_id, attr_detail in enumerate(self._attr_details):
            radio_button = widgets.RadioButton(attr_detail.name)
            radio_widget.box.addWidget(radio_button)
            self.button_group.addButton(radio_button, button_id)

        self.button_group.button(0).setChecked(True)

        radio_widget.box.addStretch(1)
        group_box.box.addWidget(radio_widget)

        self.editor = widgets.PlainTextEdit(read_only=True, font=gui.Font.mono())
        group_box.box.addWidget(self.editor)

        # Splitter parameters
        self.central_splitter.setCollapsible(0, False)
        self.central_splitter.setCollapsible(1, True)
        self.central_splitter.setSizes([400, 200])
        self.central_splitter.setStretchFactor(0, 10)
        self.central_splitter.setStretchFactor(1, 0)

        selection_model = self.obj_tree.selectionModel()
        selection_model.currentChanged.connect(self._update_details)
        menubar = self.menuBar()
        file_menu = menubar.add_menu("&File")
        file_menu.add_action(text="C&lose", triggered=self.close, shortcut="Ctrl+W")
        file_menu.add_action(
            text="E&xit",
            triggered=lambda: widgets.app().closeAllWindows(),
            shortcut="Ctrl+Q",
        )

        view_menu = menubar.add_menu("&View")
        view_menu.add_action(
            text="&Refresh", triggered=self._tree_model.refresh_tree, shortcut="Ctrl+R"
        )
        view_menu.addAction(self.toggle_auto_refresh_action)

        view_menu.addSeparator()
        self.show_cols_submenu = self.obj_tree.h_header.createPopupMenu()
        self.show_cols_submenu.setTitle("Table columns")
        view_menu.add_menu(self.show_cols_submenu)
        view_menu.addSeparator()
        view_menu.addAction(self.toggle_callable_action)
        view_menu.addAction(self.toggle_special_attribute_action)

        assert self._refresh_rate > 0
        self._refresh_timer = core.Timer(self)
        self._refresh_timer.setInterval(self._refresh_rate * 1000)
        self._refresh_timer.timeout.connect(self._tree_model.refresh_tree)

        # Update views with model
        self.toggle_special_attribute_action.setChecked(show_special_attrs)
        self.toggle_callable_action.setChecked(show_callable_attrs)
        self.toggle_auto_refresh_action.setChecked(self._auto_refresh)

        # Select first row so that a hidden root node will not be selected.
        first_row_index = self._proxy_tree_model.first_item_index()
        self.obj_tree.setCurrentIndex(first_row_index)
        if self._tree_model.show_root:
            self.obj_tree.expand(first_row_index)

    @core.Slot(core.ModelIndex, core.ModelIndex)
    def _update_details(
        self, current_index: core.ModelIndex, _previous_index: core.ModelIndex
    ):
        """Show the object details in the editor given an index."""
        tree_item = self._proxy_tree_model.data_by_index(current_index)
        self._update_details_for_item(tree_item)

    def _change_details_field(self, _button_id=None):
        """Change the field that is displayed in the details pane."""
        # logger.debug("_change_details_field: {}".format(_button_id))
        current_index = self.obj_tree.selectionModel().currentIndex()
        tree_item = self._proxy_tree_model.data_by_index(current_index)
        self._update_details_for_item(tree_item)

    def _update_details_for_item(self, tree_item):
        """Show the object details in the editor given an tree_item."""
        button_id = self.button_group.checkedId()
        attr_details = self._attr_details[button_id]
        data = attr_details.get_data(tree_item)
        self.editor.set_text(data)
        self.editor.set_word_wrap_mode(attr_details.line_wrap)

    def toggle_auto_refresh(self, checked):
        """Toggle auto-refresh on/off."""
        if checked:
            logger.info("Auto-refresh on. Rate %g seconds", self._refresh_rate)
            self._refresh_timer.start()
        else:
            logger.info("Auto-refresh off")
            self._refresh_timer.stop()
        self._auto_refresh = checked

    def closeEvent(self, event):
        """Called when the window is closed."""
        logger.debug("closeEvent")
        self._refresh_timer.stop()
        self._refresh_timer.timeout.disconnect(self._tree_model.refresh_tree)
        self.toggle_callable_action.toggled.disconnect(
            self._proxy_tree_model.set_show_callables
        )
        self.toggle_special_attribute_action.toggled.disconnect(
            self._proxy_tree_model.set_show_special_attrs
        )
        self.toggle_auto_refresh_action.toggled.disconnect(self.toggle_auto_refresh)
        self.refresh_action_f5.triggered.disconnect(self._tree_model.refresh_tree)
        self.button_group.buttonClicked.disconnect(self._change_details_field)
        selection_model = self.obj_tree.selectionModel()
        selection_model.currentChanged.disconnect(self._update_details)
        self.close()
        event.accept()


if __name__ == "__main__":
    struct = dict(a={1, 2, frozenset([1, 2])})
    app = widgets.app()
    with app.debug_mode():
        object_browser = ObjectBrowser(struct)
        object_browser.show()
        app.main_loop()
