from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


ECHO_MODE = bidict(
    normal=QtWidgets.QLineEdit.EchoMode.Normal,
    no_echo=QtWidgets.QLineEdit.EchoMode.NoEcho,
    password=QtWidgets.QLineEdit.EchoMode.Password,
    echo_on_edit=QtWidgets.QLineEdit.EchoMode.PasswordEchoOnEdit,
)

EchoModeStr = Literal["normal", "no_echo", "password", "echo_on_edit"]

ACTION_POSITION = bidict(
    leading=QtWidgets.QLineEdit.ActionPosition.LeadingPosition,
    trailing=QtWidgets.QLineEdit.ActionPosition.TrailingPosition,
)

ActionPositionStr = Literal["leading", "trailing"]

QtWidgets.QLineEdit.__bases__ = (widgets.Widget,)


class LineEdit(QtWidgets.QLineEdit):
    focusLost = core.Signal()
    enterPressed = core.Signal()
    editComplete = core.Signal(str)

    value_changed = core.Signal(str)

    def __init__(
        self,
        default_value: str = "",
        read_only: bool = False,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(default_value, parent)
        self.textChanged.connect(self._set_validation_color)
        self.textChanged.connect(self.value_changed)
        self.set_read_only(read_only)

    def __repr__(self):
        return f"{type(self).__name__}: {self.serialize_fields()}"

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_text(state["text"])
        self.setValidator(state["validator"])
        self.setInputMask(state["input_mask"])
        self.setMaxLength(state["max_length"])
        self.setPlaceholderText(state["placeholder_text"])
        self.setReadOnly(state["read_only"])
        self.setFrame(state["has_frame"])
        self.setClearButtonEnabled(state["clear_button_enabled"])
        # self.setAlignment(state["alignment"])
        self.set_cursor_move_style(state["cursor_move_style"])
        self.set_echo_mode(state["echo_mode"])
        self.setCursorPosition(state["cursor_position"])
        self.setDragEnabled(state["drag_enabled"])
        self.setModified(state["is_modified"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: str):
        self.append_text(other)
        return self

    def serialize_fields(self):
        return dict(
            text=self.text(),
            # alignment=self.alignment(),
            validator=self.validator(),
            max_length=self.maxLength(),
            read_only=self.isReadOnly(),
            input_mask=self.inputMask(),
            has_frame=self.hasFrame(),
            placeholder_text=self.placeholderText(),
            clear_button_enabled=self.isClearButtonEnabled(),
            cursor_move_style=self.get_cursor_move_style(),
            echo_mode=self.get_echo_mode(),
            cursor_position=self.cursorPosition(),
            drag_enabled=self.dragEnabled(),
            is_modified=self.isModified(),
        )

    def focusOutEvent(self, event):
        self.focusLost.emit()
        return super().focusOutEvent(event)

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key.Key_Enter, QtCore.Qt.Key.Key_Return]:
            self.enterPressed.emit()
        return super().keyPressEvent(event)

    def _on_edit_complete(self):
        self.editComplete.emit(self.text())

    def font(self) -> gui.Font:
        return gui.Font(super().font())

    def append_text(self, text: str):
        self.set_text(self.text() + text)

    def set_text(self, text: str):
        self.setText(text)

    def set_read_only(self, value: bool = True):
        """Set text to read-only.

        Args:
            value: True, for read-only, otherwise False
        """
        self.setReadOnly(value)

    def set_regex_validator(self, regex: str, flags=0) -> gui.RegularExpressionValidator:
        validator = gui.RegularExpressionValidator(self)
        validator.set_regex(regex, flags)
        self.set_validator(validator)
        return validator

    def set_range(self, lower: int | None, upper: int | None):
        val = gui.IntValidator()
        val.set_range(lower, upper)
        self.set_validator(val)

    def set_validator(self, validator: gui.Validator):
        self.setValidator(validator)
        self._set_validation_color()

    def set_input_mask(self, mask: str):
        self.setInputMask(mask)

    def _set_validation_color(self, state: bool = True):
        color = "orange" if not self.is_valid() else None
        self.set_background_color(color)

    def set_echo_mode(self, mode: EchoModeStr):
        """Set echo mode.

        Args:
            mode: echo mode to use

        Raises:
            InvalidParamError: invalid echo mode
        """
        if mode not in ECHO_MODE:
            raise InvalidParamError(mode, ECHO_MODE)
        self.setEchoMode(ECHO_MODE[mode])

    def get_echo_mode(self) -> EchoModeStr:
        """Return echo mode.

        Returns:
            echo mode
        """
        return ECHO_MODE.inverse[self.echoMode()]

    def set_cursor_move_style(self, style: constants.CursorMoveStyleStr):
        """Set cursor move style.

        Args:
            style: cursor move style to use

        Raises:
            InvalidParamError: invalid cursor move style
        """
        if style not in constants.CURSOR_MOVE_STYLE:
            raise InvalidParamError(style, constants.CURSOR_MOVE_STYLE)
        self.setCursorMoveStyle(constants.CURSOR_MOVE_STYLE[style])

    def get_cursor_move_style(self) -> constants.CursorMoveStyleStr:
        """Return cursor move style.

        Returns:
            cursor move style
        """
        return constants.CURSOR_MOVE_STYLE.inverse[self.cursorMoveStyle()]

    def add_action(
        self, action: QtWidgets.QAction, position: ActionPositionStr = "trailing"
    ):
        self.addAction(action, ACTION_POSITION[position])

    def set_value(self, value: str):
        self.setText(value)

    def get_value(self) -> str:
        return self.text()

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()


if __name__ == "__main__":
    app = widgets.app()
    widget = LineEdit()
    action = widgets.Action(text="hallo", icon="mdi.folder")
    widget.add_action(action)
    widget.setPlaceholderText("test")
    widget.setClearButtonEnabled(True)
    # widget.set_regex_validator("[0-9]+")
    widget.setFont(gui.Font("Consolas"))
    widget.show()
    app.main_loop()
