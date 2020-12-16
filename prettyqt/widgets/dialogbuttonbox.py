from typing import Callable, Iterator, Literal, Optional, Sequence, Union

from qtpy import QtCore, QtWidgets

from prettyqt import constants, core, widgets
from prettyqt.utils import InvalidParamError, bidict


BUTTONS = bidict(
    cancel=QtWidgets.QDialogButtonBox.Cancel,
    ok=QtWidgets.QDialogButtonBox.Ok,
    save=QtWidgets.QDialogButtonBox.Save,
    open=QtWidgets.QDialogButtonBox.Open,
    close=QtWidgets.QDialogButtonBox.Close,
    discard=QtWidgets.QDialogButtonBox.Discard,
    apply=QtWidgets.QDialogButtonBox.Apply,
    reset=QtWidgets.QDialogButtonBox.Reset,
    restore_defaults=QtWidgets.QDialogButtonBox.RestoreDefaults,
    help=QtWidgets.QDialogButtonBox.Help,
    save_all=QtWidgets.QDialogButtonBox.SaveAll,
    yes=QtWidgets.QDialogButtonBox.Yes,
    yes_to_all=QtWidgets.QDialogButtonBox.YesToAll,
    no=QtWidgets.QDialogButtonBox.No,
    no_to_all=QtWidgets.QDialogButtonBox.NoToAll,
    abort=QtWidgets.QDialogButtonBox.Abort,
    retry=QtWidgets.QDialogButtonBox.Retry,
    ignore=QtWidgets.QDialogButtonBox.Ignore,
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
    invalid=QtWidgets.QDialogButtonBox.InvalidRole,
    accept=QtWidgets.QDialogButtonBox.AcceptRole,
    reject=QtWidgets.QDialogButtonBox.RejectRole,
    destructive=QtWidgets.QDialogButtonBox.DestructiveRole,
    action=QtWidgets.QDialogButtonBox.ActionRole,
    help=QtWidgets.QDialogButtonBox.HelpRole,
    yes=QtWidgets.QDialogButtonBox.YesRole,
    no=QtWidgets.QDialogButtonBox.NoRole,
    apply=QtWidgets.QDialogButtonBox.ApplyRole,
    reset=QtWidgets.QDialogButtonBox.ResetRole,
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

    def __contains__(self, item: ButtonStr):
        return self[item] is not None

    @classmethod
    def create(cls, **kwargs):
        box = cls()
        for k, v in kwargs.items():
            box.add_default_button(k, callback=v)  # type: ignore
        return box

    def on_click(self, button):
        self.button_clicked.emit(button.objectName())

    def set_horizontal(self):
        self.setOrientation(QtCore.Qt.Horizontal)

    def set_vertical(self):
        self.setOrientation(QtCore.Qt.Vertical)

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
        self, button: ButtonStr, callback: Optional[Callable] = None
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
        button: Union[QtWidgets.QPushButton, ButtonStr],
        role: RoleStr = "accept",
        callback: Optional[Callable] = None,
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
