from __future__ import annotations

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtWidgets


class Animator(core.Object):
    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.direction = "horizontal"
        self.speed = 500
        self.animation_type = "out_cubic"
        self.now = 0
        self.next = 0
        self.wrap = False
        self.pnow = core.Point(0, 0)
        self.active = False

    def set_direction(self, direction: constants.OrientationStr):
        self.direction = direction

    def set_speed(self, speed: int):
        self.speed = speed

    def set_animation(self, animation_type: core.easingcurve.TypeStr):
        self.animation_type = animation_type

    def set_wrap(self, wrap: bool):
        self.wrap = wrap

    @core.Slot()
    def slide_in_previous(self):
        now = self._widget.currentIndex()
        if self.wrap or now > 0:
            self.slide_in(now - 1)

    @core.Slot()
    def slide_in_next(self):
        now = self._widget.currentIndex()
        if self.wrap or now < (self._widget.count() - 1):
            self.slide_in(now + 1)

    def slide_in(self, idx: int | QtWidgets.QWidget):
        if self.active:
            return
        if isinstance(idx, int):
            if idx > (self._widget.count() - 1):
                idx = idx % self._widget.count()
            elif idx < 0:
                idx = (idx + self._widget.count()) % self._widget.count()
            idx = self._widget.widget(idx)

        self.active = True

        _now = self._widget.currentIndex()
        _next = self._widget.indexOf(idx)

        if _now == _next:
            self.active = False
            return
        if hasattr(self._widget, "frameRect"):  # TabWidget doesnt have frameRect
            frame_rect = self._widget.frameRect()
        else:
            frame_rect = self._widget.rect()
        offsetx, offsety = (frame_rect.width(), frame_rect.height())
        self._widget.widget(_next).setGeometry(frame_rect)

        if self.direction == "horizontal":
            if _now < _next:
                offsetx, offsety = -offsetx, 0
            else:
                offsety = 0

        elif _now < _next:
            offsetx, offsety = 0, -offsety
        else:
            offsetx = 0
        pnext = self._widget.widget(_next).pos()
        pnow = self._widget.widget(_now).pos()
        self.pnow = pnow

        offset = core.Point(offsetx, offsety)
        self._widget.widget(_next).move(pnext - offset)
        self._widget.widget(_next).show()
        self._widget.widget(_next).raise_()

        anim_group = core.ParallelAnimationGroup(
            self._widget, finished=self._on_animation_done
        )

        for index, start, end in zip(
            (_now, _next), (pnow, pnext - offset), (pnow + offset, pnext)
        ):
            animation = core.PropertyAnimation(
                self._widget.widget(index),
                b"pos",
                duration=self.speed,
                easing_curve=self.animation_type,
                start_value=start,
                end_value=end,
            )
            anim_group.addAnimation(animation)

        self.next = _next
        self.now = _now
        self.active = True
        anim_group.start_animation(policy="delete")

    @core.Slot()
    def _on_animation_done(self):
        self._widget.setCurrentIndex(self.next)
        self._widget.widget(self.now).hide()
        self._widget.widget(self.now).move(self.pnow)
        self.active = False

    def fade_in(self, widget: int | QtWidgets.QWidget):
        widget = self._widget.widget(widget) if isinstance(widget, int) else widget
        self._widget.fader_widget = FaderWidget(
            self._widget.currentWidget(), widget, self.speed
        )
        self._widget.setCurrentWidget(widget)


class FaderWidget(widgets.Widget):
    pixmap_opacity = 1.0

    def __init__(
        self,
        old_widget: QtWidgets.QWidget,
        new_widget: QtWidgets.QWidget,
        duration: int = 300,
    ):
        super().__init__(new_widget)

        pr = gui.Window().devicePixelRatio()
        self.old_pixmap = gui.Pixmap(new_widget.size() * pr)
        self.old_pixmap.setDevicePixelRatio(pr)
        old_widget.render(self.old_pixmap)

        self.timeline = core.TimeLine(duration=duration, finished=self.close)
        self.timeline.value_changed.connect(self.animate)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        with gui.Painter(self) as painter:
            painter.setOpacity(self.pixmap_opacity)
            painter.drawPixmap(0, 0, self.old_pixmap)

    def animate(self, value: float):
        self.pixmap_opacity = 1.0 - value
        self.repaint()
