from typing import Optional

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets


class ExpandableLine(widgets.Widget):
    def __init__(
        self,
        title: str = "",
        animation_duration: int = 300,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent=parent)

        self._animation_duration = animation_duration

        base_layout = widgets.GridLayout()
        base_layout.setVerticalSpacing(0)
        base_layout.set_margin(0)
        self.setLayout(base_layout)

        self.expand_btn = widgets.ToolButton()
        self.expand_btn.set_text(title)
        with self.expand_btn.edit_stylesheet() as ss:
            ss.QToolButton.border.setValue(None)
        self.expand_btn.set_style("text_beside_icon")
        self.expand_btn.set_arrow_type("right")
        self.expand_btn.setCheckable(True)
        self.expand_btn.setChecked(False)

        header_line = widgets.Frame()
        header_line.set_frame_shape("h_line")
        header_line.set_frame_shadow("sunken")
        header_line.set_size_policy("expanding", "maximum")

        self.content_area = widgets.ScrollArea()
        with self.expand_btn.edit_stylesheet() as ss:
            print(dir(ss))
            ss.QAbstractScrollArea.border.setValue(None)
        self.content_area.set_size_policy("expanding", "fixed")
        self.content_area.setMaximumHeight(1)
        # self.content_area.setMinimumHeight(0)

        self.toggle_anim = core.ParallelAnimationGroup()
        self.toggle_anim.add_property_animation(self, "minimumHeight")
        self.toggle_anim.add_property_animation(self, "maximumHeight")
        self.toggle_anim.add_property_animation(self.content_area, "maximumHeight")
        base_layout.addWidget(self.expand_btn, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        base_layout[0, 2] = header_line
        base_layout[1, 0:2] = self.content_area
        # self.toggle_anim.setStartValue(0)
        # self.toggle_anim.setEndValue(300)

        def expand_view(checked):
            arrow_type = "down" if checked else "right"
            direction = "forward" if checked else "backward"
            self.expand_btn.set_arrow_type(arrow_type)
            self.toggle_anim.set_direction(direction)
            self.toggle_anim.start()

        # === SIGNALS === #
        self.expand_btn.toggled.connect(expand_view)
        self.toggle_anim.set_duration(0)
        self.toggle_anim.set_duration(self._animation_duration)

    def set_layout(self, content_layout):
        self.content_area.destroy()
        self.content_area.setLayout(content_layout)
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = content_layout.sizeHint().height() + 300
        for expand_anim in self.toggle_anim[:-1]:
            # expand_anim.setDuration(self._animation_duration)
            expand_anim.setStartValue(collapsed_height)
            expand_anim.setEndValue(collapsed_height + content_height)
        content_anim = self.toggle_anim[-1]
        content_anim.setStartValue(1)
        content_anim.setEndValue(content_height)


if __name__ == "__main__":
    app = widgets.app()
    layout = widgets.BoxLayout("vertical")
    layout.addWidget(widgets.TextBrowser())
    widget = ExpandableLine("Test")
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
