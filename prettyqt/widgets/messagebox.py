from __future__ import annotations

import sys
import traceback
from typing import Literal

from prettyqt import gui, iconprovider, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


ICONS = bidict(
    none=QtWidgets.QMessageBox.Icon.NoIcon,
    information=QtWidgets.QMessageBox.Icon.Information,
    warning=QtWidgets.QMessageBox.Icon.Warning,
    critical=QtWidgets.QMessageBox.Icon.Critical,
    question=QtWidgets.QMessageBox.Icon.Question,
)

IconStr = Literal["none", "information", "warning", "critical", "question"]

BUTTONS = bidict(
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

ButtonStr = Literal[
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

BUTTON_ROLE = bidict(
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

TEXT_FORMAT = bidict(
    rich=QtCore.Qt.TextFormat.RichText,
    plain=QtCore.Qt.TextFormat.PlainText,
    auto=QtCore.Qt.TextFormat.AutoText,
    markdown=QtCore.Qt.TextFormat.MarkdownText,
)

TextFormatStr = Literal["rich", "plain", "auto", "markdown"]

QtWidgets.QMessageBox.__bases__ = (widgets.Dialog,)


class MessageBox(QtWidgets.QMessageBox):
    def __init__(
        self,
        icon: types.IconType | IconStr = None,
        title: str = "",
        text: str = "",
        informative_text: str = "",
        details: str = "",
        buttons: list[ButtonStr] | None = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.set_icon(icon)
        self.setText(text)
        self.setInformativeText(informative_text)
        self.setWindowTitle(title)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog  # type: ignore
            | QtCore.Qt.WindowType.WindowTitleHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.setDetailedText(details)
        if isinstance(buttons, list):
            for b in buttons:
                self.add_button(b)

    def serialize_fields(self):
        return dict(
            icon=self.get_icon(),
            detailed_text=self.detailedText(),
            icon_pixmap=self.get_icon_pixmap(),
            informative_text=self.informativeText(),
            text=self.text(),
            text_format=self.get_text_format(),
        )

    @classmethod
    def message(
        cls,
        text: str,
        title: str = "",
        icon: types.IconType = None,
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

    def set_icon(self, icon: types.IconType | IconStr):
        if icon in ICONS:
            self.setIcon(ICONS[icon])
        else:
            ico = iconprovider.get_icon(icon)
            self.setIconPixmap(ico.get_pixmap(size=64))

    def show_blocking(self) -> ButtonStr:
        return BUTTONS.inverse[self.main_loop()]

    def get_icon_pixmap(self) -> gui.Pixmap | None:
        pix = self.iconPixmap()
        if pix.isNull():
            return None
        return gui.Pixmap(pix)

    def get_standard_buttons(self) -> list[ButtonStr]:
        return [k for k, v in BUTTONS.items() if v & self.standardButtons()]

    def add_button(self, button: ButtonStr) -> QtWidgets.QPushButton:
        """Add a default button.

        Args:
            button: button to add

        Returns:
            created button

        Raises:
            InvalidParamError: Button type not available
        """
        if button not in BUTTONS:
            raise InvalidParamError(button, BUTTONS)
        return self.addButton(BUTTONS[button])

    # @classmethod
    # def show_exception(cls, exception):
    #     header = str(exception[0])
    #     error_text = str(exception[1])
    #     widgets.MessageBox.message(error_text, header, "mdi.exclamation")

    def set_text_format(self, text_format: TextFormatStr):
        """Set the text format.

        Args:
            text_format: text format to use

        Raises:
            InvalidParamError: text format does not exist
        """
        if text_format not in TEXT_FORMAT:
            raise InvalidParamError(text_format, TEXT_FORMAT)
        self.setTextFormat(TEXT_FORMAT[text_format])

    def get_text_format(self) -> TextFormatStr:
        """Return current text format.

        Returns:
            text format
        """
        return TEXT_FORMAT.inverse[self.textFormat()]

    def set_escape_button(self, button: ButtonStr | QtWidgets.QAbstractButton):
        if isinstance(button, QtWidgets.QAbstractButton):
            self.setEscapeButton(button)
        else:
            self.setEscapeButton(BUTTONS[button])

    def set_default_button(self, button: ButtonStr | QtWidgets.QPushButton):
        if isinstance(button, QtWidgets.QPushButton):
            self.setDefaultButton(button)
        else:
            self.setDefaultButton(BUTTONS[button])


if __name__ == "__main__":
    app = widgets.app()
    ret = MessageBox(icon="warning", title="header", text="text", details="details")
    ret.set_icon("mdi.folder")
    ret.show()
    print(ret)
    app.main_loop()
