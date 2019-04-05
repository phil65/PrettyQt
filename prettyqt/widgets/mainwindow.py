# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys

from prettyqt import widgets
from qtpy import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    """
    Class for our mainWindow
    includes all docks, a centralwidget and a toolbar
    """

    # def load_window_state(self):
    #     prefix = os.environ["QT_API"]
    #     geom = application.settings.get(f"{prefix}.geometry",
    #                                     self.saveGeometry())
    #     state = application.settings.get(f"{prefix}.state",
    #                                      self.saveState())
    #     self.restoreGeometry(geom)
    #     self.restoreState(state)

    # def closeEvent(self, event):
    #     """
    #     override, gets executed when app gets closed.
    #     saves GUI settings
    #     """
    #     prefix = os.environ["QT_API"]
    #     application.settings[f"{prefix}.geometry"] = self.saveGeometry()
    #     application.settings[f"{prefix}.state"] = self.saveState()
    #     super().closeEvent(event)
    #     event.accept()

    def add_dockwidget(self,
                       name: str,
                       title: str,
                       vertical: bool = True,
                       position: int = 1) -> widgets.DockWidget:
        dock_widget = widgets.DockWidget(self, name=name, title=title)
        widget = QtWidgets.QWidget()
        widget.setObjectName(f"{name}.widget")
        if vertical:
            layout = QtWidgets.QVBoxLayout(widget)
        else:
            layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        dock_widget.setWidget(widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(position), dock_widget)
        dock_widget.layout = layout
        return dock_widget

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


if __name__ == "__main__":
    app = widgets.Application(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
