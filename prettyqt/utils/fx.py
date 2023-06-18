from __future__ import annotations

import logging

from prettyqt import core, widgets
from prettyqt.utils import colors, datatypes, helpers

logger = logging.getLogger(__name__)


class AnimationTimer(core.Timer):
    """Timer with animation attached.

    Is returned for animations in order to stop them afterwards.
    """

    def __init__(
        self,
        animation: core.PropertyAnimation,
        interval: int,
        single_shot: bool = True,
        parent: core.QObject | None = None,
    ):
        # we could also take targetObject as parent?
        # that would limit the usage to PropertyAnimations though.
        self.animation = animation
        super().__init__(
            timeout=animation.start,
            interval=interval,
            single_shot=single_shot,
            parent=parent,
        )


class AnimationWrapper:
    def __init__(self, animation: core.PropertyAnimation, fx: Fx):
        self._animation = animation
        self.fx = fx

    def animate(
        self,
        start: datatypes.VariantType,
        end: datatypes.VariantType,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        duration: int = 1000,
        delay: int | str = 0,
        reverse: bool = False,
        single_shot: bool = True,
    ) -> AnimationTimer:
        """General animation with global coordinates."""
        self._animation.set_start_value(start)
        self._animation.set_end_value(end)
        self._animation.set_easing(easing)
        self._animation.set_duration(duration)
        logger.debug(f"Setting up animation: {start=}, {end=}, {easing=}, {duration=}")
        if reverse:
            self._animation.append_reversed()
        return self.fx.run(self._animation, delay=delay, single_shot=single_shot)

    def transition_to(
        self,
        end: datatypes.VariantType | tuple,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        duration: int = 1000,
        delay: int | str = 0,
        relative: bool = False,
        reverse: bool = False,
        single_shot: bool = True,
    ) -> AnimationTimer:
        """Makes property transition from current value to given end value."""
        prop_name = self._animation.get_property_name()
        obj = self._animation.targetObject()
        prop = core.MetaObject(obj.metaObject()).get_property(prop_name)
        start: core.VariantType = prop.read(obj)
        end = datatypes.align_types(start, end)
        if isinstance(end, core.QPoint | core.QRect | core.QPointF | core.QRectF):
            end = obj.map_to("parent", end)
        if relative and hasattr(end, "__add__"):
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
        delay: int | str = 0,
        relative: bool = False,
        reverse: bool = False,
        single_shot: bool = True,
    ) -> AnimationTimer:
        """Makes property transition from given start value to its current value."""
        prop_name = self._animation.get_property_name()
        obj = self._animation.targetObject()
        prop = core.MetaObject(obj.metaObject()).get_property(prop_name)
        end = prop.read(obj)
        start = datatypes.align_types(end, start)
        if isinstance(start, core.QPoint | core.QRect | core.QPointF | core.QRectF):
            start = obj.map_to("parent", start)
        if relative and hasattr(start, "__add__"):
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
        event: core.event.TypeStr,
        start: datatypes.VariantType,
        end: datatypes.VariantType,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        duration: int = 1000,
        delay: int = 0,
    ) -> core.PropertyAnimation:
        """Starts property transition from start to end when given event occurs."""
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
        logger.debug(f"Building {value!r} PropertyAnimation for {self._widget!r}")
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
    ) -> AnimationTimer:
        """Trigger a fade-in animation."""
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
    ) -> AnimationTimer:
        """Trigger a fade-out animation."""
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
    ) -> AnimationTimer:
        """Trigger a zoom animation with given anchor."""
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
        start=None,
        end=None,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        delay: int = 0,
        reverse: bool = False,
        single_shot: bool = True,
    ) -> AnimationTimer:
        anim = core.PropertyAnimation(parent=self._widget)
        anim.set_easing(easing)
        pos = self._widget.geometry().topLeft()
        start_offset = core.Point(0, 0) if start is None else datatypes.to_point(start)
        end_offset = core.Point(0, 0) if end is None else datatypes.to_point(end)
        anim.set_start_value(pos + start_offset)
        anim.set_end_value(pos + end_offset)
        anim.setDuration(duration)
        anim.apply_to(self._widget.pos)
        if reverse:
            anim.append_reversed()
        return self.run(anim, delay, single_shot=single_shot)

    def bounce(
        self,
        end: datatypes.PointType,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        duration: int = 1000,
        delay: int = 0,
    ) -> AnimationTimer:
        return self["pos"].transition_to(
            end,
            easing=easing,
            duration=duration,
            delay=delay,
            reverse=True,
        )

    def run(
        self,
        animation: core.QPropertyAnimation,
        delay: int | str = 0,
        single_shot: bool = True,
    ) -> AnimationTimer:
        if not animation.targetObject().isVisible():
            logger.info("Attention. Starting animation for invisible widget.")
        logger.debug(f"starting {animation!r} with {delay=}. ({single_shot=})")
        timer = AnimationTimer(
            parent=self._widget,
            single_shot=single_shot,
            interval=helpers.parse_time(delay) if isinstance(delay, str) else delay,
            animation=animation,
        )
        timer.start()
        return timer

    def highlight_widget(self, widget: widgets.QWidget):
        from prettyqt.custom_widgets.overlayborder import FocusWidget

        widget = FocusWidget(self, widget)
        widget.show()


if __name__ == "__main__":
    app = widgets.app()
    with app.debug_mode():
        w1 = widgets.RadioButton("test")
        w2 = widgets.RadioButton("test")
        w3 = widgets.Splitter("horizontal")
        w4 = widgets.RadioButton("test")
        widget = widgets.Widget()
        container = widget.set_layout("horizontal")
        container.add(w1)
        container.add(w2)
        w3.add(w4)
        container.add(w3)
        widget.show()
        # container[:].fx["size"].transition_from(
        #     (100, 100), duration=3000, reverse=True, single_shot=False
        # )
        # timer = container[::2].fx.slide(
        #     start=(-100, 0), duration=3000, reverse=True, single_shot=False
        # )
        w4.fx.bounce((0, -100), duration=5000)
        # print(timer)
        # app.sleep(1)  #
        # timer[0].animation.toggle_direction()
        app.main_loop()
