import contextlib

from prettyqt import core


class BaseEventFilter(core.Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.objectName():
            self.setObjectName(type(self).__name__)

    @contextlib.contextmanager
    def applied_to(self, obj):
        obj.installEventFilter(self)
        try:
            yield obj
        finally:
            obj.removeEventFilter(self)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.Widget()
    eventfilter = BaseEventFilter()
    with eventfilter.applied_to(widget):
        pass
