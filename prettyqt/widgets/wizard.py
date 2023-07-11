from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from collections.abc import Iterator


mod = widgets.QWizard

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

WIZARD_BUTTON: bidict[WizardButtonStr, mod.WizardButton] = bidict(
    back=mod.WizardButton.BackButton,
    next=mod.WizardButton.NextButton,
    commit=mod.WizardButton.CommitButton,
    finish=mod.WizardButton.FinishButton,
    cancel=mod.WizardButton.CancelButton,
    help=mod.WizardButton.HelpButton,
    custom_1=mod.WizardButton.CustomButton1,
    custom_2=mod.WizardButton.CustomButton2,
    custom_3=mod.WizardButton.CustomButton3,
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

WIZARD_OPTIONS: bidict[WizardOptionStr, mod.WizardOption] = bidict(
    independent_pages=mod.WizardOption.IndependentPages,
    ignore_subtitles=mod.WizardOption.IgnoreSubTitles,
    extended_watermark_bitmap=mod.WizardOption.ExtendedWatermarkPixmap,
    no_default_button=mod.WizardOption.NoDefaultButton,
    no_back_button_on_start_page=mod.WizardOption.NoBackButtonOnStartPage,
    no_back_button_on_last_page=mod.WizardOption.NoBackButtonOnLastPage,
    disabled_back_button_on_last_page=mod.WizardOption.DisabledBackButtonOnLastPage,
    next_button_on_last_page=mod.WizardOption.HaveNextButtonOnLastPage,
    finish_button_on_early_pages=mod.WizardOption.HaveFinishButtonOnEarlyPages,
    no_cancel_button=mod.WizardOption.NoCancelButton,
    cancel_button_on_left=mod.WizardOption.CancelButtonOnLeft,
    help_button=mod.WizardOption.HaveHelpButton,
    help_button_on_right=mod.WizardOption.HelpButtonOnRight,
    custom_button_1=mod.WizardOption.HaveCustomButton1,
    custom_button_2=mod.WizardOption.HaveCustomButton2,
    custom_button_3=mod.WizardOption.HaveCustomButton3,
    no_cancel_button_on_last_page=mod.WizardOption.NoCancelButtonOnLastPage,
)

WizardPixmapStr = Literal["watermark", "logo", "banner", "background"]

WIZARD_PIXMAP: bidict[WizardPixmapStr, mod.WizardPixmap] = bidict(
    watermark=mod.WizardPixmap.WatermarkPixmap,
    logo=mod.WizardPixmap.LogoPixmap,
    banner=mod.WizardPixmap.BannerPixmap,
    background=mod.WizardPixmap.BackgroundPixmap,
)

WizardStyleStr = Literal["classic", "modern", "mac", "aero"]

WIZARD_STYLE: bidict[WizardStyleStr, mod.WizardStyle] = bidict(
    classic=mod.WizardStyle.ClassicStyle,
    modern=mod.WizardStyle.ModernStyle,
    mac=mod.WizardStyle.MacStyle,
    aero=mod.WizardStyle.AeroStyle,
)


class WizardMixin(widgets.DialogMixin):
    custom_button_1_clicked = core.Signal()
    custom_button_2_clicked = core.Signal()
    custom_button_3_clicked = core.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customButtonClicked.connect(self._on_custom_button_clicked)

    def __getitem__(self, key: int) -> widgets.QWizardPage:
        p = self.page(key)
        if p is None:
            raise KeyError(key)
        return p

    def __setitem__(self, key: int, value: widgets.QWizardPage):
        return self.setPage(key, value)

    def __delitem__(self, key: int):
        if key not in self.pageIds():
            raise KeyError(key)
        return self.removePage(key)

    def __iter__(self) -> Iterator[widgets.QWizardPage]:
        return iter(self.page(i) for i in self.pageIds())

    def __add__(self, other: widgets.QWizardPage) -> Wizard:
        self.addPage(other)
        return self

    def _on_custom_button_clicked(self, which: int):
        match which:
            case 6:
                self.custom_button_1_clicked.emit()
            case 7:
                self.custom_button_2_clicked.emit()
            case 8:
                self.custom_button_3_clicked.emit()

    def add_widget_as_page(self, widget: widgets.QWidget) -> None:
        page = widgets.WizardPage(self)
        layout = page.set_layout("vertical")
        layout += widget

    def set_title_format(self, fmt: constants.TextFormatStr | constants.TextFormat):
        """Set the title format.

        Allowed values are "rich", "plain", "auto", "markdown"

        Args:
            fmt: title format to use
        """
        self.setTitleFormat(constants.TEXT_FORMAT.get_enum_value(fmt))

    def get_title_format(self) -> constants.TextFormatStr:
        """Return current title format.

        Possible values: "rich", "plain", "auto", "markdown"

        Returns:
            title format
        """
        return constants.TEXT_FORMAT.inverse[self.titleFormat()]

    def set_subtitle_format(self, fmt: constants.TextFormatStr | constants.TextFormat):
        """Set the subtitle format.

        Allowed values are "rich", "plain", "auto", "markdown"

        Args:
            fmt: subtitle format to use
        """
        self.setSubTitleFormat(constants.TEXT_FORMAT.get_enum_value(fmt))

    def get_subtitle_format(self) -> constants.TextFormatStr:
        """Return current subtitle format.

        Possible values: "rich", "plain", "auto", "markdown"

        Returns:
            subtitle format
        """
        return constants.TEXT_FORMAT.inverse[self.subTitleFormat()]

    def get_button(
        self, button_type: WizardButtonStr | mod.WizardButton
    ) -> widgets.QAbstractButton:
        return self.button(WIZARD_BUTTON.get_enum_value(button_type))

    def set_button_text(
        self, button_type: WizardButtonStr | mod.WizardButton, value: str
    ):
        """Set text for given button type.

        Args:
            button_type: button to get text from
            value: text to set

        """
        self.setButtonText(WIZARD_BUTTON.get_enum_value(button_type), value)

    def get_button_text(self, button_type: WizardButtonStr | mod.WizardButton) -> str:
        """Return text for given button type.

        Args:
            button_type: button to get text from

        Returns:
            Button text
        """
        return self.buttonText(WIZARD_BUTTON.get_enum_value(button_type))

    def set_pixmap(
        self, typ: WizardPixmapStr | mod.WizardPixmap, pixmap: gui.QPixmap | None
    ):
        if pixmap is None:
            pixmap = gui.QPixmap()
        self.setPixmap(WIZARD_PIXMAP.get_enum_value(typ), pixmap)

    def get_pixmap(self, typ: WizardPixmapStr | mod.WizardPixmap) -> gui.Pixmap | None:
        pix = gui.Pixmap(self.pixmap(WIZARD_PIXMAP.get_enum_value(typ)))
        return None if pix.isNull() else pix

    def set_wizard_style(self, style: WizardStyleStr | mod.WizardStyle):
        """Set the wizard style.

        Args:
            style: wizard style
        """
        self.setWizardStyle(WIZARD_STYLE.get_enum_value(style))

    def get_wizard_style(self) -> WizardStyleStr:
        """Return current wizard style.

        Returns:
            Wizard style
        """
        return WIZARD_STYLE.inverse[self.wizardStyle()]

    def set_option(self, option: WizardOptionStr | mod.WizardOption, value: bool):
        """Set option to given value.

        Args:
            option: option to use
            value: value to set
        """
        self.setOption(WIZARD_OPTIONS.get_enum_value(option), value)

    def get_option(self, option: WizardOptionStr | mod.WizardOption) -> bool:
        """Return the value assigned to option.

        Args:
            option: option to get

        Returns:
            option
        """
        return self.testOption(WIZARD_OPTIONS.get_enum_value(option))

    def set_custom_button(
        self, button: Literal[1, 2, 3], text: str | None, callback: Callable | None = None
    ):
        self.set_option(f"custom_button_{button}", text is not None)
        if text is None:
            return
        self.setButtonText(WIZARD_BUTTON[f"custom_{button}"], text)
        if callback:
            match button:
                case 1:
                    self.custom_button_1_clicked.connect(callback)
                case 2:
                    self.custom_button_2_clicked.connect(callback)
                case 3:
                    self.custom_button_3_clicked.connect(callback)


class Wizard(WizardMixin, widgets.QWizard):
    """Framework for wizards."""


if __name__ == "__main__":
    app = widgets.app()
    dlg = Wizard()
    dlg.add_widget_as_page(widgets.RadioButton("test"))
    dlg.set_custom_button(1, "1", lambda: print("1"))
    dlg.set_custom_button(2, "2", lambda: print("2"))
    dlg.set_custom_button(3, "3", lambda: print("3"))
    dlg.show()
    app.exec()
