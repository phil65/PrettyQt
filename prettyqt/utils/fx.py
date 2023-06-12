from __future__ import annotations

import logging

from prettyqt import core, widgets
from prettyqt.utils import colors, datatypes, helpers

logger = logging.getLogger(__name__)


class AnimationWrapper:
    def __init__(self, animation, fx):
        self._animation = animation
        self.fx = fx

    def animate(
        self, start, end, easing="in_out_sine", duration: int = 1000, delay: int = 0
    ):
        self._animation.set_start_value(start)
        self._animation.set_end_value(end)
        self._animation.set_easing(easing)
        self._animation.set_duration(duration)
        self.fx.run(self._animation, delay)
        return self._animation

    def transition_to(
        self,
        end,
        easing="in_out_sine",
        duration: int = 1000,
        delay: int = 0,
        relative: bool = False,
    ):
        prop_name = self._animation.get_property_name()
        obj = self._animation.targetObject()
        prop = core.MetaObject(obj.metaObject()).get_property(prop_name)
        start = prop.read(obj)
        if relative:
            end = end + start
        return self.animate(start, end, easing)

    def transition_from(
        self,
        start,
        easing="in_out_sine",
        duration: int = 1000,
        delay: int = 0,
        relative: bool = False,
    ):
        prop_name = self._animation.get_property_name()
        obj = self._animation.targetObject()
        prop = core.MetaObject(obj.metaObject()).get_property(prop_name)
        end = prop.read(obj)
        if relative:
            start = end + start
        return self.animate(start, end, easing)

    def animate_on_event(
        self,
        event: core.event.EventStr,
        start,
        end,
        easing="in_out_sine",
        duration: int = 1000,
        delay: int = 0,
    ):
        self._animation.setStartValue(start)
        self._animation.setEndValue(end)
        self._animation.setDuration(duration)
        self._animation.set_easing(easing)

        def on_event(event):
            self._animation.start()
            return False

        obj = self._animation.targetObject()
        obj.add_callback_for_event(on_event, include=event)
        return self._animation


class Fx:
    def __init__(self, widget):
        self._widget = widget
        self._wrapper = None

    def __getitem__(self, value: str):
        value = helpers.to_lower_camel(value)
        anim = core.PropertyAnimation()
        anim.apply_to(self._widget.__getattr__(value))
        # meta = core.MetaObject(self._widget.metaObject())
        # pytype = meta.get_property(value).get_pyhon_type()
        # keep a reference
        self._wrapper = AnimationWrapper(anim, self)
        return self._wrapper

    def set_colorize_effect(
        self,
        strength: float = 0.5,
        color: datatypes.ColorType = "blue",
    ) -> widgets.GraphicsColorizeEffect:
        effect = widgets.GraphicsColorizeEffect(self._widget)
        effect.setColor(colors.get_color(color))
        effect.setStrength(strength)
        self._widget.setGraphicsEffect(effect)
        return effect

    def set_opacity_effect(self, opacity: float = 0.7) -> widgets.GraphicsOpacityEffect:
        effect = widgets.GraphicsOpacityEffect(self._widget)
        effect.setOpacity(opacity)
        self._widget.setGraphicsEffect(effect)
        return effect

    def set_blur_effect(self, radius: int = 10) -> widgets.GraphicsBlurEffect:
        effect = widgets.GraphicsBlurEffect(self._widget)
        effect.setBlurRadius(radius)
        self._widget.setGraphicsEffect(effect)
        return effect

    def set_drop_shadow_effect(
        self,
        radius: int = 10,
        color: datatypes.ColorType = "blue",
    ) -> widgets.GraphicsDropShadowEffect:
        effect = widgets.GraphicsDropShadowEffect(self._widget)
        effect.setBlurRadius(radius)
        effect.setColor(colors.get_color(color))
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

    def zoom(
        self,
        duration: int = 1000,
        start: float = 1.0,
        end: float = 1.0,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        anchor: str = "center",
        delay: int = 0,
    ):
        from prettyqt import custom_animations

        anim = custom_animations.ZoomAnimation(parent=self._widget, anchor=anchor)
        anim.set_easing(easing)
        anim.set_start_value(start)
        anim.set_end_value(end)
        anim.set_duration(duration)
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
    toolbar = widgets.ToolBar("test")
    radio = widgets.RadioButton("abc")
    action = toolbar.addWidget(radio)
    toolbar.show()
    radio.fx["pos"].transition_from(core.Point(0, 100), relative=True)
    toolbar.show_tooltips(content="shortcut")
    app.main_loop()
    with app.debug_mode():
        app.main_loop()
