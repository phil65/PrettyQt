from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Callable, Literal

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


BUTTONS = bidict(
    cancel=QtWidgets.QDialogButtonBox.StandardButton.Cancel,
    ok=QtWidgets.QDialogButtonBox.StandardButton.Ok,
    save=QtWidgets.QDialogButtonBox.StandardButton.Save,
    open=QtWidgets.QDialogButtonBox.StandardButton.Open,
    close=QtWidgets.QDialogButtonBox.StandardButton.Close,
    discard=QtWidgets.QDialogButtonBox.StandardButton.Discard,
    apply=QtWidgets.QDialogButtonBox.StandardButton.Apply,
    reset=QtWidgets.QDialogButtonBox.StandardButton.Reset,
    restore_defaults=QtWidgets.QDialogButtonBox.StandardButton.RestoreDefaults,
    help=QtWidgets.QDialogButtonBox.StandardButton.Help,
    save_all=QtWidgets.QDialogButtonBox.StandardButton.SaveAll,
    yes=QtWidgets.QDialogButtonBox.StandardButton.Yes,
    yes_to_all=QtWidgets.QDialogButtonBox.StandardButton.YesToAll,
    no=QtWidgets.QDialogButtonBox.StandardButton.No,
    no_to_all=QtWidgets.QDialogButtonBox.StandardButton.NoToAll,
    abort=QtWidgets.QDialogButtonBox.StandardButton.Abort,
    retry=QtWidgets.QDialogButtonBox.StandardButton.Retry,
    ignore=QtWidgets.QDialogButtonBox.StandardButton.Ignore,
)

ButtonStr = Literal[
    "cancel",
    "ok",
    "save",
    "open",
    "close",
    "discard",
    "apply",
    "reset",
    "restore_defaults",
    "help",
    "save_all",
    "yes",
    "yes_to_all",
    "no",
    "no_to_all",
    "abort",
    "retry",
    "ignore",
]

ROLES = bidict(
    invalid=QtWidgets.QDialogButtonBox.ButtonRole.InvalidRole,
    accept=QtWidgets.QDialogButtonBox.ButtonRole.AcceptRole,
    reject=QtWidgets.QDialogButtonBox.ButtonRole.RejectRole,
    destructive=QtWidgets.QDialogButtonBox.ButtonRole.DestructiveRole,
    action=QtWidgets.QDialogButtonBox.ButtonRole.ActionRole,
    help=QtWidgets.QDialogButtonBox.ButtonRole.HelpRole,
    yes=QtWidgets.QDialogButtonBox.ButtonRole.YesRole,
    no=QtWidgets.QDialogButtonBox.ButtonRole.NoRole,
    apply=QtWidgets.QDialogButtonBox.ButtonRole.ApplyRole,
    reset=QtWidgets.QDialogButtonBox.ButtonRole.ResetRole,
)

RoleStr = Literal[
    "invalid",
    "accept",
    "reject",
    "destructive",
    "action",
    "help",
    "yes",
    "no",
    "apply",
    "reset",
]

QtWidgets.QDialogButtonBox.__bases__ = (widgets.Widget,)


class DialogButtonBox(QtWidgets.QDialogButtonBox):

    button_clicked = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.on_click)

    def __len__(self) -> int:
        return len(self.buttons())

    def __getitem__(self, index: ButtonStr) -> QtWidgets.QPushButton:
        return self.button(BUTTONS[index])

    def __iter__(self) -> Iterator[QtWidgets.QAbstractButton]:
        return iter(self.buttons())

    def __contains__(self, index: ButtonStr):
        return self.button(BUTTONS[index]) is not None

    @classmethod
    def create(cls, **kwargs):
        box = cls()
        for k, v in kwargs.items():
            box.add_default_button(k, callback=v)  # type: ignore
        return box

    def on_click(self, button: QtCore.QObject):
        self.button_clicked.emit(button.objectName())

    def set_horizontal(self):
        self.setOrientation(constants.HORIZONTAL)

    def set_vertical(self):
        self.setOrientation(constants.VERTICAL)

    def set_orientation(self, orientation: constants.OrientationStr):
        """Set the orientation of the button box.

        Args:
            orientation: orientation for the button box

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in constants.ORIENTATION:
            raise InvalidParamError(orientation, constants.ORIENTATION)
        self.setOrientation(constants.ORIENTATION[orientation])

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]

    def add_default_buttons(self, buttons: Sequence[ButtonStr]):
        return [self.add_default_button(btn) for btn in buttons]

    def add_default_button(
        self, button: ButtonStr, callback: Callable | None = None
    ) -> QtWidgets.QPushButton:
        """Add a default button.

        Args:
            button: button to add
            callback: function to call when button gets clicked

        Returns:
            created button

        Raises:
            InvalidParamError: Button type not available
        """
        if button not in BUTTONS:
            raise InvalidParamError(button, BUTTONS)
        btn = self.addButton(BUTTONS[button])
        btn.setObjectName(button)
        if callback:
            btn.clicked.connect(callback)
        return btn

    def add_button(
        self,
        button: QtWidgets.QPushButton | ButtonStr,
        role: RoleStr = "accept",
        callback: Callable | None = None,
    ) -> widgets.PushButton:
        """Add a button.

        Args:
            button: button to add
            role: role of the button
            callback: function to call when button gets clicked

        Returns:
            created button

        Raises:
            InvalidParamError: Button type not available
        """
        if isinstance(button, str):
            button = widgets.PushButton(button)
        self.addButton(button, ROLES[role])
        if callback:
            button.clicked.connect(callback)
        return button


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = DialogButtonBox()
    buttons = list(BUTTONS.keys())
    widget.add_default_buttons(buttons)
    widget.button_clicked.connect(print)
    widget.show()
    app.main_loop()
