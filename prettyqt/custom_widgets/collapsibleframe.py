from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class CollapsibleFrame(widgets.Frame):
    expanded = core.Signal()
    collapsed = core.Signal()

    def __init__(self, text: str = "", parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.set_frame_shape("styled_panel")
        self.set_frame_shadow("plain")
        # layout
        _layout = widgets.VBoxLayout()
        _layout.set_margin(0)
        _layout.setSpacing(0)
        self.setLayout(_layout)
        # button
        self._button = widgets.ToolButton(
            self,
            clicked=self.on_button_click,
            arrow_type="right",
            auto_raise=False,
            text=text,
            visible=True,
        )
        self._button.set_style("text_beside_icon")
        self.set_size_policy("minimum_expanding", "fixed")
        _layout.addWidget(self._button, 0)
        # group box
        self._panel = widgets.Widget(self, visible=False)
        _layout.addWidget(self._panel)
        self._panel_layout = widgets.VBoxLayout()
        self._panel_layout.set_margin(1)
        self._panel_layout.setSpacing(2)
        self._panel.setLayout(self._panel_layout)
        # connect signals
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
