from __future__ import annotations

from typing import Iterator, Literal

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import InvalidParamError, bidict


WIZARD_BUTTON = bidict(
    back=QtWidgets.QWizard.BackButton,
    next=QtWidgets.QWizard.NextButton,
    commit=QtWidgets.QWizard.CommitButton,
    finish=QtWidgets.QWizard.FinishButton,
    cancel=QtWidgets.QWizard.CancelButton,
    help=QtWidgets.QWizard.HelpButton,
    custom_1=QtWidgets.QWizard.CustomButton1,
    custom_2=QtWidgets.QWizard.CustomButton2,
    custom_3=QtWidgets.QWizard.CustomButton3,
)

WizardButtonStr = Literal[
    "back",
    "next",
    "commit",
    "finish",
    "cancel",
    "help",
    "custom_1",
    "custom_2",
    "custom_3",
]

WIZARD_OPTIONS = bidict(
    independent_pages=QtWidgets.QWizard.IndependentPages,
    ignore_subtitles=QtWidgets.QWizard.IgnoreSubTitles,
    extended_watermark_bitmap=QtWidgets.QWizard.ExtendedWatermarkPixmap,
    no_default_button=QtWidgets.QWizard.NoDefaultButton,
    no_back_button_on_start_page=QtWidgets.QWizard.NoBackButtonOnStartPage,
    no_back_button_on_last_page=QtWidgets.QWizard.NoBackButtonOnLastPage,
    disabled_back_button_on_last_page=QtWidgets.QWizard.DisabledBackButtonOnLastPage,
    next_button_on_last_page=QtWidgets.QWizard.HaveNextButtonOnLastPage,
    finish_button_on_early_pages=QtWidgets.QWizard.HaveFinishButtonOnEarlyPages,
    no_cancel_button=QtWidgets.QWizard.NoCancelButton,
    cancel_button_on_left=QtWidgets.QWizard.CancelButtonOnLeft,
    help_button=QtWidgets.QWizard.HaveHelpButton,
    help_button_on_right=QtWidgets.QWizard.HelpButtonOnRight,
    custom_button_1=QtWidgets.QWizard.HaveCustomButton1,
    custom_button_2=QtWidgets.QWizard.HaveCustomButton2,
    custom_button_3=QtWidgets.QWizard.HaveCustomButton3,
    no_cancel_button_on_last_page=QtWidgets.QWizard.NoCancelButtonOnLastPage,
)

WizardOptionStr = Literal[
    "independent_pages",
    "ignore_subtitles",
    "extended_watermark_bitmap",
    "no_default_button",
    "no_back_button_on_start_page",
    "no_back_button_on_last_page",
    "disabled_back_button_on_last_page",
    "next_button_on_last_page",
    "finish_button_on_early_pages",
    "no_cancel_button",
    "cancel_button_on_left",
    "help_button",
    "help_button_on_right",
    "custom_button_1",
    "custom_button_2",
    "custom_button_3",
    "no_cancel_button_on_last_page",
]

WIZARD_PIXMAP = bidict(
    watermark=QtWidgets.QWizard.WatermarkPixmap,
    logo=QtWidgets.QWizard.LogoPixmap,
    banner=QtWidgets.QWizard.BannerPixmap,
    background=QtWidgets.QWizard.BackgroundPixmap,
)

WizardPixmapStr = Literal["watermark", "logo", "banner", "background"]

WIZARD_STYLE = bidict(
    classic=QtWidgets.QWizard.ClassicStyle,
    modern=QtWidgets.QWizard.ModernStyle,
    mac=QtWidgets.QWizard.MacStyle,
    aero=QtWidgets.QWizard.AeroStyle,
)

WizardStyleStr = Literal["classic", "modern", "mac", "aero"]

TEXT_FORMATS = bidict(
    rich=QtCore.Qt.RichText, plain=QtCore.Qt.PlainText, auto=QtCore.Qt.AutoText
)

if core.VersionNumber.get_qt_version() >= (5, 14, 0):
    TEXT_FORMATS["markdown"] = QtCore.Qt.MarkdownText

QtWidgets.QWizard.__bases__ = (widgets.BaseDialog,)


