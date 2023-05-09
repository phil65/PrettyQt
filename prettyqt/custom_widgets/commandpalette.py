from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
import logging
import re
from typing import Any, Generic, TypeVar

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


logger = logging.getLogger(__name__)
MATCH_COLOR = "blue"
DISABLED_COLOR = "gray"


def bold_colored(text: str, color: str) -> str:
    return f"<b><font color={color!r}>{text}</font></b>"


def colored(text: str, color: str) -> str:
    return f"<font color={color!r}>{text}</font>"


class CommandMatchModel(core.AbstractListModel):
    """A list model for the command palette."""

    def __init__(self, parent: widgets.Widget = None):
        super().__init__(parent)
        self._commands: list[Command] = []
        self._max_matches = 80

    def rowCount(self, parent: core.ModelIndex = None) -> int:
        return self._max_matches

    def data(self, index: core.ModelIndex, role: int = constants.DISPLAY_ROLE) -> Any:
        return None

    def flags(self, index: core.ModelIndex) -> QtCore.Qt.ItemFlag:
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable


class CommandLabel(widgets.Label):
    """The label widget to display a command in the palette."""

    def __init__(self, cmd: Command | None = None):
        super().__init__()
        if cmd is not None:
            self.set_command(cmd)
        else:
            self._command_text = ""

    def command(self) -> Command:
        """Command bound to this label."""
        return self._command

    def set_command(self, cmd: Command) -> None:
        """Set command to this widget."""
        command_text = cmd.fmt()
        self._command_text = command_text
        self._command = cmd
        self.setText(command_text)
        self.setToolTip(cmd.tooltip)

    def command_text(self) -> str:
        """The original command text."""
        return self._command_text

    def set_text_colors(self, input_text: str, /, color: str = MATCH_COLOR):
        """Set label text color based on the input text."""
        if not input_text:
            return None
        text = self.command_text()
        words = input_text.split(" ")
        pattern = re.compile("|".join(words), re.IGNORECASE)

        output_text = ""
        last_end = 0
        for match_obj in pattern.finditer(text):
            output_text += text[last_end : match_obj.start()]
            word = match_obj.group()
            output_text += bold_colored(word, color)
            last_end = match_obj.end()
        output_text += text[last_end:]

        self.setText(output_text)

    def set_disabled(self) -> None:
        """Set the label to disabled."""
        text = self.command_text()
        self.setText(colored(text, DISABLED_COLOR))


class CommandList(widgets.ListView):
    command_clicked = core.Signal(int)  # one of the items is clicked

    def __init__(self, parent: widgets.Widget | None = None) -> None:
        super().__init__(parent)
        self.set_cursor("pointing_hand")
        self.setModel(CommandMatchModel(self))
        self.set_selection_mode(None)
        self._selected_index = 0
        self._label_widgets: list[CommandLabel] = []
        self._current_max_index = 0
        for i in range(self.model()._max_matches):
            lw = CommandLabel()
            self._label_widgets.append(lw)
            self.setIndexWidget(self.model().index(i), lw)
        self.pressed.connect(self._on_clicked)

        self._match_color = QtGui.QColor("#468cc6")

    @core.Property(QtGui.QColor)
    def matchColor(self) -> QtGui.QColor:
        return self._match_color

    @matchColor.setter
    def matchColor(self, color: QtGui.QColor):
        self._match_color = color

    def _on_clicked(self, index: core.ModelIndex) -> None:
        if index.isValid():
            self.command_clicked.emit(index.row())

    def move_selection(self, dx: int) -> None:
        self._selected_index += dx
        self._selected_index = max(0, self._selected_index)
        self._selected_index = min(self._current_max_index - 1, self._selected_index)
        self.update_selection()

    def update_selection(self):
        index = self.model().index(self._selected_index)
        self.selectionModel().setCurrentIndex(
            index, core.ItemSelectionModel.SelectionFlag.ClearAndSelect
        )

    @property
    def all_commands(self) -> list[Command]:
        return self.model()._commands

    def add_command(self, command: Command) -> None:
        self.all_commands.append(command)

    def extend_command(self, commands: list[Command]) -> None:
        """Extend the list of commands."""
        self.all_commands.extend(commands)

    def clear_commands(self) -> None:
        """Clear all the command."""
        return self.all_commands.clear()

    def command_at(self, index: int) -> Command:
        return self.indexWidget(self.model().index(index)).command()

    def set_command_at(self, index: int, cmd: Command) -> None:
        self.indexWidget(self.model().index(index)).set_command(cmd)

    def iter_command(self) -> Iterator[Command]:
        for i in range(self.model().rowCount()):
            if not self.isRowHidden(i):
                yield self.command_at(i)

    def execute(self, index: int | None = None) -> None:
        """Execute the currently selected command."""
        if index is None:
            index = self._selected_index
        cmd = self.command_at(index)
        logger.debug(f"executing command: {cmd.fmt()}")
        cmd(self.parent())
        # move to the top
        self.all_commands.remove(cmd)
        self.all_commands.insert(0, cmd)

    def can_execute(self, index: int | None = None) -> bool:
        if index is None:
            index = self._selected_index
        cmd = self.command_at(index)
        return cmd.enabled()

    def update_for_text(self, input_text: str) -> None:
        """Update the list to match the input text."""
        self._selected_index = 0
        max_matches = self.model()._max_matches
        row = 0
        for cmd in self.all_commands:
            if cmd.matches(input_text):
                self.setRowHidden(row, False)
                lw = self.indexWidget(self.model().index(row))
                lw.set_command(cmd)
                if cmd.enabled():
                    lw.set_text_colors(input_text, color=self.matchColor.name())
                else:
                    lw.set_disabled()
                row += 1

                if row >= max_matches:
                    self._current_max_index = max_matches
                    break
        else:
            self._current_max_index = row
            for row_to_hide in range(row, max_matches):
                self.setRowHidden(row_to_hide, True)
        self.update_selection()
        self.update()


