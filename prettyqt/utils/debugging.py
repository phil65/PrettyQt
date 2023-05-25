"""Module containing helper functions."""

from __future__ import annotations

import collections
import contextlib
from collections.abc import Callable, Generator

import logging
import re
import sys
from typing import TypeVar

from prettyqt import core, gui, qt, widgets
from prettyqt.qt import QtCore
from prettyqt.utils import helpers


T = TypeVar("T", bound=QtCore.QObject)


logger = logging.getLogger(__name__)

LOG_MAP = {
    QtCore.QtMsgType.QtDebugMsg: logging.DEBUG,
    QtCore.QtMsgType.QtInfoMsg: logging.INFO,
    QtCore.QtMsgType.QtWarningMsg: logging.WARNING,
    QtCore.QtMsgType.QtCriticalMsg: logging.ERROR,
    QtCore.QtMsgType.QtFatalMsg: logging.CRITICAL,
    QtCore.QtMsgType.QtSystemMsg: logging.CRITICAL,
}

# qFormatLogMessage(QtMsgType type, const QMessageLogContext context, const QString str)
# qInstallMessageHandler(QtMessageHandler handler)
# qSetMessagePattern(const QString &pattern)


class QtLogger(logging.Handler):
    def emit(self, record: logging.LogRecord):
        match record.level:
            case logging.DEBUG:
                QtCore.qDebug(self.format(record))
            case logging.INFO:
                QtCore.qInfo(self.format(record))
            case logging.WARNING:
                QtCore.qWarning(self.format(record))
            case logging.CRITICAL:
                QtCore.qCritical(self.format(record))
            case logging.CRITICAL:
                QtCore.qFatal(self.format(record))


class MessageHandler:
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self._previous_handler = None

    def install(self):
        self._previous_handler = QtCore.qInstallMessageHandler(self)

    def uninstall(self):
        if self._previous_handler is None:
            QtCore.qInstallMessageHandler(self._previous_handler)

    def __enter__(self):
        self.install()
        return self

    def __exit__(self, *args):
        self.uninstall()

    def __call__(
        self,
        msgtype: QtCore.QtMsgType,
        context: QtCore.QMessageLogContext,
        message: str,
    ):
        ctx = dict.fromkeys(["category", "file", "function", "line"])
        with contextlib.suppress(UnicodeDecodeError):
            ctx["category"] = context.category
        with contextlib.suppress(UnicodeDecodeError):
            ctx["file"] = context.file
        with contextlib.suppress(UnicodeDecodeError):
            ctx["function"] = context.function
        with contextlib.suppress(UnicodeDecodeError):
            ctx["line"] = context.line

        level = LOG_MAP[msgtype]
        self._logger.log(level, message, extra=ctx)


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


def is_deleted(obj) -> bool:
    match qt.API:
        case "pyside6":
            import shiboken6

            return not shiboken6.isValid(obj)
        case "pyqt6":
            from PyQt6 import sip

            return sip.isdeleted(obj)


class TracebackDialog(widgets.Dialog):
    """A dialog box that shows Python traceback."""

    def __init__(self, parent):
        super().__init__(parent, window_title="Traceback")
        layout = widgets.VBoxLayout()
        self.setLayout(layout)
        self._text = widgets.TextEdit(self, read_only=True, line_wrap_mode="none")
        self._text.setFontFamily(gui.Font.mono().family())
        layout.addWidget(self._text)
        self.resize(600, 400)

    def setText(self, text: str):
        """Always set text as a HTML text."""
        self._text.setHtml(text)


class ErrorMessageBox(widgets.MessageBox):
    """An message box widget for displaying Python exception."""

    def __init__(self, title: str, text_or_exception: str | Exception, parent):
        if isinstance(text_or_exception, str):
            text = text_or_exception
            exc = None
        else:
            text = str(text_or_exception)
            exc = text_or_exception
        super().__init__(
            # icon=MBox.Icon.Critical,
            title=title,
            text=str(text)[:1000],
            buttons=["ok", "help", "close"],
            parent=parent,
        )

        self._exc = exc

        traceback_button = self.button(widgets.MessageBox.StandardButton.Help)
        traceback_button.setText("Show trackback")
        close_button = self.button(widgets.MessageBox.StandardButton.Close)
        close_button.setText("Quit application")

    def exec(self):
        match super().exec():
            case widgets.MessageBox.StandardButton.Help:
                tb = self._get_traceback()
                dlg = TracebackDialog(self)
                dlg.setText(tb)
                dlg.exec()
            case widgets.MessageBox.StandardButton.Close:
                sys.exit(1)
            case widgets.MessageBox.StandardButton.Ok:
                return True

    @classmethod
    def from_exc(cls, e: Exception, parent=None):
        """Construct message box from a exception."""
        return cls(type(e).__name__, e, parent)

    @classmethod
    def raise_(cls, e: Exception, parent=None):
        """Raise exception in the message box."""
        # unwrap EmitLoopError
        return cls.from_exc(e, parent=parent).exec()

    def _get_traceback(self):
        if self._exc is None:
            import traceback

            tb = traceback.format_exc()
            print(tb)
        else:
            tb = get_tb_formatter(gui.Font.mono().family())(self._exc, as_html=True)
        return tb

    @classmethod
    def _excepthook(cls, exc_type: type[Exception], exc_value: Exception, exc_traceback):
        """Exception hook used during application execution."""
        logger.exception(exc_value)
        return ErrorMessageBox.raise_(exc_value, parent=None)


