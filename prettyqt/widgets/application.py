# -*- coding: utf-8 -*-
"""
"""

import pathlib
from typing import Optional
import logging

from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import colors

logger = logging.getLogger(__name__)

QtWidgets.QApplication.__bases__ = (gui.GuiApplication,)


class Application(QtWidgets.QApplication):
    def set_icon(self, icon: gui.icon.IconType):
        """set the default window icon

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon, color=colors.WINDOW_ICON_COLOR)
        self.setWindowIcon(icon)

    def load_language_file(self, path: pathlib.Path):
        translator = core.Translator(self)
        translator.load(str(path))
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

    def about_popup(self, title="About"):
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

    def main_loop(self):
        return self.exec_()

    @classmethod
    def use_hdpi_bitmaps(cls, state: bool = True):
        cls.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, state)

    @classmethod
    def disable_window_help_button(cls, state: bool = True):
        cls.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton, state)

    @classmethod
    def copy_to_clipboard(cls, text: str):
        """
        Sets clipboard to supplied text
        """
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
