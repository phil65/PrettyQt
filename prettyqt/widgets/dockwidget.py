from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


class CustomTitleBar(widgets.Widget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        layout = self.set_layout("horizontal", margin=0, spacing=0)
        layout.set_alignment("right")
        maximize_button = widgets.PushButton(clicked=parent.maximize)
        maximize_button.set_style_icon("titlebar_max_button", size=12)
        close_button = widgets.PushButton(clicked=parent.close)
        close_button.set_style_icon("titlebar_close_button", size=12)
        layout.add(widgets.Label(parent.windowTitle()))
        layout.add(maximize_button)
        layout.add(close_button)


class DockWidget(widgets.WidgetMixin, QtWidgets.QDockWidget):
    def __init__(self, *args, allowed_areas="all", **kwargs):
        super().__init__(*args, allowed_areas=allowed_areas, **kwargs)
        self._area: constants.DockWidgetAreasStr = "none"
        self.dockLocationChanged.connect(self._on_location_change)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"allowedAreas": constants.DOCK_WIDGET_AREAS}
        return maps

    def set_widget(self, widget: QtWidgets.QWidget):
        self.setWidget(widget)

    def set_allowed_areas(self, area: constants.DockWidgetAreasStr):
        self.setAllowedAreas(constants.DOCK_WIDGET_AREAS[area])

    def _on_location_change(self, area: constants.DockWidgetArea):
        self._area = constants.DOCK_WIDGET_AREAS.inverse[area]

    def get_current_area(self) -> constants.DockWidgetAreasStr:
        return self._area

    def setup_title_bar(self):
        title_bar = CustomTitleBar(parent=self)
        self.setTitleBarWidget(title_bar)

    def maximize(self):
        if not self.isFloating():
            self.setFloating(True)
        if not self.isMaximized():
            self.showMaximized()
        else:
            self.showMinimized()


if __name__ == "__main__":
    app = widgets.app()
    win = widgets.MainWindow()
    dock_widget = DockWidget(window_title="Test")
    dock_widget.setup_title_bar()
    win.add_dockwidget(dock_widget, "left")
    win.show()
    app.exec()
