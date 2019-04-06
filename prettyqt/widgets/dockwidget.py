# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""


from qtpy import QtWidgets, QtCore
from prettyqt import widgets


class DockWidget(QtWidgets.QDockWidget):
    """
    Customized DockWidget class
    contains a custom TitleBar with maximise button
    """

    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)
        title = kwargs.pop("title", None)
        super().__init__(*args, **kwargs)
        if name:
            self.setObjectName(name)
        if title:
            self.setWindowTitle(title)
        self.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)

    def setup_title_bar(self):
        title_bar = widgets.Widget()
        layout = widgets.BoxLayout("horizontal")
        layout.set_alignment("right")
        title_bar.setLayout(layout)
        maximise_button = widgets.PushButton()
        layout.addWidget(maximise_button)
        maximise_button.set_style_icon("maximise")
        maximise_button.clicked.connect(self.maximise)
        close_button = widgets.PushButton()
        close_button.set_style_icon("close")
        layout.addWidget(close_button)
        close_button.clicked.connect(self.close)
        self.setTitleBarWidget(title_bar)

    def maximise(self):
        if not self.isFloating():
            self.setFloating(True)
        self.showMaximized()


if __name__ == "__main__":
    import sys
    app = widgets.Application(sys.argv)
    win = widgets.MainWindow()
    dock_widget = DockWidget(name="aa", title="Test")
    dock_widget.setup_title_bar()
    win.addDockWidget(QtCore.Qt.DockWidgetArea(1), dock_widget)
    win.show()
    app.exec_()
