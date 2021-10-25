from __future__ import annotations

from prettyqt import core, custom_animations, widgets
from prettyqt.qt import QtCore, QtWidgets


class AnimatedToolTipEventFilter(QtWidgets.QAbstractButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tool_tip = widgets.Label()
        self.tool_tip.set_flags(frameless=True, tooltip=True)
        self.tool_tip.set_attributes(
            transparent_for_mouse_events=True,
            no_system_background=True,
            translucent_background=True,
        )
        self.tool_tip.hide()
        self.slide_anim = custom_animations.SlideAnimation(duration=1000)
        self.slide_anim.apply_to(self.tool_tip)
        self.fade_anim = custom_animations.FadeInAnimation(duration=1000)
        self.fade_anim.apply_to(self.tool_tip)
        self.animation = self.slide_anim | self.fade_anim

    def eventFilter(self, obj: QtWidgets.QAbstractButton, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.Type.Enter:
            # self.tool_tip.adjustSize()
            self.tool_tip.setText(obj.toolTip())
            self.tool_tip.show()
            position = "bottom"
            distance = 100
            center = obj.rect().center()
            if position == "top":
                center.setY(obj.rect().bottom())
                delta = core.Point(0, distance)
            elif position == "bottom":
                center.setY(obj.rect().top())
                delta = core.Point(0, -distance)
            elif position == "left":
                center.setX(obj.rect().right())
                delta = core.Point(distance, 0)
            elif position == "right":
                center.setX(obj.rect().left())
                delta = core.Point(-distance, 0)
            center = obj.mapToGlobal(center)
            self.slide_anim.set_start_value(center + delta)
            self.slide_anim.set_end_value(center)
            self.animation.start_animation()
        elif event.type() == QtCore.QEvent.Type.Leave:
            self.tool_tip.hide()
            self.animation.stop()
        elif event.type() == QtCore.QEvent.Type.ToolTip:
            return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.ToolButton()
    ef = AnimatedToolTipEventFilter()
    w.installEventFilter(ef)
    w.setText("test")
    w.set_icon("mdi.timer")
    w.set_tooltip("testus")
    w.show()
    app.main_loop()
