from __future__ import annotations

import re
from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, datatypes, get_repr, helpers


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

ValidatorStr = Literal[
    "double",
    "color",
    "integer",
    "whitelist",
    "blacklist",
    "integer_classic",
    "path",
    "scientific_integer",
    "scientific_float",
    "python_code",
    "not_zero",
    "json",
    "regex",
    "regular_expression",
    "regex_pattern",
    "int_list",
    "float_list",
    "qss",
    "hex",
    "alphanumeric",
    "text_length",
    "website",
    "email",
]

WEB_REGEX = (
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}"
    r"\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)

MAIL_REGEX = r"[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+"


def get_validator(
    validator: ValidatorStr | datatypes.PatternType,
    **kwargs,
) -> QtGui.QValidator:
    match validator:
        case "email":
            return get_validator("regular_expression", regular_expression=MAIL_REGEX)
        case "website":
            return get_validator("regular_expression", regular_expression=WEB_REGEX)
        case str():
            ValidatorClass = helpers.get_class_for_id(gui.ValidatorMixin, validator)
            validator = ValidatorClass(**kwargs)
            return validator
        case QtCore.QRegularExpression():
            return get_validator("regular_expression", regular_expression=validator)
        case re.Pattern():
            return get_validator(
                "regular_expression", regular_expression=core.RegularExpression(validator)
            )
        case _:
            raise ValueError(validator)


class LineEdit(widgets.WidgetMixin, QtWidgets.QLineEdit):
    value_changed = core.Signal(str)
    tab_pressed = core.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self._on_value_change)

    def _on_value_change(self):
        val = self.get_value()
        self._set_validation_color()
        self.value_changed.emit(val)

    def __repr__(self):
        return get_repr(self, self.text())

    def __add__(self, other: str):
        self.append_text(other)
        return self

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "echoMode": ECHO_MODE,
            "cursorMoveStyle": constants.CURSOR_MOVE_STYLE,
            "alignment": constants.ALIGNMENTS,
        }
        return maps

    def font(self) -> gui.Font:
        return gui.Font(super().font())

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key.Key_Tab:
            self.tab_pressed.emit()

    def append_text(self, text: str):
        self.set_text(self.text() + text)

    def set_text(self, text: str):
        self.setText(text)

    def set_completer(self, completer: QtWidgets.QCompleter | Literal["files"]):
        match completer:
            case QtWidgets.QCompleter():
                self.setCompleter(completer)
            case "files":
                model = widgets.FileSystemModel()
                model.set_root_path("")
                completer = widgets.Completer(self)
                completer.setModel(model)
                self.setCompleter(completer)

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

    def set_validator(
        self,
        validator: QtGui.QValidator | ValidatorStr | datatypes.PatternType | None,
        strict: bool = True,
        empty_allowed: bool = True,
        **kwargs,
    ) -> QtGui.QValidator:
        from prettyqt import custom_validators

        match validator:
            case str() if "|" in validator:
                validators = [get_validator(i, **kwargs) for i in validator.split("|")]
                validator = custom_validators.CompositeValidator(validators)
            case str() | re.Pattern() | QtCore.QRegularExpression():
                validator = get_validator(validator, **kwargs)
            case None | QtGui.QValidator():
                pass
            case _:
                raise ValueError(validator)
        if not empty_allowed:
            validator = custom_validators.CompositeValidator(
                [validator, custom_validators.NotEmptyValidator()]
            )
        if not strict:
            validator = custom_validators.NotStrictValidator(validator)
        self.setValidator(validator)
        self._set_validation_color()
        return validator

    def set_input_mask(self, mask: str):
        match mask:
            case "ip_address":
                mask = "000.000.000.000;_"
            case "mac_address":
                mask = "HH:HH:HH:HH:HH:HH;_"
            case "iso_date":
                mask = "0000-00-00"
        self.setInputMask(mask)

    def _set_validation_color(self):
        color = None if self.hasAcceptableInput() else "orange"
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

    def add_action(self, action: QtGui.QAction, position: ActionPositionStr = "trailing"):
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
    action = gui.Action(text="hallo", icon="mdi.folder")
    # widget.add_action(action)
    widget.set_validator("website")
    widget.setPlaceholderText("test")
    widget.setClearButtonEnabled(True)
    # widget.set_regex_validator("[0-9]+")
    widget.show()
    app.main_loop()
    print(widget.hasAcceptableInput())
