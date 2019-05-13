# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""


from qtpy import QtCore, QtWidgets

from prettyqt import widgets

ALLOWED_AREAS = dict(all=QtCore.Qt.AllDockWidgetAreas,
                     left=QtCore.Qt.LeftDockWidgetArea,
                     right=QtCore.Qt.RightDockWidgetArea,
                     top=QtCore.Qt.TopDockWidgetArea,
                     bottom=QtCore.Qt.BottomDockWidgetArea)


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
        self.set_allowed_areas("all")

    def set_allowed_areas(self, area):
        self.setAllowedAreas(ALLOWED_AREAS[area])

    def setup_title_bar(self):
        title_bar = widgets.Widget()
        layout = widgets.BoxLayout("horizontal")
        layout.set_margin(0)
        layout.set_alignment("right")
        title_bar.setLayout(layout)
        maximise_button = widgets.PushButton()
        layout += maximise_button
        maximise_button.set_style_icon("maximise")
        maximise_button.clicked.connect(self.maximise)
        close_button = widgets.PushButton()
        close_button.set_style_icon("close")
        layout += close_button
        close_button.clicked.connect(self.close)
        self.setTitleBarWidget(title_bar)

    def maximise(self):
        if not self.isFloating():
            self.setFloating(True)
        if not self.isMaximized():
            self.showMaximized()
        else:
            self.showMinimized()


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    win = widgets.MainWindow()
    dock_widget = DockWidget(name="aa", title="Test")
    dock_widget.setup_title_bar()
    win.add_dockwidget(dock_widget, "left")
    win.show()
    app.exec_()
