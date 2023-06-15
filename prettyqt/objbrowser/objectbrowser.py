"""Object browser GUI in Qt."""


from __future__ import annotations

import hashlib
import logging
import traceback

from prettyqt import constants, core, gui, widgets
from prettyqt.objbrowser import objectbrowsertreemodel
from prettyqt.objbrowser.attribute_model import (
    ATTR_MODEL_GET_COMMENTS,
    ATTR_MODEL_GET_DOC,
    ATTR_MODEL_GET_FILE,
    ATTR_MODEL_GET_SOURCE,
    ATTR_MODEL_PATH,
    ATTR_MODEL_PRETTY_PRINT,
    ATTR_MODEL_REPR,
    ATTR_MODEL_STR,
    DEFAULT_ATTR_COLS,
)


DEFAULT_ATTR_DETAILS = [
    ATTR_MODEL_PATH,
    ATTR_MODEL_STR,
    ATTR_MODEL_REPR,
    ATTR_MODEL_PRETTY_PRINT,
    ATTR_MODEL_GET_DOC,
    ATTR_MODEL_GET_COMMENTS,
    ATTR_MODEL_GET_FILE,
    ATTR_MODEL_GET_SOURCE,
]

logger = logging.getLogger(__name__)


# It's not possible to use locals() as default for obj by taking take the locals
# from one stack frame higher; you can't know if the ObjectBrowser.__init__ was
# called directly, via the browse() wrapper or via a descendants' constructor.


class ObjectBrowser(widgets.MainWindow):
    """Object browser main application window."""

    def __init__(self, obj, stack=None, name: str = ""):
        super().__init__()
        self.set_title("Object browser")
        self.set_icon("mdi.language-python")
        self._attr_cols = DEFAULT_ATTR_COLS
        self._attr_details = DEFAULT_ATTR_DETAILS

        with core.Settings(settings_id=self._settings_group_name("model")) as settings:
            self._auto_refresh = settings.get("auto_refresh", False)
            self._refresh_rate = settings.get("refresh_rate", 2)
            show_callable_attrs = settings.get("show_callable_attrs", True)
            show_special_attrs = settings.get("show_special_attrs", True)
        self._tree_model = objectbrowsertreemodel.ObjectBrowserTreeModel(
            obj, columns=self._attr_cols, show_root=False
        )
        # proxy = self._tree_model.proxifier.modify(
        #     fn=lambda x: SPECIAL_ATTR_FONT,
        #     role=constants.FONT_ROLE,
        #     selector=lambda x: x.startswith("__") and x.endswith("__"),
        #     selector_role=constants.DISPLAY_ROLE
        # )

        self._proxy_tree_model = objectbrowsertreemodel.ObjectBrowserTreeProxyModel(
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

        # Editor widget
        font = gui.Font("Courier")
        font.setFixedPitch(True)
        # font.setPointSize(14)

        self.editor = widgets.PlainTextEdit(read_only=True, font=font)
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

    def _settings_group_name(self, postfix: str) -> str:
        """Construct a group name for the persistent settings.

        Because the columns in the main table are extendible, we must store the settings
        in a different group if a different combination of columns is used. Therefore the
        settings group name contains a hash that is calculated from the used column names.
        Furthermore the window number is included in the settings group name. Finally a
        postfix string is appended.
        """
        column_names = ",".join([col.name for col in self._attr_cols])
        columns_hash = hashlib.md5(column_names.encode()).hexdigest()
        return f"{columns_hash}_win_{postfix}"

    def _write_model_settings(self):
        """Write the model settings to the persistent store."""
        new = dict(
            auto_refresh=self._auto_refresh,
            refresh_rate=self._refresh_rate,
            show_callable_attrs=self._proxy_tree_model.get_show_callables(),
            show_special_attrs=self._proxy_tree_model.get_show_special_attrs(),
        )
        settings_id = self._settings_group_name("model")
        logger.debug(f"New settings: {new}")
        with core.Settings(settings_id=settings_id) as settings:
            settings.update(new)

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
        with self.editor.edit_stylesheet() as ss:
            ss.color.setValue("black")
        try:
            # obj = tree_item.obj
            button_id = self.button_group.checkedId()
            assert button_id >= 0, "No radio button selected. Please report this bug."
            attr_details = self._attr_details[button_id]
            data = attr_details.get_label(tree_item)
            self.editor.set_text(data)
            self.editor.set_word_wrap_mode(attr_details.line_wrap)

        except Exception as ex:
            with self.editor.edit_stylesheet() as ss:
                ss.color.setValue("red")
            stack_trace = traceback.format_exc()
            self.editor.set_text(f"{ex}\n\n{stack_trace}")
            self.editor.set_wrap_mode("boundary_or_anywhere")

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
        self._write_model_settings()
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
    app = widgets.app()  # keeping reference to prevent garbage collection.
    with app.debug_mode():
        object_browser = ObjectBrowser(struct)
        object_browser.show()
        app.main_loop()
