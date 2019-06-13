# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QWizardPage.__bases__ = (widgets.Widget,)


class WizardPage(QtWidgets.QWizardPage):
    pass
