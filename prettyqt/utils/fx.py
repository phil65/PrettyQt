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
        self,
        start: datatypes.VariantType,
        end: datatypes.VariantType,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        duration: int = 1000,
        delay: int = 0,
        reverse: bool = False,
        single_shot: bool = True,
    ) -> core.PropertyAnimation:
        self._animation.set_start_value(start)
        self._animation.set_end_value(end)
        self._animation.set_easing(easing)
        self._animation.set_duration(duration)
        if reverse:
            self._animation = self._animation.append_reversed()
        self.fx.run(self._animation, delay=delay, single_shot=single_shot)
        return self._animation

    def transition_to(
        self,
        end: datatypes.VariantType,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        duration: int = 1000,
        delay: int = 0,
        relative: bool = False,
        reverse: bool = False,
        single_shot: bool = True,
    ) -> core.PropertyAnimation:
        prop_name = self._animation.get_property_name()
        obj = self._animation.targetObject()
        prop = core.MetaObject(obj.metaObject()).get_property(prop_name)
        start = prop.read(obj)
        end = datatypes.align_types(start, end)
        if relative and isinstance(start, int | float | core.QPoint | core.QPointF):
            end = end + start
        return self.animate(
            start,
            end,
            easing=easing,
            duration=duration,
            delay=delay,
            reverse=reverse,
            single_shot=single_shot,
        )

    def transition_from(
        self,
        start: datatypes.VariantType,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        duration: int = 1000,
        delay: int = 0,
        relative: bool = False,
        reverse: bool = False,
        single_shot: bool = True,
    ) -> core.PropertyAnimation:
        prop_name = self._animation.get_property_name()
        obj = self._animation.targetObject()
        prop = core.MetaObject(obj.metaObject()).get_property(prop_name)
        end = prop.read(obj)
        start = datatypes.align_types(end, start)
        if relative and isinstance(start, int | float | core.QPoint | core.QPointF):
            start = end + start
        return self.animate(
            start,
            end,
            easing=easing,
            duration=duration,
            delay=delay,
            reverse=reverse,
            single_shot=single_shot,
        )

    def animate_on_event(
        self,
        event: core.event.EventStr,
        start: datatypes.VariantType,
        end: datatypes.VariantType,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        duration: int = 1000,
        delay: int = 0,
    ) -> core.PropertyAnimation:
        self._animation.setStartValue(start)
        self._animation.setEndValue(end)
        self._animation.setDuration(duration)
        self._animation.set_easing(easing)

        def on_event(event):
            self.fx.run(self._animation, delay=delay)
            return False

        obj = self._animation.targetObject()
        obj.add_callback_for_event(on_event, include=event)
        return self._animation


class Fx:
    def __init__(self, widget: widgets.QWidget):
        self._widget = widget
        self._wrapper = None
        # self._meta = core.MetaObject(self._widget.metaObject())

    def __getitem__(self, value: str) -> AnimationWrapper:
        value = helpers.to_lower_camel(value)
        anim = core.PropertyAnimation()
        anim.apply_to(self._widget.__getattr__(value))
        # pytype = meta.get_property(value).get_pyhon_type()
        # keep a reference
        self._wrapper = AnimationWrapper(anim, self)
        return self._wrapper

    # def __getattr__(self, attr):
    #     return self.__getitem__(attr)

    # def __dir__(self):
    #     props = self._meta.get_properties(only_writable=True)
    #     prop_names = [p.get_name() for p in props]
    #     return super().__dir__() + prop_names

    def set_colorize_effect(
        self,
        color: datatypes.ColorType,
        strength: float = 0.7,
    ) -> widgets.GraphicsColorizeEffect:
        effect = widgets.GraphicsColorizeEffect(self._widget)
        effect.setColor(colors.get_color(color))
        effect.setStrength(strength)
        self._widget.setGraphicsEffect(effect)
        return effect

    def set_opacity_effect(self, opacity: float) -> widgets.GraphicsOpacityEffect:
        effect = widgets.GraphicsOpacityEffect(self._widget)
        effect.setOpacity(opacity)
        self._widget.setGraphicsEffect(effect)
        return effect

    def set_blur_effect(self, radius: int) -> widgets.GraphicsBlurEffect:
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
    ) -> core.PropertyAnimation:
        return self["windowOpacity"].transition_from(
            0.0,
            easing=easing,
            duration=duration,
            delay=delay,
        )

    def fade_out(
        self,
        duration: int = 1000,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        delay: int = 0,
    ) -> core.PropertyAnimation:
        return self["windowOpacity"].transition_to(
            0.0,
            easing=easing,
            duration=duration,
            delay=delay,
        )

    def zoom(
        self,
        duration: int = 1000,
        start: float = 1.0,
        end: float = 1.0,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        anchor: str = "center",
        delay: int = 0,
    ) -> core.ZoomAnimation:
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
    ) -> core.PropertyAnimation:
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
        end: datatypes.PointType,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        duration: int = 1000,
        delay: int = 0,
    ) -> core.PropertyAnimation:
        return self["pos"].transition_from(
            end,
            easing=easing,
            duration=duration,
            delay=delay,
            reverse=True,
        )

    def run(
        self, animation: core.QPropertyAnimation, delay: int = 0, single_shot: bool = True
    ):
        self._widget.start_callback_timer(
            animation.start, interval=delay, single_shot=single_shot
        )

    def highlight_widget(self, widget: widgets.QWidget):
        from prettyqt.custom_widgets.overlayborder import FocusWidget

        widget = FocusWidget(self, widget)
        widget.show()


if __name__ == "__main__":
    app = widgets.app()
    toolbar = widgets.ToolBar("test")
    radio = widgets.RadioButton("abc")
    action = toolbar.addWidget(radio)
    toolbar.show()
    # toolbar.fx["windowOpacity"].animate_on_event(
    #     "hover_enter", start=0.0, end=1.0, duration=1000, delay=2000
    # )
    radio.fx["pos"].transition_from((0, 100), relative=True)
    toolbar.fx["pos"].transition_from(
        (0, -100), duration=2000, relative=True, reverse=True, single_shot=False
    )
    toolbar.fx.fade_out(duration=5000)

    toolbar.show_tooltips(content="shortcut")
    app.main_loop()
    with app.debug_mode():
        app.main_loop()
