from __future__ import annotations

from prettyqt import core, eventfilters


class TextUpdateEventFilter(eventfilters.BaseEventFilter):
    def __init__(self, parent, interval: int = 1000, **kwargs):
        super().__init__(parent, **kwargs)
        parent.startTimer(interval)
        self._update_text()

    def eventFilter(self, obj, event: core.QEvent) -> bool:
        # if obj is not self.parent():
        #     return super().eventFilter(obj, event)
        match event.type():
            case core.Event.Type.Timer:
                self._update_text()
                return True
        return super().eventFilter(obj, event)

    def _update_text(self):
        return NotImplemented


class TimeLabelEventFilter(TextUpdateEventFilter):
    ID = "time_label"

    def __init__(self, parent, time_format: str = "hh:mm:ss", **kwargs):
        self._format = time_format
        super().__init__(parent, **kwargs)

    def _update_text(self):
        time = core.Time.get_current_time()
        self.parent().set_text(time.toString(self._format))


class DateLabelEventFilter(TextUpdateEventFilter):
    ID = "date_label"

    def __init__(self, parent, date_format: str = "dd.MM.yyyy", **kwargs):
        self._format = date_format
        super().__init__(parent, **kwargs)

    def _update_text(self):
        time = core.Date.get_current_date()
        self.parent().set_text(time.toString(self._format))


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.PushButton()
    widget.set_icon("mdi.folder")
    test = DateLabelEventFilter(widget)
    widget.installEventFilter(test)
    widget.show()
    app.exec()
