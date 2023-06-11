from __future__ import annotations

import logging
from typing import Literal

from prettyqt import core, widgets
from prettyqt.utils import colors, datatypes

logger = logging.getLogger(__name__)


class Fx:
    def __init__(self, widget):
        self._widget = widget

    def set_graphics_effect(
        self,
        effect: widgets.QGraphicsEffect
        | Literal["drop_shadow", "blur", "opacity", "colorize"],
        radius: int = 10,
        opacity: float = 0.7,
        strength: float = 0.5,
        color: datatypes.ColorType = "blue",
    ) -> widgets.QGraphicsEffect:
        match effect:
            case "drop_shadow":
                effect = widgets.GraphicsDropShadowEffect(self._widget)
                effect.setBlurRadius(radius)
                effect.setColor(colors.get_color(color))
            case "blur":
                effect = widgets.GraphicsBlurEffect(self._widget)
                effect.setBlurRadius(radius)
            case "opacity":
                effect = widgets.GraphicsOpacityEffect(self._widget)
                effect.setOpacity(opacity)
            case "colorize":
                effect = widgets.GraphicsColorizeEffect(self._widget)
                effect.setColor(colors.get_color(color))
                effect.setStrength(strength)
        self._widget.setGraphicsEffect(effect)
        return effect

    def fade_in(
        self,
        duration: int = 1000,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        delay: int = 0,
    ):
        anim = core.PropertyAnimation(parent=self._widget)
        anim.set_easing(easing)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setDuration(duration)
        anim.apply_to(self._widget.windowOpacity)
        self.run(anim, delay)
        return anim

    def fade_out(
        self,
        duration: int = 1000,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        delay: int = 0,
    ):
        anim = core.PropertyAnimation(parent=self._widget)
        anim.set_easing(easing)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setDuration(duration)
        anim.apply_to(self._widget.windowOpacity)
        self.run(anim, delay)
        return anim

    def slide(
        self,
        duration: int = 1000,
        start_value=None,
        end_value=None,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        delay: int = 0,
    ):
        anim = core.PropertyAnimation(parent=self._widget)
        anim.set_easing(easing)
        pos = self._widget.geometry().topLeft()
        start_offset = datatypes.to_point(start_value)
        end_offset = datatypes.to_point(end_value)
        anim.set_start_value(pos + start_offset)
        anim.set_end_value(pos + end_offset)
        anim.setDuration(duration)
        anim.apply_to(self._widget.pos)
        self.run(anim, delay)
        return anim

    def bounce(
        self,
        duration: int = 1000,
        start=None,
        end=None,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        delay: int = 0,
    ):
        from prettyqt import custom_animations

        anim = custom_animations.BounceAnimation(parent=self._widget)
        anim.set_easing(easing)
        anim.set_start_value(start)
        anim.set_end_value(start)
        anim.setDuration(duration)
        anim.apply_to(self._widget.windowOpacity)
        self.run(anim, delay)
        return anim

    def play_property_animation(
        self,
        property_name: str,
        start_value,
        end_value,
        easing="in_out_sine",
        duration: int = 1000,
        delay: int = 0,
    ) -> core.QPropertyAnimation:
        anim = core.PropertyAnimation(parent=self._widget)
        anim.setTargetObject(self._widget)
        anim.set_property_name(property_name)
        anim.setStartValue(start_value)
        anim.setEndValue(end_value)
        anim.setDuration(duration)
        anim.set_easing(easing)
        self.run(anim, delay)
        return anim

    def animate_on_event(
        self,
        event: core.event.EventStr,
        property_name: str,
        start_value,
        end_value,
        easing="in_out_sine",
        duration: int = 1000,
        delay: int = 0,
    ):
        anim = core.PropertyAnimation(parent=self._widget)
        anim.setTargetObject(self._widget)
        anim.set_property_name(property_name)
        anim.setStartValue(start_value)
        anim.setEndValue(end_value)
        anim.setDuration(duration)
        anim.set_easing(easing)

        def on_event(event):
            anim.start()
            return False

        self._widget.add_callback_for_event(on_event, include=event)

    def run(
        self, animation: core.QPropertyAnimation, delay: int = 0, single_shot: bool = True
    ):
        self._widget.start_callback_timer(animation.start, delay, single_shot=single_shot)

    def highlight_widget(self, widget):
        from prettyqt.custom_widgets.overlayborder import FocusWidget

        widget = FocusWidget(self, widget)
        widget.show()


if __name__ == "__main__":
    app = widgets.app()

    test = widgets.PlainTextEdit()
    test.show()
    with app.debug_mode():
        app.main_loop()
