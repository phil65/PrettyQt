import sys
import traceback
from typing import List, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import InvalidParamError, bidict


ICONS = bidict(
    none=QtWidgets.QMessageBox.NoIcon,
    information=QtWidgets.QMessageBox.Information,
    warning=QtWidgets.QMessageBox.Warning,
    critical=QtWidgets.QMessageBox.Critical,
    question=QtWidgets.QMessageBox.Question,
)

BUTTONS = bidict(
    none=QtWidgets.QMessageBox.NoButton,
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
    ignore=QtWidgets.QMessageBox.Ignore,
)

TEXT_FORMAT = bidict(
    rich=QtCore.Qt.RichText, plain=QtCore.Qt.PlainText, auto=QtCore.Qt.AutoText
)
if core.VersionNumber.get_qt_version() >= (5, 14, 0):
    TEXT_FORMAT["markdown"] = QtCore.Qt.MarkdownText

QtWidgets.QMessageBox.__bases__ = (widgets.BaseDialog,)


class MessageBox(QtWidgets.QMessageBox):
    def __init__(
        self,
        icon: gui.icon.IconType = None,
        title: Optional[str] = None,
        text: str = "",
        informative_text: str = "",
        details: str = "",
        buttons: Optional[list] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent)
        self.set_icon(icon)
        self.setText(text)
        self.setInformativeText(informative_text)
        self.setWindowTitle(title)
        self.setWindowFlags(
            QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint
        )
        self.setDetailedText(details)
        if isinstance(buttons, list):
            for b in buttons:
                self.add_button(b)

    @classmethod
    def message(
        cls,
        text: str,
        title: str = None,
        icon: gui.icon.IconType = None,
        detail_text: Optional[str] = None,
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

    def set_icon(self, icon: gui.icon.IconType):
        if icon in ICONS:
            self.setIcon(ICONS[icon])
            return None
        icon = gui.icon.get_icon(icon)
        self.setIconPixmap(icon.get_pixmap(size=64))

    def show_blocking(self) -> str:
        return BUTTONS.inverse[self.exec_()]

    def get_standard_buttons(self) -> List[str]:
        return [k for k, v in BUTTONS.items() if v & self.standardButtons()]

    def add_button(self, button: str) -> QtWidgets.QPushButton:
        """Add a default button.

        Valid arguments: "none", "cancel", "ok", "save", "open", "close",
                         "discard", "apply", "reset", "restore_defaults",
                         "help", "save_all", "yes", "yes_to_all", "no",
                         "no_to_all", "abort", "retry", "ignore"

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

    def set_text_format(self, text_format: str):
        """Set the text format.

        Allowed values are "rich", "plain", "auto"

        Args:
            text_format: text format to use

        Raises:
            InvalidParamError: text format does not exist
        """
        if text_format not in TEXT_FORMAT:
            raise InvalidParamError(text_format, TEXT_FORMAT)
        self.setTextFormat(TEXT_FORMAT[text_format])

    def get_text_format(self) -> str:
        """Return current text format.

        Possible values: "rich", "plain", "auto"

        Returns:
            text format
        """
        return TEXT_FORMAT.inverse[self.textFormat()]


if __name__ == "__main__":
    app = widgets.app()
    ret = MessageBox(icon="warning", title="header", text="text", details="details")
    ret.set_icon("mdi.folder")
    ret.show()
    print(ret)
    app.main_loop()
