from __future__ import annotations

import collections
import contextlib

# import enum
import logging
from typing import Any, TypeVar

from prettyqt import constants, core, eventfilters, gui


logger = logging.getLogger(__name__)

T = TypeVar("T", bound=core.QObject)


class EventSignaller(core.Object):
    signal = core.Signal(core.QEvent)

    def __init__(self, obj: core.QObject, **kwargs):
        super().__init__(**kwargs)
        self._obj = obj

    def __getattr__(self, name):
        typ = getattr(core.QEvent.Type, name)
        self.ec = self._obj.add_callback_for_event(self._on_event_detected, include=typ)
        return self.signal

    def _on_event_detected(self, event: core.QEvent):
        self.signal.emit(event)
        return False


class Stalker(core.Object):
    # @core.Enum
    # class LogLevel(enum.IntEnum):
    #     """Log level."""

    #     DEBUG = logging.DEBUG
    #     INFO = logging.INFO
    #     WARNING = logging.WARNING
    #     CRITICAL = logging.CRITICAL
    #     ERROR = logging.ERROR

    keypress_detected = core.Signal(str)
    leftclick_detected = core.Signal(core.QPointF)
    rightclick_detected = core.Signal(core.QPointF)
    event_detected = core.Signal(core.QEvent)
    signal_emitted = core.Signal(core.MetaMethod, object)  # signal, args
    signal_connected = core.Signal(core.MetaMethod)
    signal_disconnected = core.Signal(core.MetaMethod)

    def __init__(
        self,
        qobject: core.QObject,
        include=None,
        exclude=None,
        **kwargs: Any,
    ):
        self._log_level = logging.INFO
        super().__init__(**kwargs)
        self._obj = qobject
        qmeta = self._obj.metaObject()
        assert qmeta
        self._meta = core.MetaObject(qmeta)
        self.counter: collections.defaultdict[str, int] = collections.defaultdict(int)
        self.signal_counter: collections.defaultdict[str, int] = collections.defaultdict(
            int
        )
        self.exclude = ["meta_call", "timer"] if exclude is None else exclude
        self.include = include
        self._handles: list[core.QMetaObject.Connection] = []

    def __enter__(self):
        self.hook()
        return self

    def __exit__(self, typ, value, traceback):
        self.unhook()

    @property
    def eventsignals(self):
        return EventSignaller(self._obj)

    def hook(self):
        # enable event logging by installing EventCatcher, which includes logging
        self.eventcatcher = eventfilters.EventCatcher(
            self.include, self.exclude, self._on_event_detected, parent=self._obj
        )
        self._obj.installEventFilter(self.eventcatcher)
        # enable logging of signals emitted by connecting all signals to our fn
        for signal in self._meta.get_signals(only_notifiers=False):
            signal_name = signal.get_name()
            # PyQt reports non-existing signals in MetaObject.
            if hasattr(self._obj, signal_name):
                signal_instance = getattr(self._obj, signal_name)
            fn = self._on_signal_emitted(signal)
            handle = signal_instance.connect(fn)
            self._handles.append(handle)
        self.log(f"Stalking {len(self._handles)} signals")
        # enable logging of all signal (dis)connections by hooking to connectNotify
        self.old_connectNotify = self._obj.connectNotify
        self.old_disconnectNotify = self._obj.disconnectNotify
        self._obj.connectNotify = self._on_signal_connected
        self._obj.disconnectNotify = self._on_signal_disconnected
        # self._obj.destroyed.connect(self.unhook)
        # self.destroyed.connect(self.unhook)

    def unhook(self):
        if self.eventcatcher is None:
            logger.warning("unhook() called before hook()")
            return
        """Clean up our mess."""
        self._obj.connectNotify = self.old_connectNotify
        self._obj.disconnectNotify = self.old_disconnectNotify
        self.old_connectNotify = None
        self.old_disconnectNotify = None
        for handle in self._handles:
            self._obj.disconnect(handle)
        self._handles = []
        with contextlib.suppress(RuntimeError):
            self._obj.removeEventFilter(self.eventcatcher)

    def log(self, message: str):
        if self.log_level:
            with contextlib.suppress(RuntimeError):
                logger.log(self._log_level, f"{self._obj!r}: {message}")  # noqa: G004

    def _on_signal_connected(self, qsignal: core.QMetaMethod):
        signal = core.MetaMethod(qsignal)
        self.log(f"Connected signal {signal.get_name()}")
        self.signal_connected.emit(signal)

    def _on_signal_disconnected(self, qsignal: core.QMetaMethod):
        signal = core.MetaMethod(qsignal)
        self.log(f"Disconnected signal {signal.get_name()}")
        self.signal_disconnected.emit(signal)

    def _on_event_detected(self, event) -> bool:
        """Used for EventCatcher, returns false to not eat signals."""
        try:
            self.event_detected.emit(event)
        except RuntimeError:
            return None
        match event.type():
            case core.Event.Type.KeyPress:
                combo = gui.KeySequence(event.keyCombination()).toString()
                self.keypress_detected.emit(combo)
            case core.Event.Type.MouseButtonRelease:
                if event.button() == constants.MouseButton.LeftButton:
                    self.leftclick_detected.emit(event.position())
                if event.button() == constants.MouseButton.RightButton:
                    self.rightclick_detected.emit(event.position())
        self.log(f"Received event {event.type()!r}")
        self.counter[event.type()] += 1
        return False

    def _on_signal_emitted(self, signal: core.MetaMethod):
        def fn(*args, **kwargs):
            try:
                self.signal_emitted.emit(signal, args)
                self.signal_counter[signal.get_name()] += 1
                self.log(f"Emitted signal {signal.get_name()}{args}")
            except RuntimeError:
                pass

        return fn

    def set_log_level(self, level: int):
        self._log_level = level

    def get_log_level(self) -> int:
        return self._log_level

    def count_children(self, type_filter: type[T] = core.QObject) -> collections.Counter:
        objects = self.findChildren(type_filter)
        return collections.Counter([type(o) for o in objects])

    def show(self):
        from prettyqt import custom_widgets

        widget = custom_widgets.LogRecordTableView()
        widget.set_logger(logger, level=self.log_level)
        widget.show()

    log_level = core.Property(
        int,
        get_log_level,
        set_log_level,
        doc="Level to use for logging",
    )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.LineEdit()
    widget.show()
    with app.debug_mode(), Stalker(widget, log_level=logging.INFO) as stalker:
        stalker.eventsignals.MouseButtonPress.connect(print)
        stalker.show()
        app.exec()
