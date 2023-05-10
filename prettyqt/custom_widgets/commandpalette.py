from __future__ import annotations

import logging

from prettyqt import constants, core, custom_delegates, custom_models, gui, widgets
from prettyqt.custom_models import actionsmodel
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import fuzzy


logger = logging.getLogger(__name__)
MATCH_COLOR = "blue"
DISABLED_COLOR = "gray"


class CommandPaletteModel(custom_models.ColumnTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_marker_text = ""

    def set_current_marker_text(self, text: str):
        with self.reset_model():
            self.current_marker_text = text

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        action = self.data_by_index(index)
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                label = action.text()
                return (
                    color_text(self.current_marker_text, label)
                    if self.current_marker_text
                    else label
                )
            # case constants.DISPLAY_ROLE, 1:
            #     label = action.text()
            #     result = fuzzy.fuzzy_match(self.current_marker_text, label)
            #     return str(result[1])
            case constants.SORT_ROLE, _:
                label = action.text()
                result = fuzzy.fuzzy_match(self.current_marker_text, label)
                return result[1]
            case _, _:
                return super().data(index, role)


def bold_colored(text: str, color: str) -> str:
    return f"<b><font color={color!r}>{text}</font></b>"


def colored(text: str, color: str) -> str:
    return f"<font color={color!r}>{text}</font>"


def color_text(
    input_text: str, text: str, case_sensitive: bool = False, color=MATCH_COLOR
):
    def converter(x):
        return x if case_sensitive else x.lower()

    output_text = ""
    for char in text:
        if input_text and converter(char) == converter(input_text[0]):
            output_text += bold_colored(char, color)
            input_text = input_text[1:]
        else:
            output_text += char
    return output_text


class CommandTable(widgets.TableView):
    action_clicked = core.Signal(int)

    def __init__(self, parent: widgets.Widget | None = None) -> None:
        super().__init__(parent)
        self.set_cursor("pointing_hand")
        columns = actionsmodel.COLUMNS
        self._model = CommandPaletteModel([], columns, parent=self)
        self._proxy = custom_models.FuzzyFilterModel()
        self._proxy.set_filter_case_sensitive(False)
        self._proxy.set_sort_role(constants.SORT_ROLE)
        self._proxy.setSourceModel(self._model)
        self.setModel(self._proxy)
        self.set_selection_mode("single")
        self.set_selection_behaviour("rows")
        self.setSortingEnabled(True)
        self.pressed.connect(self._on_clicked)
        self.set_delegate(custom_delegates.HtmlItemDelegate())
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


class PaletteLineEdit(widgets.LineEdit):
    def keyPressEvent(self, e: core.Event):
        if e.modifiers() in (
            QtCore.Qt.KeyboardModifier.NoModifier,
            QtCore.Qt.KeyboardModifier.KeypadModifier,
        ):
            match e.key():
                case QtCore.Qt.Key.Key_Escape:
                    self.parent().hide()
                    return
                case QtCore.Qt.Key.Key_Return:
                    self.parent().hide()
                    self.parent()._table.execute_focused()
                    return
                case QtCore.Qt.Key.Key_Up:
                    self.parent()._table.move_row_selection(-1)
                    return
                case QtCore.Qt.Key.Key_Down:
                    self.parent()._table.move_row_selection(1)
                    return
        return super().keyPressEvent(e)


class CommandPalette(widgets.Widget):
    """A Qt command palette widget."""

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)
        # self.setWindowFlags(
        #     QtCore.Qt.WindowType.WindowStaysOnTopHint
        #     | QtCore.Qt.WindowType.FramelessWindowHint
        # )
        self._line = PaletteLineEdit()
        self._table = CommandTable()
        self._line.value_changed.connect(self._table._model.set_current_marker_text)
        # self._line.value_changed.connect(self._table.select_first_row)
        self._line.value_changed.connect(self._table._proxy.set_search_term)
        layout = widgets.BoxLayout("vertical", self)
        layout.addWidget(self._line)
        layout.addWidget(self._table)
        self.setLayout(layout)
        self.add_shortcut("Ctrl+P", self.close)

        # self._line.textChanged.connect(self._on_text_changed)
        # self._table.action_clicked.connect(self._on_action_clicked)
        self._line.editingFinished.connect(self.hide)

    def populate_from_widget(self, widget):
        self.add_actions(widget.actions())
        while parent := widget.parent():
            self.add_actions(parent.actions())

    def match_color(self) -> str:
        """The color used for the matched characters."""
        return self._table.matchColor

    def set_match_color(self, color):
        """Set the color used for the matched characters."""
        self._table.matchColor = QtGui.QColor(color)

    def install_to(self, parent: widgets.Widget):
        self.setParent(parent, QtCore.Qt.WindowType.SubWindow)
        self.hide()

    # def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
    #     self.hide()
    #     return super().focusOutEvent(a0)

    def add_actions(self, actions: list[QtGui.QAction]):
        self._table._model.add_items(actions)
        self._table.select_first_row()

    def show(self):
        self._line.setText("")
        self.resize(500, 300)
        self.center()
        super().show()
        # if parent := self.parentWidget():
        #     parent_rect = parent.rect()
        #     self_size = self.size()
        #     w = min(int(parent_rect.width() * 0.8), self_size.width())
        #     topleft = parent.rect().topLeft()
        #     topleft.setX(int(topleft.x() + (parent_rect.width() - w) / 2))
        #     topleft.setY(int(topleft.y() + 3))
        #     self.move(topleft)
        #     self.resize(w, self_size.height())

        self.raise_()
        self._line.setFocus()

    # def show_center(self):
    #     """Show command palette widget in the center of the screen."""
    #     self._line.setText("")
    #     # self._table.update_for_text("")
    #     self.setWindowFlags(
    #         QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.FramelessWindowHint
    #     )
    #     super().show()

    #     screen_rect = gui.GuiApplication.primaryScreen().geometry()
    #     self.resize(
    #         int(screen_rect.width() * 0.5),
    #         int(screen_rect.height() * 0.5),
    #     )
    #     point = screen_rect.center() - self.rect().center()
    #     self.move(point)

    #     self.raise_()
    #     self._line.setFocus()


if __name__ == "__main__":
    app = widgets.app()
    window = widgets.MainWindow()
    window.setCentralWidget(widgets.Label("Press Ctrl+P"))
    window.addAction(
        gui.Action(text="MainWindowAction", parent=window, callback=window.close)
    )
    pal = CommandPalette()
    window.add_shortcut("Ctrl+P", pal.show)
    actions = [
        gui.Action(
            text="super duper action",
            shortcut="Ctrl+A",
            tooltip="some Tooltip text",
            icon="mdi.folder",
            callback=lambda: print("test"),
        ),
        gui.Action(
            text="this is an action",
            shortcut="Ctrl+B",
            tooltip="Tooltip",
            icon="mdi.folder-outline",
            checked=True,
            checkable=True,
        ),
        gui.Action(
            text="another one P",
            shortcut="Ctrl+Alt+A",
            tooltip="Some longer tooltiPpp",
            icon="mdi.folder",
        ),
        gui.Action(
            text="another onpe P",
            shortcut="Ctrl+Alt+A",
            tooltip="Some longer tooltiPpp",
            icon="mdi.folder",
        ),
        gui.Action(text="a", shortcut="Ctrl+A", tooltip="Tooltip", icon="mdi.folder"),
    ]
    pal.populate_from_widget(window)
    print(window.actions())
    pal.add_actions(actions)
    window.show()
    app.main_loop()
