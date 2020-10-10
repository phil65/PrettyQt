# -*- coding: utf-8 -*-

import pathlib
from typing import Optional, Union, Iterator
import logging

from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict, colors, InvalidParamError

logger = logging.getLogger(__name__)

STANDARD_PIXMAPS = widgets.style.STANDARD_PIXMAPS

QtWidgets.QApplication.__bases__ = (gui.GuiApplication,)

UI_EFFECTS = bidict(
    animate_menu=QtCore.Qt.UI_AnimateMenu,
    fade_menu=QtCore.Qt.UI_FadeMenu,
    animate_combo=QtCore.Qt.UI_AnimateCombo,
    animate_tooltip=QtCore.Qt.UI_AnimateTooltip,
    fade_tooltip=QtCore.Qt.UI_FadeTooltip,
    animate_toolbox=QtCore.Qt.UI_AnimateToolBox,
)

NAVIGATION_MODES = bidict(
    none=QtCore.Qt.NavigationModeNone,
    keypad_tab_order=QtCore.Qt.NavigationModeKeypadTabOrder,
    keypad_directional=QtCore.Qt.NavigationModeKeypadDirectional,
    cursor_auto=QtCore.Qt.NavigationModeCursorAuto,
    cursor_force_visible=QtCore.Qt.NavigationModeCursorForceVisible,
)


class Application(QtWidgets.QApplication):
    def __class_getitem__(cls, name: str) -> QtWidgets.QWidget:
        widget = cls.get_widget(name)
        if widget is None:
            raise ValueError(f"Widget {name!r} does not exist.")
        return widget

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.topLevelWidgets())

    def set_icon(self, icon: gui.icon.IconType):
        """Set the default window icon.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon, color=colors.WINDOW_ICON_COLOR)
        self.setWindowIcon(icon)

    def load_language_file(self, file: Union[pathlib.Path, str]):
        translator = core.Translator(self)
        if file in ["de", "fr"]:
            path = pathlib.Path(__file__).parent.parent
            file = path / "localization" / f"qtbase_{file}.ts"
        translator.load(str(file))
        self.installTranslator(translator)

    def set_metadata(
        self,
        app_name: Optional[str] = None,
        app_version: Optional[str] = None,
        org_name: Optional[str] = None,
        org_domain: Optional[str] = None,
    ):
        if app_name:
            self.setApplicationName(app_name)
        if app_version:
            self.setApplicationVersion(app_name)
        if org_name:
            self.setOrganizationName(org_name)
        if org_domain:
            self.setOrganizationDomain(org_domain)

    def about_popup(self, title: str = "About"):
        text = (
            f"{self.applicationName()}\n\n"
            f"{self.organizationName()}\n"
            f"{self.applicationVersion()}\n"
            f"{self.organizationDomain()}"
        )
        popup = widgets.MessageBox(
            widgets.MessageBox.NoIcon, title, text, buttons=widgets.MessageBox.Ok
        )
        popup.set_icon("mdi.information-outline")
        popup.exec_()

    def main_loop(self) -> int:
        return self.exec_()

    @classmethod
    def use_hdpi_bitmaps(cls, state: bool = True):
        cls.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, state)

    @classmethod
    def disable_window_help_button(cls, state: bool = True):
        cls.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton, state)

    @classmethod
    def copy_to_clipboard(cls, text: str):
        """Sets clipboard to supplied text."""
        cb = cls.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)

    @classmethod
    def get_mainwindow(cls) -> Optional[QtWidgets.QMainWindow]:
        widget_list = cls.instance().topLevelWidgets()
        for widget in widget_list:
            if isinstance(widget, QtWidgets.QMainWindow):
                return widget
        return None

    @classmethod
    def get_widget(cls, name: str) -> Optional[QtWidgets.QWidget]:
        mw = cls.get_mainwindow()
        if mw is None:
            logger.warning("Trying to get widget from nonexistent mainwindow")
            return None
        return mw.findChild(QtWidgets.QWidget, name)
        # widget_list = cls.instance().allWidgets()
        # for widget in widget_list:
        #     if isinstance(widget, QtWidgets.QWidget) and widget.objectName() == name:
        #         return widget
        # return None

    @classmethod
    def get_icon(cls, icon: str) -> gui.Icon:
        style = cls.style()
        # icon_size = style.pixelMetric(QtWidgets.QStyle.PM_MessageBoxIconSize)
        if icon not in STANDARD_PIXMAPS:
            raise InvalidParamError(icon, STANDARD_PIXMAPS)
        icon = style.standardIcon(STANDARD_PIXMAPS[icon])
        return gui.Icon(icon)

    def set_effect_enabled(self, effect: str, enabled: bool = True):
        """Set the enabled state of a desktop effect.

        valid values are: "animate_menu", "fade_menu", "animate_combo",
        "animate_tooltip", "fade_tooltip", "animate_toolbox"

        Args:
            effect: desktop effect to set
            enabled: new state

        Raises:
            InvalidParamError: invalid desktop effect
        """
        if effect not in UI_EFFECTS:
            raise InvalidParamError(effect, UI_EFFECTS)
        self.setEffectEnabled(UI_EFFECTS[effect])

    def is_effect_enabled(self, effect: str) -> str:
        """Return desktop effect state.

        possible values are "animate_menu", "fade_menu", "animate_combo",
        "animate_tooltip", "fade_tooltip", "animate_toolbox"

        Returns:
            desktop effect state
        """
        return self.isEffectEnabled(UI_EFFECTS[effect])

    def set_navigation_mode(self, mode: str):
        """Set the navigation mode.

        valid values: "none", "keypad_tab_order", "keypad_directional", "cursor_auto",
        "cursor_force_visible"

        Args:
            mode: navigation mode to use

        Raises:
            InvalidParamError: invalid navigation mode
        """
        if mode not in NAVIGATION_MODES:
            raise InvalidParamError(mode, NAVIGATION_MODES)
        self.setNavigationMode(NAVIGATION_MODES[mode])

    def get_navigation_mode(self) -> str:
        """Return navigation mode.

        possible values: "none", "keypad_tab_order", "keypad_directional", "cursor_auto",
        "cursor_force_visible"

        Returns:
            navigation mode
        """
        return NAVIGATION_MODES.inv[self.navigationMode()]


if __name__ == "__main__":
    app = Application([])
    app.load_language_file("de")
