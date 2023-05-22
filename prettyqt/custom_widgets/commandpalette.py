from __future__ import annotations

import collections
from collections.abc import Sequence
import logging

from prettyqt import constants, core, custom_delegates, custom_models, gui, widgets
from prettyqt.custom_models import actionsmodel
from prettyqt.qt import QtCore, QtGui, QtWidgets
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
    action_clicked = core.Signal(int)

    def __init__(self, parent: widgets.Widget | None = None) -> None:
        super().__init__(
            parent,
            selection_mode="single",
            selection_behavior="rows",
            sorting_enabled=True,
        )
        # self.set_cursor("pointing_hand")
        self._model = custom_models.ColumnTableModel(
            [], actionsmodel.COLUMNS, parent=self
        )
        self._proxy = custom_models.FuzzyFilterProxyModel(filter_key_column=0)
        self._proxy.set_filter_case_sensitive(False)
        # self._proxy.set_sort_role(constants.SORT_ROLE)
        self._proxy.setSourceModel(self._model)
        self._proxy.invalidated.connect(self.select_first_row)
        self.setModel(self._proxy)
        self.h_header.set_resize_mode("stretch")
        self.pressed.connect(self._on_clicked)
        self.set_delegate(custom_delegates.HtmlItemDelegate(), column=0)
        self._match_color = QtGui.QColor("#468cc6")

    @core.Property(QtGui.QColor)
    def matchColor(self) -> QtGui.QColor:
        return self._match_color

    @matchColor.setter
    def matchColor(self, color: QtGui.QColor):
        self._match_color = color

    def _on_clicked(self, index: core.ModelIndex) -> None:
        if index.isValid():
            data = index.data(constants.USER_ROLE)
            data.trigger()

    def execute_focused(self):
        fn = self.current_data()
        fn.trigger()


class CommandPalette(widgets.Widget):
    """A Qt command palette widget."""

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.FramelessWindowHint
            # | QtCore.Qt.WindowType.ToolTip
        )
        self.set_focus_policy("strong")
        self.setMinimumWidth(700)
        self._line = widgets.LineEdit()
        self._table = CommandTable()
        # self._line.value_changed.connect(self._table.select_first_row)
        self._line.value_changed.connect(self._table._proxy.set_search_term)
        layout = widgets.VBoxLayout(self)
        layout.addWidget(self._line)
        layout.addWidget(self._table)
        self.setLayout(layout)
        self.add_shortcut("Ctrl+P", self.close)
        self._line.installEventFilter(self)

        # self._line.textChanged.connect(self._on_text_changed)
        # self._table.action_clicked.connect(self._on_action_clicked)
        # self._line.editingFinished.connect(self.hide)

    def eventFilter(self, source: QtCore.QObject, e: QtCore.QEvent) -> bool:
        if source != self._line or e.type() != QtCore.QEvent.Type.KeyPress:
            return super().eventFilter(source, e)
        if e.modifiers() in (
            QtCore.Qt.KeyboardModifier.NoModifier,
            QtCore.Qt.KeyboardModifier.KeypadModifier,
        ):
            match e.key():
                case QtCore.Qt.Key.Key_Escape:
                    self.hide()
                    return True
                case QtCore.Qt.Key.Key_Return:
                    self.hide()
                    self._table.execute_focused()
                    return True
                case QtCore.Qt.Key.Key_Up:
                    self._table.move_row_selection(-1)
                    return True
                case QtCore.Qt.Key.Key_Down:
                    self._table.move_row_selection(1)
                    return True
        return super().eventFilter(source, e)

    def populate_from_widget(self, widget: QtWidgets.QWidget):
        self.add_actions(widget.actions())
        if not callable(widget.parent):
            return
        while widget := widget.parent():
            self.add_actions(widget.actions())

    def match_color(self) -> str:
        """The color used for the matched characters."""
        return self._table.match_color

    def set_match_color(self, color):
        """Set the color used for the matched characters."""
        self._table.match_color = colors.get_color(color).name()

    def install_to(self, parent: widgets.Widget):
        self.setParent(parent, QtCore.Qt.WindowType.SubWindow)
        self.hide()

    # def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
    #     self.hide()
    #     return super().focusOutEvent(a0)

    def add_actions(self, actions: Sequence[QtGui.QAction]):
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
    print(window.actions())
    pal.add_actions(actions)
    for _ in range(1000):
        label = "".join(random.choices(string.ascii_uppercase, k=10))
        pal.add_actions([gui.Action(text=label)])
    window.show()
    print(COMMANDS)
    with app.debug_mode():
        app.main_loop()