_R = TypeVar("_R")


@dataclass
class Command(Generic[_R]):
    """A command representation."""

    function: Callable[..., _R]
    title: str
    desc: str
    tooltip: str = ""
    when: Callable[..., bool] = field(default=lambda: True)

    def __call__(self, *args, **kwargs) -> _R:
        return self.function(*args, **kwargs)

    def fmt(self) -> str:
        """Format command for display in the palette."""
        return f"{self.title}: {self.desc}" if self.title else self.desc

    def matches(self, input_text: str) -> bool:
        """Return True if the command matches the input text."""
        fmt = self.fmt().lower()
        words = input_text.lower().split(" ")
        return all(word in fmt for word in words)

    def enabled(self) -> bool:
        """Return True if the command is enabled."""
        return self.when()


class CommandLineEdit(widgets.LineEdit):
    """The line edit used in command palette widget."""

    def commandPalette(self) -> CommandPalette:
        """The parent command palette widget."""
        return self.parent()

    def keyPressEvent(self, e: core.Event):
        if e.modifiers() in (
            QtCore.Qt.KeyboardModifier.NoModifier,
            QtCore.Qt.KeyboardModifier.KeypadModifier,
        ):
            match e.key():
                case QtCore.Qt.Key.Key_Escape:
                    self.commandPalette().hide()
                    return
                case QtCore.Qt.Key.Key_Return:
                    palette = self.commandPalette()
                    if not palette._list.can_execute():
                        return
                    self.commandPalette().hide()
                    self.commandPalette()._list.execute()
                    return
                case QtCore.Qt.Key.Key_Up:
                    self.commandPalette()._list.move_selection(-1)
                    return
                case QtCore.Qt.Key.Key_Down:
                    self.commandPalette()._list.move_selection(1)
                    return
        return super().keyPressEvent(e)


class CommandPalette(widgets.Widget):
    """A Qt command palette widget."""

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self._line = CommandLineEdit()
        self._list = CommandList()
        _layout = widgets.BoxLayout("vertical", self)
        _layout.addWidget(self._line)
        _layout.addWidget(self._list)
        self.setLayout(_layout)

        self._line.textChanged.connect(self._on_text_changed)
        self._list.command_clicked.connect(self._on_command_clicked)
        self._line.editingFinished.connect(self.hide)

    def match_color(self) -> str:
        """The color used for the matched characters."""
        return self._list.matchColor

    def set_match_color(self, color):
        """Set the color used for the matched characters."""
        self._list.matchColor = QtGui.QColor(color)

    def add_command(self, cmd: Command):
        self._list.add_command(cmd)
        return None

    def extend_command(self, list_of_commands: list[Command]):
        self._list.extend_command(list_of_commands)
        return None

    def clear_commands(self):
        self._list.clear_commands()
        return None

    def install_to(self, parent: widgets.Widget):
        self.setParent(parent, QtCore.Qt.WindowType.SubWindow)
        self.hide()

    def _on_text_changed(self, text: str):
        self._list.update_for_text(text)
        return None

    def _on_command_clicked(self, index: int):
        self._list.execute(index)
        self.hide()
        return None

    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.hide()
        return super().focusOutEvent(a0)

    def show(self):
        self._line.setText("")
        self._list.update_for_text("")
        super().show()
        if parent := self.parentWidget():
            parent_rect = parent.rect()
            self_size = self.size()
            w = min(int(parent_rect.width() * 0.8), self_size.width())
            topleft = parent.rect().topLeft()
            topleft.setX(int(topleft.x() + (parent_rect.width() - w) / 2))
            topleft.setY(int(topleft.y() + 3))
            self.move(topleft)
            self.resize(w, self_size.height())

        self.raise_()
        self._line.setFocus()

    def show_center(self):
        """Show command palette widget in the center of the screen."""
        self._line.setText("")
        self._list.update_for_text("")
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.FramelessWindowHint
        )
        super().show()

        screen_rect = gui.GuiApplication.primaryScreen().geometry()
        self.resize(
            int(screen_rect.width() * 0.5),
            int(screen_rect.height() * 0.5),
        )
        point = screen_rect.center() - self.rect().center()
        self.move(point)

        self.raise_()
        self._line.setFocus()


if __name__ == "__main__":
    app = widgets.app()
    pal = CommandPalette()
    cmd = Command(function=lambda x: print("test"), title="title", desc="desc")
    cmd2 = Command(function=lambda x: print("test2"), title="title2", desc="desc2")
    pal.add_command(cmd)
    pal.add_command(cmd2)
    pal.show()
    app.main_loop()
