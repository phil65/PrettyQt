# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import widgets

QtWidgets.QWizard.__bases__ = (widgets.BaseDialog,)


class Wizard(QtWidgets.QWizard):
    def add_widget_as_page(self, widget: QtWidgets.QWidget) -> None:
        page = widgets.WizardPage(self)
        layout = widgets.BoxLayout("vertical", self)
        layout += widget
        page.set_layout(layout)


if __name__ == "__main__":
    app = widgets.app()
    dlg = Wizard()
    dlg.add_widget_as_page(widgets.RadioButton("test"))
    dlg.show()
    app.exec_()
