from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets

DockWidgetArea = constants.DockWidgetArea


class AdjustingBoxLayoutDockWidget(widgets.DockWidget):
    """DockWidget adjusting its child widget QBoxLayout direction.

    The child widget layout direction is set according to dock widget area.
    The child widget MUST use a QBoxLayout.
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._current_area = DockWidgetArea.NoDockWidgetArea
        self.dockLocationChanged.connect(self._dock_location_changed)
        self.topLevelChanged.connect(self._top_level_changed)

    def setWidget(self, widget):
        """Set the widget of this QDockWidget."""
        super().setWidget(widget)
        self._dock_location_changed(self._current_area)

    def _dock_location_changed(self, area: DockWidgetArea):
        self._current_area = area
        if (widget := self.widget()) is not None:
            if isinstance(layout := widget.layout(), QtWidgets.QBoxLayout):
                if area in (
                    DockWidgetArea.LeftDockWidgetArea,
                    DockWidgetArea.RightDockWidgetArea,
                ):
                    direction = widgets.BoxLayout.Direction.TopToBottom
                else:
                    direction = widgets.BoxLayout.Direction.LeftToRight
                layout.setDirection(direction)
                self.resize(widget.minimumSize())
                self.adjustSize()

    def _top_level_changed(self, top_level):
        if (widget := self.widget()) is not None and top_level:
            if isinstance(layout := widget.layout(), QtWidgets.QBoxLayout):
                layout.setDirection(widgets.BoxLayout.Direction.LeftToRight)
                self.resize(widget.minimumSize())
                self.adjustSize()

    def showEvent(self, event):
        """Make sure this dock widget is raised when it is shown.

        This is useful for tabbed dock widgets.
        """
        self.raise_()


if __name__ == "__main__":
    app = widgets.app()
    mainwindow = widgets.MainWindow()
    dockwidget = AdjustingBoxLayoutDockWidget()
    textbox1 = widgets.PlainTextEdit()
    textbox2 = widgets.PlainTextEdit()
    container = widgets.Widget()
    container.set_layout("horizontal")
    container.set_layout(None)
    container.set_layout("horizontal")
    container.box.add(textbox1)
    dockwidget.setWidget(container)
    mainwindow.add_dockwidget(dockwidget)
    mainwindow.show()
    with app.debug_mode():
        app.exec()