class Wizard(QtWidgets.QWizard):
    def __getitem__(self, key: int) -> QtWidgets.QWizardPage:
        return self.page(key)

    def __setitem__(self, key: int, value: QtWidgets.QWizardPage):
        return self.setPage(key, value)

    def __delitem__(self, key: int):
        return self.removePage(key)

    def __iter__(self) -> Iterator[QtWidgets.QWizardPage]:
        return iter(self.page(i) for i in self.pageIds())

    def __add__(self, other: QtWidgets.QWizardPage) -> Wizard:
        self.addPage(other)
        return self

    def add_widget_as_page(self, widget: QtWidgets.QWidget) -> None:
        page = widgets.WizardPage(self)
        layout = widgets.BoxLayout("vertical", self)
        layout += widget
        page.set_layout(layout)

    def set_title_format(self, fmt: str):
        """Set the title format.

        Allowed values are "rich", "plain", "auto", "markdown"

        Args:
            fmt: title format to use

        Raises:
            InvalidParamError: title format does not exist
        """
        if fmt not in TEXT_FORMATS:
            raise InvalidParamError(fmt, TEXT_FORMATS)
        self.setTitleFormat(TEXT_FORMATS[fmt])

    def get_title_format(self) -> str:
        """Return current title format.

        Possible values: "rich", "plain", "auto", "markdown"

        Returns:
            title format
        """
        return TEXT_FORMATS.inverse[self.titleFormat()]

    def set_subtitle_format(self, fmt: str):
        """Set the subtitle format.

        Allowed values are "rich", "plain", "auto", "markdown"

        Args:
            fmt: subtitle format to use

        Raises:
            InvalidParamError: subtitle format does not exist
        """
        if fmt not in TEXT_FORMATS:
            raise InvalidParamError(fmt, TEXT_FORMATS)
        self.setSubTitleFormat(TEXT_FORMATS[fmt])

    def get_subtitle_format(self) -> str:
        """Return current subtitle format.

        Possible values: "rich", "plain", "auto", "markdown"

        Returns:
            subtitle format
        """
        return TEXT_FORMATS.inverse[self.subTitleFormat()]

    def get_button(self, button_type: str) -> QtWidgets.QAbstractButton:
        if button_type not in WIZARD_BUTTON:
            raise InvalidParamError(button_type, WIZARD_BUTTON)
        return self.button(WIZARD_BUTTON[button_type])

    def set_button_text(self, button_type: WizardButtonStr, value: str) -> str:
        """Set text for given button type.

        Args:
            button_type: button to get text from
            value: text to set

        """
        if button_type not in WIZARD_BUTTON:
            raise InvalidParamError(button_type, WIZARD_BUTTON)
        return self.setButtonText(WIZARD_BUTTON[button_type], value)

    def get_button_text(self, button_type: WizardButtonStr) -> str:
        """Return text for given button type.

        Args:
            button_type: button to get text from

        Returns:
            Button text
        """
        if button_type not in WIZARD_BUTTON:
            raise InvalidParamError(button_type, WIZARD_BUTTON)
        return self.buttonText(WIZARD_BUTTON[button_type])

    def set_pixmap(self, typ: WizardPixmapStr, pixmap: QtGui.QPixmap):
        if typ not in WIZARD_PIXMAP:
            raise InvalidParamError(typ, WIZARD_PIXMAP)
        self.setPixmap(WIZARD_PIXMAP[typ], pixmap)

    def get_pixmap(self, typ: WizardPixmapStr) -> gui.Pixmap:
        if typ not in WIZARD_PIXMAP:
            raise InvalidParamError(typ, WIZARD_PIXMAP)
        return gui.Pixmap(self.pixmap(WIZARD_PIXMAP[typ]))

    def set_wizard_style(self, style: WizardStyleStr):
        """Set the wizard style.

        Args:
            style: wizard style

        Raises:
            InvalidParamError: wizard style does not exist
        """
        if style not in WIZARD_STYLE:
            raise InvalidParamError(style, WIZARD_STYLE)
        self.setWizardStyle(WIZARD_STYLE[style])

    def get_wizard_style(self) -> WizardStyleStr:
        """Return current wizard style.

        Returns:
            Wizard style
        """
        return WIZARD_STYLE.inverse[self.wizardStyle()]

    def set_option(self, option: WizardOptionStr, value: bool):
        """Set option to given value.

        Args:
            option: option to use
            value: value to set

        Raises:
            InvalidParamError: option does not exist
        """
        if option not in WIZARD_OPTIONS:
            raise InvalidParamError(option, WIZARD_OPTIONS)
        self.setOption(WIZARD_OPTIONS[option], value)

    def get_option(self, option: WizardOptionStr) -> bool:
        """Return the value assigned to option.

        Args:
            option: option to get

        Returns:
            option
        """
        if option not in WIZARD_OPTIONS:
            raise InvalidParamError(option, WIZARD_OPTIONS)
        return self.testOption(WIZARD_OPTIONS[option])


if __name__ == "__main__":
    app = widgets.app()
    dlg = Wizard()
    dlg.add_widget_as_page(widgets.RadioButton("test"))
    dlg.show()
    app.main_loop()