# Following functions are mostly copied from napari (BSD 3-Clause).
# See https://github.com/napari/napari/blob/main/napari/utils/notifications.py


def get_tb_formatter(font: str = "Monospace") -> Callable[[Exception, bool, str], str]:
    """Return a formatter callable that uses IPython VerboseTB if available.

    Imports IPython lazily if available to take advantage of ultratb.VerboseTB.
    If unavailable, cgitb is used instead, but this function overrides a lot of
    the hardcoded citgb styles and adds error chaining (for exceptions that
    result from other exceptions).

    Returns:
        callable: A function that accepts a 3-tuple and a boolean ``(exc_info, as_html)``
                and returns a formatted traceback string. The ``exc_info`` tuple is of
                the ``(type, value, traceback)`` format returned by sys.exc_info().
                The ``as_html`` determines whether the traceback is formatted in html
                or plain text.
    """
    try:
        import IPython.core.ultratb

        def format_exc_info(exc: Exception, as_html: bool, color="Neutral") -> str:
            # avoids printing the array data
            # some discussion related to obtaining the current string function
            # can be found here, https://github.com/numpy/numpy/issues/11266
            info = (
                exc.__class__,
                exc,
                exc.__traceback__,
            )
            import numpy as np

            np.set_string_function(lambda arr: f"{type(arr)} {arr.shape} {arr.dtype}")

            vbtb = IPython.core.ultratb.VerboseTB(color_scheme=color)
            if as_html:
                ansi_string = (
                    vbtb.text(*info)
                    .replace(" ", "&nbsp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )
                html = helpers.ansi2html(ansi_string)
                html = html.replace("\n", "<br>")
                html = (
                    f"<span style='font-family: monaco,{font},"
                    "monospace;'>" + html + "</span>"
                )
                tb_text = html
            else:
                tb_text = vbtb.text(*info)

            # resets to default behavior
            np.set_string_function(None)
            return tb_text

    except ModuleNotFoundError:
        import cgitb
        import traceback

        # cgitb does not support error chaining...
        # see https://peps.python.org/pep-3134/#enhanced-reporting
        # this is a workaround
        def cgitb_chain(exc: Exception) -> Generator[str, None, None]:
            """Recurse through exception stack and chain cgitb_html calls."""
            if exc.__cause__:
                yield from cgitb_chain(exc.__cause__)
                yield (
                    '<br><br><font color="#51B432">The above exception was '
                    "the direct cause of the following exception:</font><br>"
                )
            elif exc.__context__:
                yield from cgitb_chain(exc.__context__)
                yield (
                    '<br><br><font color="#51B432">During handling of the '
                    "above exception, another exception occurred:</font><br>"
                )
            yield cgitb_html(exc)

        def cgitb_html(exc: Exception) -> str:
            """Format exception with cgitb.html."""
            info = (type(exc), exc, exc.__traceback__)
            return cgitb.html(info)

        def format_exc_info(exc: Exception, as_html: bool, color=None) -> str:
            info = (
                exc.__class__,
                exc,
                exc.__traceback__,
            )
            # avoids printing the array data
            try:
                import numpy as np

                np.set_string_function(lambda arr: f"{type(arr)} {arr.shape} {arr.dtype}")
                np_imported = True
            except ImportError:
                np_imported = False
            if as_html:
                html = "\n".join(cgitb_chain(info[1]))
                # cgitb has a lot of hardcoded colors that don't work for us
                # remove bgcolor, and let theme handle it
                html = re.sub('bgcolor="#.*"', "", html)
                # remove superfluous whitespace
                html = html.replace("<br>\n", "\n")
                # but retain it around the <small> bits
                html = re.sub(r"(<tr><td><small.*</tr>)", "<br>\\1<br>", html)
                # weird 2-part syntax is a workaround for hard-to-grep text.
                html = html.replace(
                    "<p>A problem occurred in a Python script.  "
                    "Here is the sequence of",
                    "",
                )
                html = html.replace(
                    "function calls leading up to the error, "
                    "in the order they occurred.</p>",
                    "<br>",
                )
                # remove hardcoded fonts
                html = html.replace("\n", "<br>")
                html = (
                    f"<span style='font-family: monaco,{font},"
                    "monospace;'>" + html + "</span>"
                )
                tb_text = html
            else:
                # if we don't need HTML, just use traceback
                tb_text = "".join(traceback.format_exception(*info))
            # resets to default behavior
            if np_imported:
                np.set_string_function(None)
            return tb_text

    return format_exc_info


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.LineEdit()
    widget.show()
    with app.debug_mode():
        with Stalker(widget) as stalker:
            app.sleep(3)
            print(stalker.counter)
        app.main_loop()
