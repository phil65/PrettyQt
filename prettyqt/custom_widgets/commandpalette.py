from __future__ import annotations

import collections

from collections.abc import Sequence
import logging
import pathlib

from prettyqt import constants, core, gui, itemmodels, widgets
from prettyqt.utils import colors, datatypes


logger = logging.getLogger(__name__)

COMMANDS = collections.defaultdict(list)


class CommandGroup:
    def __init__(self, group_name: str):
        self.group_name = group_name

    def register(
        self, text: str, icon: datatypes.IconType | None = None, shortcut: str = ""
    ):
        def decorator(fn):
            COMMANDS[self.group_name].append((text, icon, shortcut, fn))
            return fn

        return decorator


class CommandTable(widgets.TableView):
    """TableView showing a Command Palette."""

    action_clicked = core.Signal(int)

    def __init__(self, parent: widgets.Widget | None = None) -> None:
        super().__init__(
            parent,
            selection_mode="single",
            selection_behavior="rows",
            sorting_enabled=True,
        )
        # self.set_cursor("pointing_hand")
        self._model = itemmodels.ActionsModel([], parent=self)
        self._proxy = itemmodels.FuzzyFilterProxyModel(
            filter_key_column=0, invalidated=self.select_first_row
        )
        self._proxy.set_filter_case_sensitive(False)
        # self._proxy.set_sort_role(constants.SORT_ROLE)
        self._proxy.setSourceModel(self._model)
        self.setModel(self._proxy)
        self.h_header.set_resize_mode("stretch")
        self.pressed.connect(self._on_clicked)
        self.set_delegate("html", column=0)
        self._match_color = gui.QColor("#468cc6")
        self.setShowGrid(False)

    @core.Property(gui.QColor)
    def matchColor(self) -> gui.QColor:
        return self._match_color

    @matchColor.setter
    def matchColor(self, color: gui.QColor):
        self._match_color = color

    def _on_clicked(self, index: core.ModelIndex) -> None:
        if index.isValid():
            role = self._model.ExtraRoles.TreeItemRole
            data = index.data(role)
            data.trigger()

    def execute_focused(self):
        fn = self.current_data()
        fn.trigger()


class CommandPalette(widgets.Widget):
    """A Qt command palette widget."""

    def __init__(self, parent: widgets.QWidget | None = None):
        super().__init__(parent=parent)
        self.setWindowFlags(
            constants.WindowType.WindowStaysOnTopHint
            | constants.WindowType.FramelessWindowHint
            # | constants.WindowType.ToolTip
        )
        self.set_focus_policy("strong")
        self.setMinimumWidth(700)
        self._line = widgets.LineEdit()
        self.setFocusProxy(self._line)
        self._table = CommandTable()
        # self._line.value_changed.connect(self._table.select_first_row)
        self._line.value_changed.connect(self._table._proxy.set_search_term)
        layout = self.set_layout("vertical")
        layout.addWidget(self._line)
        layout.addWidget(self._table)
        self.add_shortcut("Ctrl+P", self.close)
        self._line.installEventFilter(self)

        # self._line.textChanged.connect(self._on_text_changed)
        # self._table.action_clicked.connect(self._on_action_clicked)
        # self._line.editingFinished.connect(self.hide)

    def eventFilter(self, source: core.QObject, e: core.QEvent) -> bool:
        if source != self._line or e.type() != core.QEvent.Type.KeyPress:
            return super().eventFilter(source, e)
        if e.modifiers() in (
            constants.KeyboardModifier.NoModifier,
            constants.KeyboardModifier.KeypadModifier,
        ):
            match e.key():
                case constants.Key.Key_Escape:
                    self.hide()
                    return True
                case constants.Key.Key_Return:
                    self.hide()
                    self._table.execute_focused()
                    return True
                case constants.Key.Key_Up:
                    self._table.move_row_selection(-1)
                    return True
                case constants.Key.Key_Down:
                    self._table.move_row_selection(1)
                    return True
        return super().eventFilter(source, e)

    def populate_from_widget(self, widget: widgets.QWidget):
        self.add_actions(widget.actions())
        if not callable(widget.parent):
            return
        while widget := widget.parent():
            self.add_actions(widget.actions())

    def add_path_actions(self, path):
        path = pathlib.Path(path)
        actions = [gui.Action(str(p)) for p in path.rglob("*") if p.is_file()]
        self.add_actions(actions)

    def match_color(self) -> str:
        """The color used for the matched characters."""
        return self._table.match_color

    def set_match_color(self, color):
        """Set the color used for the matched characters."""
        self._table.match_color = colors.get_color(color).name()

    def install_to(self, parent: widgets.Widget):
        self.setParent(parent, constants.WindowType.SubWindow)
        self.hide()

    # def focusOutEvent(self, a0: gui.QFocusEvent) -> None:
    #     self.hide()
    #     return super().focusOutEvent(a0)

    def add_actions(self, actions: Sequence[gui.QAction]):
        self._table._model.add_items(actions)

    def show(self):
        self._line.setText("")
        self.resize(1000, 300)
        self.position_on("screen")
        super().show()
        self.raise_()
        self._line.setFocus()


if __name__ == "__main__":
    import random
    import string

    app = widgets.app()
    window = widgets.MainWindow()
    window.setCentralWidget(widgets.Label("Press Ctrl+P"))
    window.add_action(text="MainWindowAction", parent=window, triggered=window.close)
    pal = CommandPalette()
    window.add_shortcut("Ctrl+P", pal.show)
    actions = [
        gui.Action(
            text="super duper action",
            shortcut="Ctrl+A",
            tool_tip="some Tooltip text",
            icon="mdi.folder",
            triggered=lambda: print("test"),
        ),
        gui.Action(
            text="this is an action",
            shortcut="Ctrl+B",
            tool_tip="Tooltip",
            icon="mdi.folder-outline",
            checked=True,
            checkable=True,
        ),
        gui.Action(
            text="another one P",
            shortcut="Ctrl+Alt+A",
            tool_tip="Some longer tooltiPpp",
            icon="mdi.folder",
        ),
        gui.Action(
            text="another onpe P",
            shortcut="Ctrl+Alt+A",
            tool_tip="Some longer tooltiPpp",
            icon="mdi.folder",
        ),
        gui.Action(text="a", shortcut="Ctrl+A", tool_tip="Tooltip", icon="mdi.folder"),
    ]
    pal.populate_from_widget(window)
    pal.add_actions(actions)
    for _ in range(1000):
        label = "".join(random.choices(string.ascii_uppercase, k=10))
        pal.add_actions([gui.Action(text=label)])
    window.show()
    with app.debug_mode():
        app.exec()
