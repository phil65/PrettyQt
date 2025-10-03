from __future__ import annotations

import sys
import traceback
from typing import TYPE_CHECKING, Literal

from prettyqt import constants, gui, iconprovider, widgets
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from collections.abc import Callable

    from prettyqt.utils import datatypes


IconStr = Literal["none", "information", "warning", "critical", "question"]

ICONS: bidict[IconStr, widgets.QMessageBox.Icon] = bidict(
    none=widgets.QMessageBox.Icon.NoIcon,
    information=widgets.QMessageBox.Icon.Information,
    warning=widgets.QMessageBox.Icon.Warning,
    critical=widgets.QMessageBox.Icon.Critical,
    question=widgets.QMessageBox.Icon.Question,
)

StandardButtonStr = Literal[
    "none",
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

STANDARD_BUTTON: bidict[StandardButtonStr, widgets.QMessageBox.StandardButton] = bidict(
    none=widgets.QMessageBox.StandardButton.NoButton,
    cancel=widgets.QMessageBox.StandardButton.Cancel,
    ok=widgets.QMessageBox.StandardButton.Ok,
    save=widgets.QMessageBox.StandardButton.Save,
    open=widgets.QMessageBox.StandardButton.Open,
    close=widgets.QMessageBox.StandardButton.Close,
    discard=widgets.QMessageBox.StandardButton.Discard,
    apply=widgets.QMessageBox.StandardButton.Apply,
    reset=widgets.QMessageBox.StandardButton.Reset,
    restore_defaults=widgets.QMessageBox.StandardButton.RestoreDefaults,
    help=widgets.QMessageBox.StandardButton.Help,
    save_all=widgets.QMessageBox.StandardButton.SaveAll,
    yes=widgets.QMessageBox.StandardButton.Yes,
    yes_to_all=widgets.QMessageBox.StandardButton.YesToAll,
    no=widgets.QMessageBox.StandardButton.No,
    no_to_all=widgets.QMessageBox.StandardButton.NoToAll,
    abort=widgets.QMessageBox.StandardButton.Abort,
    retry=widgets.QMessageBox.StandardButton.Retry,
    ignore=widgets.QMessageBox.StandardButton.Ignore,
)

ButtonRoleStr = Literal[
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

BUTTON_ROLE: bidict[ButtonRoleStr, widgets.QMessageBox.ButtonRole] = bidict(
    invalid=widgets.QMessageBox.ButtonRole.InvalidRole,
    accept=widgets.QMessageBox.ButtonRole.AcceptRole,
    reject=widgets.QMessageBox.ButtonRole.RejectRole,
    destructive=widgets.QMessageBox.ButtonRole.DestructiveRole,
    action=widgets.QMessageBox.ButtonRole.ActionRole,
    help=widgets.QMessageBox.ButtonRole.HelpRole,
    yes=widgets.QMessageBox.ButtonRole.YesRole,
    no=widgets.QMessageBox.ButtonRole.NoRole,
    apply=widgets.QMessageBox.ButtonRole.ApplyRole,
    reset=widgets.QMessageBox.ButtonRole.ResetRole,
)


class MessageBox(widgets.DialogMixin, widgets.QMessageBox):
    """Modal dialog for informing the user (and for receiving an answer)."""

    def __init__(
        self,
        icon: datatypes.IconType | IconStr = None,
        buttons: (
            list[StandardButtonStr | widgets.QMessageBox.StandardButton] | None
        ) = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.set_icon(icon)
        self.setWindowFlags(
            constants.WindowType.Dialog
            | constants.WindowType.WindowTitleHint
            | constants.WindowType.CustomizeWindowHint
        )
        if isinstance(buttons, list):
            for b in buttons:
                self.add_button(b)

    def get_button(
        self, button: widgets.QMessageBox.StandardButton | StandardButtonStr
    ) -> widgets.QAbstractButton:
        return self.button(STANDARD_BUTTON.get_enum_value(button))

    @classmethod
    def message(
        cls,
        text: str,
        title: str = "",
        icon: datatypes.IconType = None,
        detail_text: str | None = None,
    ) -> str:
        m = cls("none", title, text)
        m.set_icon(icon)
        if detail_text is not None:
            m.setDetailedText(detail_text)
        return m.show_blocking()

    @classmethod
    def show_exception(cls, exception: Exception):
        exctype, value = sys.exc_info()[:2]
        tb = traceback.format_exc()
        dlg = cls(text=str(value), title=str(exctype), icon="critical", details=tb)
        dlg.show_blocking()

    def set_icon(self, icon: datatypes.IconType | IconStr):
        if icon in ICONS:
            self.setIcon(ICONS[icon])
        else:
            ico = iconprovider.get_icon(icon)
            self.setIconPixmap(ico.get_pixmap(size=64))

    def show_blocking(self) -> StandardButtonStr:
        return STANDARD_BUTTON.inverse[self.exec()]

    def get_icon_pixmap(self) -> gui.Pixmap | None:
        pix = self.iconPixmap()
        return None if pix.isNull() else gui.Pixmap(pix)

    def set_standard_buttons(
        self, buttons: list[StandardButtonStr | widgets.QMessageBox.StandardButton]
    ):
        flag = self.StandardButton.NoButton
        for val in buttons:
            flag |= STANDARD_BUTTON.get_enum_value(val)
        self.setStandardButtons(flag)

    def get_standard_buttons(self) -> list[StandardButtonStr]:
        return STANDARD_BUTTON.get_list(self.standardButtons())

    def add_button(
        self, button: StandardButtonStr | widgets.QMessageBox.StandardButton
    ) -> widgets.QPushButton:
        """Add a default button.

        Args:
            button: button to add

        Returns:
            created button
        """
        return self.addButton(STANDARD_BUTTON.get_enum_value(button))

    def add_custom_button(
        self,
        button: str,
        role: ButtonRoleStr | widgets.QMessageBox.ButtonRole,
        callback: Callable | None = None,
    ) -> widgets.QPushButton:
        btn = self.addButton(button, BUTTON_ROLE.get_enum_value(role))
        if callback:
            btn.clicked.connect(callback)

    # @classmethod
    # def show_exception(cls, exception):
    #     header = str(exception[0])
    #     error_text = str(exception[1])
    #     widgets.MessageBox.message(error_text, header, "mdi.exclamation")

    def set_text_format(
        self, text_format: constants.TextFormatStr | constants.TextFormat
    ):
        """Set the text format.

        Args:
            text_format: text format to use
        """
        self.setTextFormat(constants.TEXT_FORMAT.get_enum_value(text_format))

    def get_text_format(self) -> constants.TextFormatStr:
        """Return current text format.

        Returns:
            text format
        """
        return constants.TEXT_FORMAT.inverse[self.textFormat()]

    def set_escape_button(self, button: StandardButtonStr | widgets.QAbstractButton):
        if isinstance(button, widgets.QAbstractButton):
            self.setEscapeButton(button)
        else:
            self.setEscapeButton(STANDARD_BUTTON.get_enum_value(button))

    def set_default_button(self, button: StandardButtonStr | widgets.QPushButton):
        if isinstance(button, widgets.QPushButton):
            self.setDefaultButton(button)
        else:
            self.setDefaultButton(STANDARD_BUTTON.get_enum_value(button))


if __name__ == "__main__":
    app = widgets.app()
    ret = MessageBox(icon="warning", window_title="header", text="text")
    ret.set_standard_buttons(["ok", "cancel"])
    ret.add_custom_button("tt", "accept", callback=lambda: print("click"))
    ret.show()
    app.exec()
