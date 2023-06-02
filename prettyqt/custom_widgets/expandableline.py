from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class ExpandableLine(widgets.Widget):
    def __init__(
        self,
        title: str = "",
        animation_duration: int = 300,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._animation_duration = animation_duration

        self.expand_btn = widgets.ToolButton(
            arrow_type="right",
            tool_button_style="text_beside_icon",
            checkable=True,
            checked=False,
            text=title,
            toggled=self.expand_view,
        )
        with self.expand_btn.edit_stylesheet() as ss:
            ss.QToolButton.border.setValue(None)
        header_line = widgets.Frame(
            frame_shape="h_line",
            frame_shadow="sunken",
            size_policy=widgets.SizePolicy("expanding", "maximum"),
        )
        self.content_area = widgets.ScrollArea(
            maximum_height=1, size_policy=widgets.SizePolicy("expanding", "fixed")
        )
        with self.expand_btn.edit_stylesheet() as ss:
            ss.QAbstractScrollArea.border.setValue(None)
        # self.content_area.setMinimumHeight(0)

        self.toggle_anim = core.ParallelAnimationGroup()
        self.toggle_anim.set_duration(self._animation_duration)
        self.toggle_anim.add_property_animation(self.minimumHeight)
        self.toggle_anim.add_property_animation(self.maximumHeight)
        self.toggle_anim.add_property_animation(self.content_area.maximumHeight)
        base_layout = self.set_layout("grid", margin=0)
        base_layout.setVerticalSpacing(0)
        base_layout[0, 0] = self.expand_btn
        base_layout[0, 2] = header_line
        base_layout[1, 0:2] = self.content_area
        # self.toggle_anim.setStartValue(0)
        # self.toggle_anim.setEndValue(300)
        # === SIGNALS === #

    def expand_view(self, checked: bool):
        self.expand_btn.set_arrow_type("down" if checked else "right")
        self.toggle_anim.set_direction("forward" if checked else "backward")
        self.toggle_anim.start()

    def set_layout(
        self,
        layout: widgets.widget.LayoutStr | QtWidgets.QLayout | None,
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

    def set_animation_duration(self, duration: int):
        self._animation_duration = duration

    def get_animation_duration(self) -> int:
        return self._animation_duration

    animation_duration = core.Property(
        int, get_animation_duration, set_animation_duration
    )


if __name__ == "__main__":
    app = widgets.app()
    layout = widgets.VBoxLayout()
    layout.addWidget(widgets.TextBrowser())
    widget = ExpandableLine("Test")
    widget.set_layout(layout)
    widget.show()
    app.main_loop()
