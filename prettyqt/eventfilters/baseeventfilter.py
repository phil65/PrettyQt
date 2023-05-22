from __future__ import annotations

from prettyqt import core

import contextlib


class BaseEventFilter(core.Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.objectName():
            self.setObjectName(type(self).__name__)

    @contextlib.contextmanager
    def applied_to(self, obj):
        obj.installEventFilter(self)
        yield obj
        obj.removeEventFilter(self)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.Widget()
    eventfilter = BaseEventFilter()
    with eventfilter.applied_to(widget):
        pass
