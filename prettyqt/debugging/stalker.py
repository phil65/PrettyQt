from __future__ import annotations

import logging

import collections
from typing import TypeVar

from prettyqt import core
from prettyqt.qt import QtCore


logger = logging.getLogger(__name__)

T = TypeVar("T", bound=QtCore.QObject)


class Stalker(core.Object):
    event_detected = core.Signal(QtCore.QEvent)
    signal_emitted = core.Signal(core.MetaMethod, object)  # signal, args
    signal_connected = core.Signal(core.MetaMethod)
    signal_disconnected = core.Signal(core.MetaMethod)

    def __init__(
        self,
        qobject: QtCore.QObject,
        include=None,
        exclude=None,
        log_level=logging.INFO,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.obj = qobject
        self.log_level = log_level
        self.counter = collections.defaultdict(int)
        self.signal_counter = collections.defaultdict(int)
        if exclude is None:
            exclude = ["meta_call", "timer"]
        # enable event logging by installing EventCatcher, which includes logging
        self.eventcatcher = self.obj.add_callback_for_event(
            self._on_event_detected, include=include, exclude=exclude
        )
        self.handles = []
        # enable logging of signals emitted by connecting all signals to our fn
        for signal in self.obj.get_metaobject().get_signals():
            signal_instance = self.obj.__getattribute__(signal.get_name())
            fn = self._on_signal_emitted(signal)
            handle = signal_instance.connect(fn)
            self.handles.append(handle)
        # enable logging of all signal (dis)connections by hooking to connectNotify
        self.old_connectNotify = self.obj.connectNotify
        self.old_disconnectNotify = self.obj.disconnectNotify
        self.obj.connectNotify = self._on_signal_connected
        self.obj.disconnectNotify = self._on_signal_disconnected

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        self.unhook()

    def unhook(self):
        """Clean up our mess."""
        self.obj.connectNotify = self.old_connectNotify
        self.obj.disconnectNotify = self.old_disconnectNotify
        for handle in self.handles:
            self.obj.disconnect(handle)
        self.obj.removeEventFilter(self.eventcatcher)

    def log(self, message: str):
        if self.log_level:
            try:
                logger.log(self.log_level, f"{self.obj!r}: {message}")
            except RuntimeError:
                logger.error("Object probably already deleted.")

    def _on_signal_connected(self, signal: QtCore.QMetaMethod):
        signal = core.MetaMethod(signal)
        self.log(f"Connected signal {signal.get_name()}")
        self.signal_connected.emit(signal)

    def _on_signal_disconnected(self, signal: QtCore.QMetaMethod):
        signal = core.MetaMethod(signal)
        self.log(f"Disconnected signal {signal.get_name()}")
        self.signal_disconnected.emit(signal)

    def _on_event_detected(self, event) -> bool:
        """Used for EventCatcher, returns false to not eat signals."""
        self.event_detected.emit(event)
        self.log(f"Received event {event.type()!r}")
        self.counter[event.type()] += 1
        return False

    def _on_signal_emitted(self, signal: core.MetaMethod):
        def fn(*args, **kwargs):
            self.signal_emitted.emit(signal, args)
            self.signal_counter[signal.get_name()] += 1
            self.log(f"Emitted signal {signal.get_name()}{args}")

        return fn

    def count_children(
        self, type_filter: type[T] = QtCore.QObject
    ) -> collections.Counter:
        objects = self.findChildren(type_filter)
        return collections.Counter([type(o) for o in objects])


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.LineEdit()
    widget.show()
    with app.debug_mode():
        with Stalker(widget) as stalker:
            app.sleep(3)
            print(stalker.counter)
        app.main_loop()
