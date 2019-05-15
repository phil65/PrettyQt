# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class Wizard(QtWidgets.QWizard):

    def add_widget_as_page(self, widget):
        page = widgets.WizardPage(self)
        layout = widgets.BoxLayout("vertical", self)
        layout += widget
        page.setLayout(layout)


Wizard.__bases__[0].__bases__ = (widgets.BaseDialog,)


if __name__ == "__main__":
    app = widgets.app()
    dlg = Wizard()
    dlg.add_widget_as_page(widgets.RadioButton("test"))
    dlg.show()
    app.exec_()
