from typing import Literal, Optional

from qtpy import QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import InvalidParamError, bidict


ECHO_MODES = bidict(
    normal=QtWidgets.QLineEdit.Normal,
    no_echo=QtWidgets.QLineEdit.NoEcho,
    password=QtWidgets.QLineEdit.Password,
    echo_on_edit=QtWidgets.QLineEdit.PasswordEchoOnEdit,
)

EchoModeStr = Literal["normal", "no_echo", "password", "echo_on_edit"]


QtWidgets.QLineEdit.__bases__ = (widgets.Widget,)


class LineEdit(QtWidgets.QLineEdit):

    value_changed = core.Signal(str)

    def __init__(
        self,
        default_value: str = "",
        read_only: bool = False,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(default_value, parent)
        self.textChanged.connect(self._set_validation_color)
        self.textChanged.connect(self.value_changed)
        self.set_read_only(read_only)

    def __repr__(self):
        return f"LineEdit: {self.serialize_fields()}"

    def __setstate__(self, state):
        self.set_text(state["text"])
        self.setEnabled(state.get("enabled", True))
        self.setFont(state["font"])
        self.setValidator(state["validator"])
        self.setInputMask(state["input_mask"])
        self.setMaxLength(state["max_length"])
        self.setPlaceholderText(state["placeholder_text"])
        self.setReadOnly(state["read_only"])
        self.setFrame(state["has_frame"])
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other):
        if isinstance(other, str):
            self.append_text(other)
            return self

    def serialize_fields(self):
        return dict(
            text=self.text(),
            font=gui.Font(self.font()),
            validator=self.validator(),
            max_length=self.maxLength(),
            read_only=self.isReadOnly(),
            input_mask=self.inputMask(),
            has_frame=self.hasFrame(),
            placeholder_text=self.placeholderText(),
        )

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

    def set_regex_validator(self, regex: str, flags=0) -> gui.RegExpValidator:
        validator = gui.RegularExpressionValidator(self)
        validator.set_regex(regex, flags)
        self.set_validator(validator)
        return validator

    def set_range(self, lower, upper):
        val = gui.IntValidator()
        val.setRange(lower, upper)
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
        if mode not in ECHO_MODES:
            raise InvalidParamError(mode, ECHO_MODES)
        self.setEchoMode(ECHO_MODES[mode])

    def get_echo_mode(self) -> EchoModeStr:
        """Return echo mode.

        Returns:
            echo mode
        """
        return ECHO_MODES.inverse[self.echoMode()]

    def set_value(self, value: str):
        self.setText(value)

    def get_value(self) -> str:
        return self.text()

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()


if __name__ == "__main__":
    app = widgets.app()
    widget = LineEdit("This is a test")
    widget.set_regex_validator("[0-9]+")
    widget.setFont(gui.Font("Consolas"))
    widget.show()
    app.main_loop()
