# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""


from qtpy import QtWidgets, QtCore


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
        title_bar = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignRight)
        title_bar.setLayout(layout)
        maximise_button = QtWidgets.QPushButton()
        layout.addWidget(maximise_button)
        style = QtWidgets.QStyle.SP_TitleBarMaxButton
        icon = maximise_button.style().standardIcon(style, None, maximise_button)
        maximise_button.setIcon(icon)
        maximise_button.clicked.connect(self.maximise)
        close_button = QtWidgets.QPushButton()
        layout.addWidget(close_button)
        style = QtWidgets.QStyle.SP_TitleBarCloseButton
        icon = close_button.style().standardIcon(style, None, close_button)
        close_button.setIcon(icon)
        close_button.clicked.connect(self.close)
        # self.setTitleBarWidget(title_bar)

    def maximise(self):
        if not self.isFloating():
            self.setFloating(True)
        self.showMaximized()
