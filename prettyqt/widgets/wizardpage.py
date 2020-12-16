from qtpy import QtGui, QtWidgets

from prettyqt import gui, widgets
from prettyqt.utils import InvalidParamError


QtWidgets.QWizardPage.__bases__ = (widgets.Widget,)


class WizardPage(QtWidgets.QWizardPage):
    def set_pixmap(self, typ: str, pixmap: QtGui.QPixmap):
        if typ not in widgets.wizard.WIZARD_PIXMAP:
            raise InvalidParamError(typ, widgets.wizard.WIZARD_PIXMAP)
        self.setPixmap(widgets.wizard.WIZARD_PIXMAP[typ], pixmap)

    def get_pixmap(self, typ: str) -> gui.Pixmap:
        if typ not in widgets.wizard.WIZARD_PIXMAP:
            raise InvalidParamError(typ, widgets.wizard.WIZARD_PIXMAP)
        return gui.Pixmap(self.pixmap(widgets.wizard.WIZARD_PIXMAP[typ]))

    def set_button_text(self, button_type: str, value: str) -> str:
        """Set text for given button type.

        Args:
            button_type: button to get text from
            value: text to set

        """
        if button_type not in widgets.wizard.WIZARD_BUTTON:
            raise InvalidParamError(button_type, widgets.wizard.WIZARD_BUTTON)
        return self.setButtonText(widgets.wizard.WIZARD_BUTTON[button_type], value)

    def get_button_text(self, button_type: str) -> str:
        """Return text for given button type.

        Args:
            button_type: button to get text from

        Returns:
            Button text
        """
        if button_type not in widgets.wizard.WIZARD_BUTTON:
            raise InvalidParamError(button_type, widgets.wizard.WIZARD_BUTTON)
        return self.buttonText(widgets.wizard.WIZARD_BUTTON[button_type])
