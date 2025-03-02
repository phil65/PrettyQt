from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Self

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict, listdelegators


if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Sequence


StandardButtonStr = Literal[
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

STANDARD_BUTTON: bidict[StandardButtonStr, widgets.QDialogButtonBox.StandardButton] = (
    bidict(
        cancel=widgets.QDialogButtonBox.StandardButton.Cancel,
        ok=widgets.QDialogButtonBox.StandardButton.Ok,
        save=widgets.QDialogButtonBox.StandardButton.Save,
        open=widgets.QDialogButtonBox.StandardButton.Open,
        close=widgets.QDialogButtonBox.StandardButton.Close,
        discard=widgets.QDialogButtonBox.StandardButton.Discard,
        apply=widgets.QDialogButtonBox.StandardButton.Apply,
        reset=widgets.QDialogButtonBox.StandardButton.Reset,
        restore_defaults=widgets.QDialogButtonBox.StandardButton.RestoreDefaults,
        help=widgets.QDialogButtonBox.StandardButton.Help,
        save_all=widgets.QDialogButtonBox.StandardButton.SaveAll,
        yes=widgets.QDialogButtonBox.StandardButton.Yes,
        yes_to_all=widgets.QDialogButtonBox.StandardButton.YesToAll,
        no=widgets.QDialogButtonBox.StandardButton.No,
        no_to_all=widgets.QDialogButtonBox.StandardButton.NoToAll,
        abort=widgets.QDialogButtonBox.StandardButton.Abort,
        retry=widgets.QDialogButtonBox.StandardButton.Retry,
        ignore=widgets.QDialogButtonBox.StandardButton.Ignore,
    )
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

ROLES: bidict[RoleStr, widgets.QDialogButtonBox.ButtonRole] = bidict(
    invalid=widgets.QDialogButtonBox.ButtonRole.InvalidRole,
    accept=widgets.QDialogButtonBox.ButtonRole.AcceptRole,
    reject=widgets.QDialogButtonBox.ButtonRole.RejectRole,
    destructive=widgets.QDialogButtonBox.ButtonRole.DestructiveRole,
    action=widgets.QDialogButtonBox.ButtonRole.ActionRole,
    help=widgets.QDialogButtonBox.ButtonRole.HelpRole,
    yes=widgets.QDialogButtonBox.ButtonRole.YesRole,
    no=widgets.QDialogButtonBox.ButtonRole.NoRole,
    apply=widgets.QDialogButtonBox.ButtonRole.ApplyRole,
    reset=widgets.QDialogButtonBox.ButtonRole.ResetRole,
)


class DialogButtonBox(widgets.WidgetMixin, widgets.QDialogButtonBox):
    """Widget presenting buttons in a layout that is appropriate to the widget style."""

    button_clicked = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.on_click)

    def __len__(self) -> int:
        return len(self.buttons())

    def __getitem__(self, index: StandardButtonStr) -> widgets.QPushButton:
        return self.button(STANDARD_BUTTON[index])

    def __iter__(self) -> Iterator[widgets.QAbstractButton]:
        return iter(self.buttons())

    def __contains__(self, index: StandardButtonStr):
        return self.button(STANDARD_BUTTON[index]) is not None

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "orientation": constants.ORIENTATION,
            "standardButtons": STANDARD_BUTTON,
        }
        return maps

    @classmethod
    def create(cls, **kwargs) -> Self:
        box = cls()
        for k, v in kwargs.items():
            box.add_default_button(k, callback=v)  # type: ignore
        return box

    def on_click(self, button: core.QObject):
        self.button_clicked.emit(button.objectName())

    def set_horizontal(self):
        self.setOrientation(constants.HORIZONTAL)

    def set_vertical(self):
        self.setOrientation(constants.VERTICAL)

    def set_orientation(
        self, orientation: constants.OrientationStr | constants.Orientation
    ):
        """Set the orientation of the button box.

        Args:
            orientation: orientation for the button box
        """
        self.setOrientation(constants.ORIENTATION.get_enum_value(orientation))

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]

    def add_default_buttons(
        self, buttons: Sequence[StandardButtonStr]
    ) -> listdelegators.ListDelegator[widgets.QPushButton]:
        return [self.add_default_button(btn) for btn in buttons]

    def add_default_button(
        self,
        button: StandardButtonStr | widgets.QDialogButtonBox.StandardButton,
        callback: Callable | None = None,
    ) -> widgets.QPushButton:
        """Add a default button.

        Args:
            button: button to add
            callback: function to call when button gets clicked

        Returns:
            created button
        """
        btn = super().addButton(STANDARD_BUTTON.get_enum_value(button))
        btn.setObjectName(button)
        if callback:
            btn.clicked.connect(callback)
        return btn

    def add_button(
        self,
        button: widgets.QPushButton | str,
        role: RoleStr | widgets.QDialogButtonBox.ButtonRole = "accept",
        callback: Callable | None = None,
    ) -> widgets.QPushButton:
        """Add a button.

        Args:
            button: button to add
            role: role of the button
            callback: function to call when button gets clicked

        Returns:
            created button
        """
        if isinstance(button, str):
            button = widgets.PushButton(button)
        self.addButton(button, ROLES.get_enum_value(role))
        if callback:
            button.clicked.connect(callback)
        return button


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = DialogButtonBox()
    buttons = list(STANDARD_BUTTON.keys())
    widget.add_default_buttons(buttons)
    widget.show()
    app.exec()
