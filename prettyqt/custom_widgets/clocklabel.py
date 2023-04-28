from __future__ import annotations

from prettyqt import core, widgets


class ClockLabel(widgets.Label):
    def __init__(self, *args, time_format: str = "hh:mm:ss", **kwargs):
        self._format = time_format
        super().__init__(*args, **kwargs)
        self.startTimer(1000)

    def timerEvent(self, e):
        time = core.Time.get_current_time()
        self.set_text(time.toString(self._format))


if __name__ == "__main__":
    app = widgets.app()
    widget = ClockLabel()
    widget.show()
    app.main_loop()
