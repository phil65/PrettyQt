from __future__ import annotations

import enum
import logging

import collections
from typing import TypeVar

from prettyqt import core
from prettyqt.qt import QtCore


logger = logging.getLogger(__name__)

T = TypeVar("T", bound=QtCore.QObject)


class Stalker(core.Object):
    @core.Enum
    class LogLevel(enum.IntEnum):
        """Log level."""

        DEBUG = logging.DEBUG
        INFO = logging.INFO
        WARNING = logging.WARNING
        CRITICAL = logging.CRITICAL
        ERROR = logging.ERROR

    event_detected = core.Signal(QtCore.QEvent)
    signal_emitted = core.Signal(core.MetaMethod, object)  # signal, args
    signal_connected = core.Signal(core.MetaMethod)
    signal_disconnected = core.Signal(core.MetaMethod)

    def __init__(
        self,
        qobject: QtCore.QObject,
        include=None,
        exclude=None,
        **kwargs,
    ):
        self._log_level = logging.INFO
        super().__init__(**kwargs)
        self._obj = qobject
        self._meta = core.MetaObject(self._obj.metaObject())
        self.counter = collections.defaultdict(int)
        self.signal_counter = collections.defaultdict(int)
        self.exclude = ["meta_call", "timer"] if exclude is None else exclude
        self.include = include
        self._handles = []

    def __enter__(self):
        self.hook()
        return self

    def __exit__(self, typ, value, traceback):
        self.unhook()

    def hook(self):
        # enable event logging by installing EventCatcher, which includes logging
        self.eventcatcher = self._obj.add_callback_for_event(
            self._on_event_detected, include=self.include, exclude=self.exclude
        )
        # enable logging of signals emitted by connecting all signals to our fn
        for signal in self._meta.get_signals(only_notifiers=True):
            signal_instance = self._obj.__getattribute__(signal.get_name())
            fn = self._on_signal_emitted(signal)
            handle = signal_instance.connect(fn)
            self._handles.append(handle)
        # enable logging of all signal (dis)connections by hooking to connectNotify
        self.old_connectNotify = self._obj.connectNotify
        self.old_disconnectNotify = self._obj.disconnectNotify
        self._obj.connectNotify = self._on_signal_connected
        self._obj.disconnectNotify = self._on_signal_disconnected

    def unhook(self):
        if self.eventcatcher is None:
            raise RuntimeError("need to hook Stalker before unhooking")
        """Clean up our mess."""
        self._obj.connectNotify = self.old_connectNotify
        self._obj.disconnectNotify = self.old_disconnectNotify
        self.old_connectNotify = None
        self.old_disconnectNotify = None
        for handle in self._handles:
            self._obj.disconnect(handle)
        self._handles = None
        self._obj.removeEventFilter(self.eventcatcher)

    def log(self, message: str):
        if self._log_level:
            try:
                logger.log(self._log_level, f"{self._obj!r}: {message}")
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

    def set_log_level(self, level: int | LogLevel):
        if isinstance(level, int):
            level = self.LogLevel(level)
        self._log_level = level

    def get_log_level(self) -> LogLevel:
        return self._log_level

    def count_children(
        self, type_filter: type[T] = QtCore.QObject
    ) -> collections.Counter:
        objects = self.findChildren(type_filter)
        return collections.Counter([type(o) for o in objects])

    logLevel = core.Property(LogLevel, get_log_level, set_log_level)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.LineEdit()
    widget.show()
    with app.debug_mode():
        with Stalker(widget, log_level=logging.INFO) as stalker:
            app.sleep(3)
            print(stalker.counter)
        app.main_loop()
