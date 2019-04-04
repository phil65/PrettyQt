# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore
import qtawesome as qta


class Application(QtWidgets.QApplication):

    def set_icon(self, icon):
        if icon:
            if isinstance(icon, str):
                icon = qta.icon(icon, color="lightgray")
            self.setWindowIcon(icon)

    def load_language_file(self, path):
        translator = QtCore.QTranslator(self)
        translator.load(str(path))
        self.installTranslator(translator)

    def set_metadata(self, app_name=None, org_name=None, org_domain=None):
        if app_name:
            self.setApplicationName(app_name)
        if org_name:
            self.setOrganizationName(org_name)
        if org_domain:
            self.setOrganizationDomain(org_domain)

    @classmethod
    def use_hdpi_bitmaps(cls):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    @classmethod
    def disable_window_help_button(cls):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
