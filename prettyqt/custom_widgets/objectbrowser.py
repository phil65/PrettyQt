"""Object browser GUI in Qt."""


from __future__ import annotations

import logging

from prettyqt import constants, core, custom_models, custom_widgets,  gui, widgets
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


class ObjectBrowser(widgets.MainWindow):
    """Object browser main application window."""

    def __init__(self, obj, stack=None, name: str = ""):
        super().__init__()
        self.set_title("Object browser")
        self.set_icon("mdi.language-python")
        self._auto_refresh = False
        self._refresh_rate = 2
        self._tree_model = custom_models.PythonObjectTreeModel(obj)
        self._attr_details = [
            Klass(model=self._tree_model) for Klass in DEFAULT_ATTR_DETAILS
        ]


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
        self.obj_tree.set_model(self._tree_model)
        self.obj_tree.h_header = custom_widgets.FilterHeader(self.obj_tree)

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
        selection_model.currentRowChanged.connect(self._update_details)
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

        assert self._refresh_rate > 0
        self._refresh_timer = core.Timer(self)
        self._refresh_timer.setInterval(self._refresh_rate * 1000)
        self._refresh_timer.timeout.connect(self._tree_model.refresh_tree)
        self.toggle_auto_refresh_action.setChecked(self._auto_refresh)

    @core.Slot(core.ModelIndex, core.ModelIndex)
    def _update_details(
        self, current_index: core.ModelIndex, _previous_index: core.ModelIndex
    ):
        """Show the object details in the editor given an index."""
        if self.obj_tree.model() is None:
            return
        role = self.obj_tree.get_model(skip_proxies=True).TreeItemRole
        tree_item = current_index.data(role)
        self._update_details_for_item(tree_item)

    def _change_details_field(self, _button_id=None):
        """Change the field that is displayed in the details pane."""
        # logger.debug("_change_details_field: {}".format(_button_id))
        if self.obj_tree.get_model(skip_proxies=True) is None:
            return
        current_index = self.obj_tree.selectionModel().currentIndex()
        role = self.obj_tree.get_model(skip_proxies=True).TreeItemRole
        tree_item = current_index.data(role)
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
        self._refresh_timer.stop()
        self._refresh_timer.timeout.disconnect(self._tree_model.refresh_tree)
        self.toggle_auto_refresh_action.toggled.disconnect(self.toggle_auto_refresh)
        self.refresh_action_f5.triggered.disconnect(self._tree_model.refresh_tree)
        self.button_group.buttonClicked.disconnect(self._change_details_field)
        selection_model = self.obj_tree.selectionModel()
        selection_model.currentRowChanged.disconnect(self._update_details)
        self.close()
        event.accept()


if __name__ == "__main__":
    struct = dict(a={1, 2, frozenset([1, 2])})
    app = widgets.app()
    with app.debug_mode():
        object_browser = ObjectBrowser(struct)
        object_browser.show()
        app.main_loop()
