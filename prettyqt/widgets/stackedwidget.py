from __future__ import annotations

from collections.abc import Iterator

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtWidgets


class FaderWidget(QtWidgets.QWidget):
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


class StackedWidget(widgets.FrameMixin, QtWidgets.QStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.direction = "horizontal"
        self.speed = 300
        self.animation_type = "out_cubic"
        self.now = 0
        self.next = 0
        self.wrap = False
        self.pnow = core.Point(0, 0)
        self.active = False

    def __add__(self, other: QtWidgets.QWidget) -> StackedWidget:
        self.addWidget(other)
        return self

    def __getitem__(self, index: int) -> QtWidgets.QWidget:
        return self.widget(index)

    def __delitem__(self, item: int | QtWidgets.QWidget):
        if isinstance(item, int):
            item = self.widget(item)
        self.removeWidget(item)

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.widget(i) for i in range(self.count()))

    def __len__(self):
        # needed for PySide2
        return self.count()

    def __contains__(self, item: QtWidgets.QWidget):
        return self.indexOf(item) >= 0

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
        now = self.currentIndex()
        if self.wrap or now > 0:
            self.slide_in(now - 1)

    @core.Slot()
    def slide_in_next(self):
        now = self.currentIndex()
        if self.wrap or now < (self.count() - 1):
            self.slide_in(now + 1)

    def slide_in(self, idx: int | QtWidgets.QWidget):
        if self.active:
            return
        if isinstance(idx, int):
            if idx > (self.count() - 1):
                idx = idx % self.count()
            elif idx < 0:
                idx = (idx + self.count()) % self.count()
            idx = self.widget(idx)

        self.active = True

        _now = self.currentIndex()
        _next = self.indexOf(idx)

        if _now == _next:
            self.active = False
            return

        offsetx, offsety = self.frameRect().width(), self.frameRect().height()
        self.widget(_next).setGeometry(self.frameRect())

        if self.direction == "horizontal":
            if _now < _next:
                offsetx, offsety = -offsetx, 0
            else:
                offsety = 0

        elif _now < _next:
            offsetx, offsety = 0, -offsety
        else:
            offsetx = 0
        pnext = self.widget(_next).pos()
        pnow = self.widget(_now).pos()
        self.pnow = pnow

        offset = core.Point(offsetx, offsety)
        self.widget(_next).move(pnext - offset)
        self.widget(_next).show()
        self.widget(_next).raise_()

        anim_group = core.ParallelAnimationGroup(self, finished=self._on_animation_done)

        for index, start, end in zip(
            (_now, _next), (pnow, pnext - offset), (pnow + offset, pnext)
        ):
            animation = core.PropertyAnimation(
                self.widget(index),
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
        self.setCurrentIndex(self.next)
        self.widget(self.now).hide()
        self.widget(self.now).move(self.pnow)
        self.active = False

    def fade_in(self, widget: int | QtWidgets.QWidget):
        widget = self.widget(widget) if isinstance(widget, int) else widget
        self.fader_widget = FaderWidget(self.currentWidget(), widget, self.speed)
        self.setCurrentIndex(widget)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    stackedwidget = StackedWidget()
    widget2 = widgets.RadioButton("Test")
    widget3 = widgets.RadioButton("Test 2")
    stackedwidget += widget2
    stackedwidget += widget3
    stackedwidget.show()
    app.sleep(3)
    stackedwidget.slide_in_next()
    app.main_loop()
