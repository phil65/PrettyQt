from __future__ import annotations

from typing import Optional

from prettyqt import gui, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError


QtWidgets.QWizardPage.__bases__ = (widgets.Widget,)


class WizardPage(QtWidgets.QWizardPage):
    def set_pixmap(
        self, typ: widgets.wizard.WizardPixmapStr, pixmap: Optional[QtGui.QPixmap]
    ):
        if typ not in widgets.wizard.WIZARD_PIXMAP:
            raise InvalidParamError(typ, widgets.wizard.WIZARD_PIXMAP)
        if pixmap is None:
            pixmap = QtGui.QPixmap()
        self.setPixmap(widgets.wizard.WIZARD_PIXMAP[typ], pixmap)

    def get_pixmap(self, typ: widgets.wizard.WizardPixmapStr) -> Optional[gui.Pixmap]:
        if typ not in widgets.wizard.WIZARD_PIXMAP:
            raise InvalidParamError(typ, widgets.wizard.WIZARD_PIXMAP)
        pix = gui.Pixmap(self.pixmap(widgets.wizard.WIZARD_PIXMAP[typ]))
        if pix.isNull():
            return None
        return pix

    def set_button_text(self, button_type: widgets.wizard.WizardButtonStr, value: str):
        """Set text for given button type.

        Args:
            button_type: button to get text from
            value: text to set

        """
        if button_type not in widgets.wizard.WIZARD_BUTTON:
            raise InvalidParamError(button_type, widgets.wizard.WIZARD_BUTTON)
        self.setButtonText(widgets.wizard.WIZARD_BUTTON[button_type], value)

    def get_button_text(self, button_type: widgets.wizard.WizardButtonStr) -> str:
        """Return text for given button type.

        Args:
            button_type: button to get text from

        Returns:
            Button text
        """
        if button_type not in widgets.wizard.WIZARD_BUTTON:
            raise InvalidParamError(button_type, widgets.wizard.WIZARD_BUTTON)
        return self.buttonText(widgets.wizard.WIZARD_BUTTON[button_type])
