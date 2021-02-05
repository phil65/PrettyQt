from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class CollapsibleFrame(widgets.Frame):

    expanded = core.Signal()
    collapsed = core.Signal()

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.set_frame_shape("styled_panel")
        self.set_frame_shadow("plain")
        # layout
        self._layout = widgets.BoxLayout("vertical")
        self._layout.set_margin(0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        # button
        self._button = widgets.ToolButton(self)
        self._button.set_arrow_type("right")
        self._button.set_style("text_beside_icon")
        self._button.setAutoRaise(False)
        self._button.set_text("CollapsibleFrame")
        self.set_size_policy("minimum_expanding", "fixed")
        self._layout.addWidget(self._button, 0)
        self._button.setVisible(True)
        # group box
        self._panel = widgets.Widget(self)
        self._layout.addWidget(self._panel)
        self._panel.setVisible(False)
        self._panel_layout = widgets.BoxLayout("vertical")
        self._panel_layout.set_margin(1)
        self._panel_layout.setSpacing(2)
        self._panel.setLayout(self._panel_layout)
        # connect signals
        self._button.clicked.connect(self.on_button_click)
        # private state variables
        self._is_collapsed = True

    def set_title(self, title: str):
        self._button.set_text(title)

    def add_widget(self, widget: widgets.Widget):
        self._panel_layout.addWidget(widget)

    def remove_widget(self, widget: widgets.Widget):
        self._panel_layout.removeWidget(widget)

    def is_expanded(self) -> bool:
        return not self._is_collapsed

    def expand(self):
        self._button.set_arrow_type("down")
        self._panel.setVisible(True)
        self._is_collapsed = False
        self.set_size_policy("minimum_expanding", "minimum_expanding")

    def collapse(self):
        self._panel.setVisible(False)
        self._button.set_arrow_type("right")
        self._is_collapsed = True
        self.set_size_policy("preferred", "preferred")

    @core.Slot()
    def on_button_click(self):
        if self._is_collapsed:
            self.expand()
            self.expanded.emit()
        else:
            self.collapse()
            self.collapsed.emit()


if __name__ == "__main__":
    app = widgets.app()
    widget = CollapsibleFrame()
    widget.add_widget(widgets.Label("test"))
    widget.show()
    app.main_loop()
