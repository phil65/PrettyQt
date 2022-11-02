"""Object browser GUI in Qt."""


from __future__ import annotations

import hashlib
import logging
import sys
import traceback

from prettyqt import constants, core, gui, widgets
from prettyqt.objbrowser import objectbrowsertreemodel
from prettyqt.objbrowser.attribute_model import DEFAULT_ATTR_COLS, DEFAULT_ATTR_DETAILS


logger = logging.getLogger(__name__)


# It's not possible to use locals() as default for obj by taking take the locals
# from one stack frame higher; you can't know if the ObjectBrowser.__init__ was
# called directly, via the browse() wrapper or via a descendants' constructor.


class ObjectBrowser(widgets.MainWindow):
    """Object browser main application window."""

    _app = None  # Reference to the global application.
    _browsers: list[ObjectBrowser | None] = []  # Keep lists of browser windows.

    def __init__(self, obj, name: str = ""):
        super().__init__()
        self.set_title("Object browser")
        self._instance_nr = self._add_instance()
        self.set_icon("mdi.language-python")
        self._attr_cols = DEFAULT_ATTR_COLS
        self._attr_details = DEFAULT_ATTR_DETAILS

        logger.debug("Reading model settings for window: %d", self._instance_nr)
        with core.Settings(settings_id=self._settings_group_name("model")) as settings:
            self._auto_refresh = settings.get("auto_refresh", False)
            self._refresh_rate = settings.get("refresh_rate", 2)
            show_callable_attrs = settings.get("show_callable_attrs", True)
            show_special_attrs = settings.get("show_special_attrs", True)
        self._tree_model = objectbrowsertreemodel.ObjectBrowserTreeModel(
            obj, name, attr_cols=self._attr_cols
        )

        self._proxy_tree_model = objectbrowsertreemodel.ObjectBrowserTreeProxyModel(
            show_callable_attrs=show_callable_attrs,
            show_special_attrs=show_special_attrs,
        )

        self._proxy_tree_model.setSourceModel(self._tree_model)
        # self._proxy_tree_model.setSortRole(RegistryTableModel.SORT_ROLE)
        self._proxy_tree_model.setDynamicSortFilter(True)
        # self._proxy_tree_model.setSortCaseSensitivity(Qt.CaseInsensitive)

        # Views
        self._setup_actions()
        self.central_splitter = widgets.Splitter(
            parent=self, orientation=constants.VERTICAL
        )
        self.setCentralWidget(self.central_splitter)

        # Tree widget
        self.obj_tree = widgets.TreeView()
        self.obj_tree.setRootIsDecorated(True)
        self.obj_tree.setAlternatingRowColors(True)
        self.obj_tree.set_model(self._proxy_tree_model)
        self.obj_tree.set_selection_behaviour("rows")
        self.obj_tree.setUniformRowHeights(True)
        self.obj_tree.setAnimated(True)

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

        self.button_group = widgets.ButtonGroup(self)
        for button_id, attr_detail in enumerate(self._attr_details):
            radio_button = widgets.RadioButton(attr_detail.name)
            radio_widget.box.addWidget(radio_button)
            self.button_group.addButton(radio_button, button_id)

        self.button_group.buttonClicked.connect(self._change_details_field)
        self.button_group.button(0).setChecked(True)

        radio_widget.box.addStretch(1)
        group_box.box.addWidget(radio_widget)

        # Editor widget
        font = gui.Font("Courier")
        font.setFixedPitch(True)
        # font.setPointSize(14)

        self.editor = widgets.PlainTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setFont(font)
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
        close_action = widgets.Action(
            text="C&lose", callback=self.close, shortcut="Ctrl+W"
        )
        file_menu.addAction(close_action)
        exit_action = widgets.Action(
            text="E&xit",
            callback=lambda: widgets.app().closeAllWindows(),
            shortcut="Ctrl+Q",
        )
        file_menu.addAction(exit_action)

        view_menu = menubar.add_menu("&View")
        refresh_action = widgets.Action(
            text="&Refresh",
            callback=self._tree_model.refresh_tree,
            shortcut="Ctrl+R",
        )
        view_menu.addAction(refresh_action)
        view_menu.addAction(self.toggle_auto_refresh_action)

        view_menu.addSeparator()
        self.show_cols_submenu = widgets.Menu("Table columns")
        view_menu.add_menu(self.show_cols_submenu)
        actions = self.obj_tree.h_header.get_header_actions()
        self.show_cols_submenu.add_actions(actions)
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
        if self._tree_model.inspected_node_is_visible:
            self.obj_tree.expand(first_row_index)

    def _add_instance(self) -> int:
        """Adds the browser window to the list of browser references.

        If a None is present in the list it is inserted at that position, otherwise
        it is appended to the list. The index number is returned.

        This mechanism is used so that repeatedly creating and closing windows does not
        increase the instance number, which is used in writing the persistent settings.
        """
        try:
            idx = self._browsers.index(None)
        except ValueError:
            self._browsers.append(self)
            idx = len(self._browsers) - 1
        else:
            self._browsers[idx] = self

        return idx

    def _setup_actions(self):
        """Create the main window actions."""
        # Show/hide callable objects
        self.toggle_callable_action = widgets.Action(
            text="Show callable attributes",
            parent=self,
            checkable=True,
            shortcut=gui.KeySequence("Alt+C"),
            statustip="Shows/hides callable attributes (functions, methods, etc.)",
        )
        self.toggle_callable_action.toggled.connect(
            self._proxy_tree_model.set_show_callables
        )

        # Show/hide special attributes
        self.toggle_special_attribute_action = widgets.Action(
            text="Show __special__ attributes",
            parent=self,
            checkable=True,
            shortcut=gui.KeySequence("Alt+S"),
            statustip="Shows or hides __special__ attributes",
        )
        self.toggle_special_attribute_action.toggled.connect(
            self._proxy_tree_model.set_show_special_attrs
        )

        # Toggle auto-refresh on/off
        self.toggle_auto_refresh_action = widgets.Action(
            text="Auto-refresh",
            parent=self,
            checkable=True,
            statustip=f"Auto refresh every {self._refresh_rate} seconds",
        )
        self.toggle_auto_refresh_action.toggled.connect(self.toggle_auto_refresh)

        # Add another refresh action with a different shortcut. An action must be added to
        # a visible widget for it to receive events. It is added to the main windows to
        # prevent it from being displayed again in the menu
        self.refresh_action_f5 = widgets.Action(self, text="&Refresh2", shortcut="F5")
        self.refresh_action_f5.triggered.connect(self._tree_model.refresh_tree)
        self.addAction(self.refresh_action_f5)

    def _settings_group_name(self, postfix: str) -> str:
        """Construct a group name for the persistent settings.

        Because the columns in the main table are extendible, we must store the settings
        in a different group if a different combination of columns is used. Therefore the
        settings group name contains a hash that is calculated from the used column names.
        Furthermore the window number is included in the settings group name. Finally a
        postfix string is appended.
        """
        column_names = ",".join([col.name for col in self._attr_cols])
        columns_hash = hashlib.md5(column_names.encode("utf-8")).hexdigest()
        return f"{columns_hash}_win{self._instance_nr}_{postfix}"

    def _write_model_settings(self):
        """Write the model settings to the persistent store."""
        logger.debug("Writing model settings for window: %d", self._instance_nr)
        new = dict(
            auto_refresh=self._auto_refresh,
            refresh_rate=self._refresh_rate,
            show_callable_attrs=self._proxy_tree_model.get_show_callables(),
            show_special_attrs=self._proxy_tree_model.get_show_special_attrs(),
        )
        settings_id = self._settings_group_name("model")
        logger.debug(f"New settings: {new}")
        with core.Settings(settings_id=settings_id) as settings:
            settings.set_values(new)

    @core.Slot(core.ModelIndex, core.ModelIndex)
    def _update_details(
        self, current_index: core.ModelIndex, _previous_index: core.ModelIndex
    ):
        """Show the object details in the editor given an index."""
        tree_item = self._proxy_tree_model.tree_item(current_index)
        self._update_details_for_item(tree_item)

    def _change_details_field(self, _button_id=None):
        """Change the field that is displayed in the details pane."""
        # logger.debug("_change_details_field: {}".format(_button_id))
        current_index = self.obj_tree.selectionModel().currentIndex()
        tree_item = self._proxy_tree_model.tree_item(current_index)
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
        """Set the reference in the browser list to None."""
        idx = self._browsers.index(self)
        self._browsers[idx] = None
        logger.debug("Closed window %s", self._instance_nr)

    @classmethod
    def browse(cls, *args, **kwargs):
        """Create and run object browser.

        For this, the following three steps are done:
        1) Create QApplication object if it doesn't yet exist
        2) Create and show an ObjectBrowser window
        3) Start the Qt event loop.

        The *args and **kwargs will be passed to the ObjectBrowser constructor.
        """
        cls.app = widgets.app()  # keeping reference to prevent garbage collection.
        cls.app.setOrganizationName("phil65")
        cls.app.setApplicationName("PrettyQt")
        object_browser = cls(*args, **kwargs)
        object_browser.show()
        object_browser.raise_()
        return cls.app.main_loop()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    struct = dict(a={1, 2, frozenset([1, 2])})
    app = widgets.app()  # keeping reference to prevent garbage collection.
    app.setOrganizationName("phil65")
    app.setApplicationName("PrettyQt")
    object_browser = ObjectBrowser(struct)
    object_browser.show()
    app.main_loop()
