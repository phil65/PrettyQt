from __future__ import annotations

from collections.abc import Sequence
import logging
from typing import TYPE_CHECKING

from prettyqt import core, eventfilters


if TYPE_CHECKING:
    from collections.abc import Callable


logger = logging.getLogger(__name__)


class EventCatcher(eventfilters.BaseEventFilter):
    ID = "eventcatcher"

    caught = core.Signal(core.QEvent)

    def __init__(
        self,
        include: core.QEvent.Type
        | core.event.TypeStr
        | Sequence[core.QEvent.Type | core.event.TypeStr]
        | None = None,
        exclude: core.QEvent.Type
        | core.event.TypeStr
        | Sequence[core.QEvent.Type | core.event.TypeStr]
        | None = None,
        do_filter: bool | Callable[[core.QEvent], bool] = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        match include:
            case str():
                self.include = [core.event.TYPE[include]]
            case Sequence():
                self.include = [
                    core.event.TYPE[i] if isinstance(i, str) else i for i in include
                ]
            case core.QEvent.Type():
                self.include = [include]
            case None:
                self.include = []
            case _:
                raise ValueError(include)
        match exclude:
            case str():
                self.exclude = [core.event.TYPE[exclude]]

            case Sequence():
                self.exclude = [
                    core.event.TYPE[i] if isinstance(i, str) else i for i in exclude
                ]
            case core.QEvent.Type():
                self.exclude = [exclude]
            case None:
                self.exclude = []
            case _:
                raise ValueError(exclude)
        self.do_filter = do_filter

    def eventFilter(self, source: core.QObject, event: core.QEvent) -> bool:
        if (not self.include or event.type() in self.include) and (
            not self.exclude or event.type() not in self.exclude
        ):
            self.caught.emit(event)
            # logger.debug(f"{source!r}: {event.type()!r}")
            val = self.do_filter(event) if callable(self.do_filter) else self.do_filter
            if not isinstance(val, bool):
                logger.warning("Non-bool value returned for %r: %s ", source, val)
            return bool(val)
        return False


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    window = widgets.MainWindow()
    eventcatcher = EventCatcher()
