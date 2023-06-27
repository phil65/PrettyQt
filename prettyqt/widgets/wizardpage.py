from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtGui, QtWidgets


class WizardPageMixin(widgets.WidgetMixin):
    def set_pixmap(
        self,
        typ: widgets.wizard.WizardPixmapStr | widgets.QWizard.WizardPixmap,
        pixmap: QtGui.QPixmap | None,
    ):
        if pixmap is None:
            pixmap = QtGui.QPixmap()
        self.setPixmap(widgets.wizard.WIZARD_PIXMAP.get_enum_value(typ), pixmap)

    def get_pixmap(
        self, typ: widgets.wizard.WizardPixmapStr | widgets.QWizard.WizardPixmap
    ) -> gui.Pixmap | None:
        pix = gui.Pixmap(self.pixmap(widgets.wizard.WIZARD_PIXMAP.get_enum_value(typ)))
        return None if pix.isNull() else pix

    def set_button_text(
        self,
        button_type: widgets.wizard.WizardButtonStr | widgets.QWizard.WizardPixmap,
        value: str,
    ):
        """Set text for given button type.

        Args:
            button_type: button to get text from
            value: text to set

        """
        self.setButtonText(
            widgets.wizard.WIZARD_BUTTON.get_enum_value(button_type), value
        )

    def get_button_text(
        self, button_type: widgets.wizard.WizardButtonStr | widgets.QWizard.WizardButton
    ) -> str:
        """Return text for given button type.

        Args:
            button_type: button to get text from

        Returns:
            Button text
        """
        return self.buttonText(widgets.wizard.WIZARD_BUTTON.get_enum_value(button_type))


class WizardPage(WizardPageMixin, QtWidgets.QWizardPage):
    pass
