# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class WizardPage(QtWidgets.QWizardPage):
    pass


WizardPage.__bases__[0].__bases__ = (widgets.Widget,)
