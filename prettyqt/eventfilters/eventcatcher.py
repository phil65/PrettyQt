from __future__ import annotations

from collections.abc import Callable, Container
import logging

from prettyqt import core
from prettyqt.qt import QtCore


logger = logging.getLogger(__name__)


class EventCatcher(core.Object):
    caught = core.Signal(QtCore.QEvent)

    def __init__(
        self,
        include: QtCore.QEvent.Type
        | core.Event.TypeStr
        | Container[QtCore.QEvent.Type | core.Event.TypeStr]
        | None = None,
        exclude: QtCore.QEvent.Type | Container[QtCore.QEvent.Type] | None = None,
        do_filter: bool | Callable[[QtCore.QEvent], bool] = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        match include:
            case list():
                self.include = [
                    core.event.TYPE[i] if isinstance(i, str) else i for i in include
                ]
            case str():
                self.include = [core.event.TYPE[include]]
            case QtCore.QEvent.Type:
                self.include = [include]
            case None:
                self.include = None
        match exclude:
            case list():
                self.exclude = [
                    core.event.TYPE[i] if isinstance(i, str) else i for i in exclude
                ]
            case str():
                self.exclude = [core.event.TYPE[exclude]]
            case QtCore.QEvent.Type:
                self.exclude = [exclude]
            case None:
                self.exclude = None
        self.do_filter = do_filter

    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if not self.include or event.type() in self.include:
            if not self.exclude or event.type() not in self.exclude:
                self.caught.emit(event)
                logger.debug(f"{source!r}: {event.type()!r}")
                if callable(self.do_filter):
                    return self.do_filter(event)
                return self.do_filter
        return False


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    window = widgets.MainWindow()
    eventcatcher = EventCatcher()
