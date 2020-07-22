# -*- coding: utf-8 -*-
"""
"""

from typing import Callable, List, Optional, Union

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict


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

ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)


QtWidgets.QDialogButtonBox.__bases__ = (widgets.Widget,)


class DialogButtonBox(QtWidgets.QDialogButtonBox):

    button_clicked = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.on_click)

    def __len__(self) -> int:
        return len(self.buttons())

    def __getitem__(self, index):
        return self.button(BUTTONS[index])

    def __iter__(self):
        return iter(self.buttons())

    def __contains__(self, item):
        return self[item] is not None

    @classmethod
    def create(cls, **kwargs):
        box = cls()
        for k, v in kwargs.items():
            box.add_default_button(k, callback=v)
        return box

    def on_click(self, button):
        self.button_clicked.emit(button.objectName())

    def set_horizontal(self):
        self.setOrientation(QtCore.Qt.Horizontal)

    def set_vertical(self):
        self.setOrientation(QtCore.Qt.Vertical)

    def set_orientation(self, orientation: str):
        """set the orientation of the button box

        Allowed values are "horizontal", "vertical"

        Args:
            orientation: orientation for the button box

        Raises:
            ValueError: orientation does not exist
        """
        if orientation not in ORIENTATIONS:
            raise ValueError(f"{orientation} not a valid orientation.")
        self.setOrientation(ORIENTATIONS[orientation])

    def get_orientation(self) -> str:
        """returns current orientation

        Possible values: "horizontal", "vertical"

        Returns:
            orientation
        """
        return ORIENTATIONS.inv[self.orientation()]

    def add_default_buttons(self, buttons: List[str]):
        return [self.add_default_button(btn) for btn in buttons]

    def add_default_button(
        self, button: str, callback: Optional[Callable] = None
    ) -> QtWidgets.QPushButton:
        """add a default button

        Valid arguments: "cancel", "ok", "save", "open", "close",
                         "discard", "apply", "reset", "restore_defaults",
                         "help", "save_all", "yes", "yes_to_all", "no",
                         "no_to_all", "abort", "retry", "ignore"

        Args:
            button: button to add
            callback: function to call when button gets clicked

        Returns:
            created button

        Raises:
            ValueError: Button type not available
        """
        if button not in BUTTONS:
            raise ValueError("button type not available")
        btn = self.addButton(BUTTONS[button])
        btn.setObjectName(button)
        if callback:
            btn.clicked.connect(callback)
        return btn

    def add_button(
        self,
        button: Union[QtWidgets.QPushButton, str],
        role: str = "accept",
        callback: Optional[Callable] = None,
    ) -> widgets.PushButton:
        """add a button

        Args:
            button: button to add
            role: role of the button
            callback: function to call when button gets clicked

        Returns:
            created button

        Raises:
            ValueError: Button type not available
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
    app.exec_()
