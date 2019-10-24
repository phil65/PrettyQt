# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

from prettyqt import widgets
from prettyqt.utils import bidict


ICONS = bidict(none=QtWidgets.QMessageBox.NoIcon,
               information=QtWidgets.QMessageBox.Information,
               warning=QtWidgets.QMessageBox.Warning,
               critical=QtWidgets.QMessageBox.Critical,
               question=QtWidgets.QMessageBox.Question)

BUTTONS = bidict(none=QtWidgets.QMessageBox.NoButton,
                 cancel=QtWidgets.QMessageBox.Cancel,
                 ok=QtWidgets.QMessageBox.Ok,
                 save=QtWidgets.QMessageBox.Save,
                 open=QtWidgets.QMessageBox.Open,
                 close=QtWidgets.QMessageBox.Close,
                 discard=QtWidgets.QMessageBox.Discard,
                 apply=QtWidgets.QMessageBox.Apply,
                 reset=QtWidgets.QMessageBox.Reset,
                 restore_defaults=QtWidgets.QMessageBox.RestoreDefaults,
                 help=QtWidgets.QMessageBox.Help,
                 save_all=QtWidgets.QMessageBox.SaveAll,
                 yes=QtWidgets.QMessageBox.Yes,
                 yes_to_all=QtWidgets.QMessageBox.YesToAll,
                 no=QtWidgets.QMessageBox.No,
                 no_to_all=QtWidgets.QMessageBox.NoToAll,
                 abort=QtWidgets.QMessageBox.Abort,
                 retry=QtWidgets.QMessageBox.Retry,
                 ignore=QtWidgets.QMessageBox.Ignore)

TEXT_FORMATS = bidict(rich=QtCore.Qt.RichText,
                      plain=QtCore.Qt.PlainText,
                      auto=QtCore.Qt.AutoText)


QtWidgets.QMessageBox.__bases__ = (widgets.BaseDialog,)


class MessageBox(QtWidgets.QMessageBox):

    def __init__(self, icon=None, title=None, text="", details="", buttons=None,
                 parent=None):
        super().__init__(parent)
        self.set_icon(icon)
        self.setText(text)
        self.setWindowTitle(title)
        self.setWindowFlags(QtCore.Qt.Dialog |
                            QtCore.Qt.WindowTitleHint |
                            QtCore.Qt.CustomizeWindowHint)
        self.setDetailedText(details)
        if isinstance(buttons, list):
            for b in buttons:
                self.add_button(b)

    @classmethod
    def message(cls, text, title=None, icon=None):
        m = cls(cls.NoIcon, title, text)
        m.set_icon(icon)
        return m.show_blocking()

    def set_icon(self, icon):
        if icon in ICONS:
            self.setIcon(ICONS[icon])
            return None
        super().set_icon(icon)

    def show_blocking(self):
        return BUTTONS.inv[self.exec_()]

    def get_standard_buttons(self) -> list:
        return [k for k, v in BUTTONS.items() if v & self.standardButtons()]

    def add_button(self, button: str):
        """add a default button

        Valid arguments: "none", "cancel", "ok", "save", "open", "close",
                         "discard", "apply", "reset", "restore_defaults",
                         "help", "save_all", "yes", "yes_to_all", "no",
                         "no_to_all", "abort", "retry", "ignore"

        Args:
            button: button to add

        Returns:
            created button

        Raises:
            ValueError: Button type not available
        """
        if button not in BUTTONS:
            raise ValueError("button type not available")
        return self.addButton(BUTTONS[button])

    # @classmethod
    # def show_exception(cls, exception):
    #     header = str(exception[0])
    #     error_text = str(exception[1])
    #     widgets.MessageBox.message(error_text, header, "mdi.exclamation")

    def set_text_format(self, text_format: str):
        """set the text format

        Allowed values are "rich", "plain", "auto"

        Args:
            mode: text format to use

        Raises:
            ValueError: text format does not exist
        """
        if text_format not in TEXT_FORMATS:
            raise ValueError("Invalid text format")
        self.setTextFormat(TEXT_FORMATS[text_format])

    def get_text_format(self) -> str:
        """returns current text format

        Possible values: "rich", "plain", "auto"

        Returns:
            text format
        """
        return TEXT_FORMATS.inv[self.textFormat()]


if __name__ == "__main__":
    app = widgets.app()
    ret = MessageBox(icon="warning", title="header", text="text", details="details")
    ret.show()
    print(ret)
    app.exec_()
