from __future__ import annotations

import contextlib
import functools
import weakref

from prettyqt import core, widgets
from prettyqt.qt import QtGui


class FlashEffect(widgets.GraphicsColorizeEffect):
    def __init__(self, duration: int = 1000, color="green", **kwargs):
        super().__init__(**kwargs)
        self._flash_animation = core.PropertyAnimation(self, b"color")
        self._flash_animation.setStartValue(QtGui.QColor(0, 0, 0, 0))
        self._flash_animation.setEndValue(QtGui.QColor(0, 0, 0, 0))
        self._flash_animation.setLoopCount(1)

        def remove_flash_animation(widget_ref: weakref.ref[widgets.QWidget]):
            """Remove flash animation from widget.

            Parameters
            ----------
            widget_ref : QWidget
                Any Qt widget.
            """
            if widget_ref() is None:
                return
            widget = widget_ref()
            with contextlib.suppress(RuntimeError):
                widget.setGraphicsEffect(None)

        # let's make sure to remove the animation from the widget because
        # if we don't, the widget will actually be black and white.
        self._flash_animation.finished.connect(
            functools.partial(remove_flash_animation, weakref.ref(self.parent()))
        )

    def flash(self, duration: int = 1000, color="red"):
        """Add flash animation to widget to highlight certain action.

        Parameters
        ----------
        widget : QWidget
            Any Qt widget.
        duration : int
            Duration of the flash animation.
        color : Array
            Color of the flash animation. By default, we use red.
        """
        color = QtGui.QColor(color)
        # now  set an actual time for the flashing and an intermediate color
        self._flash_animation.setDuration(duration)
        self._flash_animation.setKeyValueAt(0.1, color)
        self._flash_animation.start()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    btn = widgets.PushButton("ts")
    effect = FlashEffect(parent=btn)
    btn.show()
    app.sleep(2)
    btn.setGraphicsEffect(effect)
    effect.flash()
    app.exec()
