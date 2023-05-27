from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


class DockWidget(widgets.WidgetMixin, QtWidgets.QDockWidget):
    def __init__(self, *args, allowed_areas="all", **kwargs):
        super().__init__(*args, allowed_areas=allowed_areas, **kwargs)
        self._area = "none"
        self.dockLocationChanged.connect(self._on_location_change)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"allowedAreas": constants.DOCK_POSITIONS}
        return maps

    def set_widget(self, widget: QtWidgets.QWidget):
        self.setWidget(widget)

    def set_allowed_areas(self, area: constants.DockPositionsStr):
        self.setAllowedAreas(constants.DOCK_POSITIONS[area])

    def _on_location_change(self, area):
        self._area = constants.DOCK_POSITIONS.inverse[area]

    def get_current_area(self):
        return self._area

    def setup_title_bar(self):
        title_bar = widgets.Widget()
        layout = widgets.HBoxLayout()
        layout.set_margin(0)
        layout.set_alignment("right")
        title_bar.set_layout(layout)
        maximize_button = widgets.PushButton(clicked=self.maximize)
        layout.add(maximize_button)
        maximize_button.set_style_icon("titlebar_max_button")
        close_button = widgets.PushButton(clicked=self.close)
        close_button.set_style_icon("titlebar_close_button")
        layout.add(close_button)
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
    # dock_widget.setup_title_bar()
    win.add_dockwidget(dock_widget, "left")
    print(dock_widget.get_current_area())
    win.show()
    app.main_loop()
