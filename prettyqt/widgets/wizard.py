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


if __name__ == "__main__":
    import sys
    app = widgets.Application(sys.argv)
    dlg = Wizard()
    dlg.add_widget_as_page(widgets.RadioButton("test"))
    dlg.show()
    sys.exit(app.exec_())
