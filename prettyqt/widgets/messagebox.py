from __future__ import annotations

from collections.abc import Callable
import sys
import traceback
from typing import Literal

from prettyqt import constants, gui, iconprovider, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import bidict, datatypes


IconStr = Literal["none", "information", "warning", "critical", "question"]

ICONS: bidict[IconStr, QtWidgets.QMessageBox.Icon] = bidict(
    none=QtWidgets.QMessageBox.Icon.NoIcon,
    information=QtWidgets.QMessageBox.Icon.Information,
    warning=QtWidgets.QMessageBox.Icon.Warning,
    critical=QtWidgets.QMessageBox.Icon.Critical,
    question=QtWidgets.QMessageBox.Icon.Question,
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

STANDARD_BUTTON: bidict[StandardButtonStr, QtWidgets.QMessageBox.StandardButton] = bidict(
    none=QtWidgets.QMessageBox.StandardButton.NoButton,
    cancel=QtWidgets.QMessageBox.StandardButton.Cancel,
    ok=QtWidgets.QMessageBox.StandardButton.Ok,
    save=QtWidgets.QMessageBox.StandardButton.Save,
    open=QtWidgets.QMessageBox.StandardButton.Open,
    close=QtWidgets.QMessageBox.StandardButton.Close,
    discard=QtWidgets.QMessageBox.StandardButton.Discard,
    apply=QtWidgets.QMessageBox.StandardButton.Apply,
    reset=QtWidgets.QMessageBox.StandardButton.Reset,
    restore_defaults=QtWidgets.QMessageBox.StandardButton.RestoreDefaults,
    help=QtWidgets.QMessageBox.StandardButton.Help,
    save_all=QtWidgets.QMessageBox.StandardButton.SaveAll,
    yes=QtWidgets.QMessageBox.StandardButton.Yes,
    yes_to_all=QtWidgets.QMessageBox.StandardButton.YesToAll,
    no=QtWidgets.QMessageBox.StandardButton.No,
    no_to_all=QtWidgets.QMessageBox.StandardButton.NoToAll,
    abort=QtWidgets.QMessageBox.StandardButton.Abort,
    retry=QtWidgets.QMessageBox.StandardButton.Retry,
    ignore=QtWidgets.QMessageBox.StandardButton.Ignore,
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

BUTTON_ROLE: bidict[ButtonRoleStr, QtWidgets.QMessageBox.ButtonRole] = bidict(
    invalid=QtWidgets.QMessageBox.ButtonRole.InvalidRole,
    accept=QtWidgets.QMessageBox.ButtonRole.AcceptRole,
    reject=QtWidgets.QMessageBox.ButtonRole.RejectRole,
    destructive=QtWidgets.QMessageBox.ButtonRole.DestructiveRole,
    action=QtWidgets.QMessageBox.ButtonRole.ActionRole,
    help=QtWidgets.QMessageBox.ButtonRole.HelpRole,
    yes=QtWidgets.QMessageBox.ButtonRole.YesRole,
    no=QtWidgets.QMessageBox.ButtonRole.NoRole,
    apply=QtWidgets.QMessageBox.ButtonRole.ApplyRole,
    reset=QtWidgets.QMessageBox.ButtonRole.ResetRole,
)


class MessageBox(widgets.DialogMixin, QtWidgets.QMessageBox):
    def __init__(
        self,
        icon: datatypes.IconType | IconStr = None,
        buttons: list[StandardButtonStr | QtWidgets.QMessageBox.StandardButton]
        | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.set_icon(icon)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.WindowTitleHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        if isinstance(buttons, list):
            for b in buttons:
                self.add_button(b)

    def get_button(
        self, button: QtWidgets.QMessageBox.StandardButton | StandardButtonStr
    ) -> QtWidgets.QAbstractButton:
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
        self, buttons: list[StandardButtonStr | QtWidgets.QMessageBox.StandardButton]
    ):
        flag = self.StandardButton.NoButton
        for val in buttons:
            flag |= STANDARD_BUTTON.get_enum_value(val)
        self.setStandardButtons(flag)

    def get_standard_buttons(self) -> list[StandardButtonStr]:
        return STANDARD_BUTTON.get_list(self.standardButtons())

    def add_button(
        self, button: StandardButtonStr | QtWidgets.QMessageBox.StandardButton
    ) -> QtWidgets.QPushButton:
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
        role: ButtonRoleStr | QtWidgets.QMessageBox.ButtonRole,
        callback: Callable | None = None,
    ) -> QtWidgets.QPushButton:
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

    def set_escape_button(self, button: StandardButtonStr | QtWidgets.QAbstractButton):
        if isinstance(button, QtWidgets.QAbstractButton):
            self.setEscapeButton(button)
        else:
            self.setEscapeButton(STANDARD_BUTTON.get_enum_value(button))

    def set_default_button(self, button: StandardButtonStr | QtWidgets.QPushButton):
        if isinstance(button, QtWidgets.QPushButton):
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
