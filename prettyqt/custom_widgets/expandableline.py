from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtWidgets


class ExpandableLine(widgets.Widget):
    def __init__(
        self,
        title: str = "",
        animation_duration: int = 300,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._animation_duration = animation_duration

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
            ss.QAbstractScrollArea.border.setValue(None)
        self.content_area.set_size_policy("expanding", "fixed")
        self.content_area.setMaximumHeight(1)
        # self.content_area.setMinimumHeight(0)

        self.toggle_anim = core.ParallelAnimationGroup()
        self.toggle_anim.add_property_animation(self, "minimumHeight")
        self.toggle_anim.add_property_animation(self, "maximumHeight")
        self.toggle_anim.add_property_animation(self.content_area, "maximumHeight")
        base_layout = widgets.GridLayout()
        base_layout.setVerticalSpacing(0)
        base_layout.set_margin(0)
        base_layout.addWidget(
            self.expand_btn, 0, 0, 1, 1, constants.ALIGN_LEFT
        )  # type: ignore
        base_layout[0, 2] = header_line
        base_layout[1, 0:2] = self.content_area
        self.setLayout(base_layout)
        # self.toggle_anim.setStartValue(0)
        # self.toggle_anim.setEndValue(300)

        def expand_view(checked: bool):
            self.expand_btn.set_arrow_type("down" if checked else "right")
            self.toggle_anim.set_direction("forward" if checked else "backward")
            self.toggle_anim.start()

        # === SIGNALS === #
        self.expand_btn.toggled.connect(expand_view)
        self.toggle_anim.set_duration(0)
        self.toggle_anim.set_duration(self._animation_duration)

    def set_layout(
        self,
        layout: str | QtWidgets.QLayout | None,
        margin: int | None = None,
        spacing: int | None = None,
    ) -> None:
        self.content_area.destroy()
        self.content_area.set_layout(layout, margin=margin, spacing=spacing)
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = self.content_area.box.sizeHint().height() + 300
        for expand_anim in self.toggle_anim[:-1]:
            # expand_anim.setDuration(self._animation_duration)
            expand_anim.set_range(collapsed_height, collapsed_height + content_height)
        content_anim = self.toggle_anim[-1]
        content_anim.set_range(1, content_height)


if __name__ == "__main__":
    app = widgets.app()
    layout = widgets.BoxLayout("vertical")
    layout.addWidget(widgets.TextBrowser())
    widget = ExpandableLine("Test")
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
