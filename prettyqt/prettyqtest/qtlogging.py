from __future__ import annotations

from collections import namedtuple
from contextlib import contextmanager
import datetime
import re

from py._code.code import ReprFileLocation, TerminalRepr
import pytest

from prettyqt import core
import prettyqt.qt


class QtLoggingPlugin:
    """Plugin responsible for installing a QtMessageHandler before each test.

    Augment reporting if the test failed with the messages captured.
    """

    LOG_FAIL_OPTIONS = ["NO", "CRITICAL", "WARNING", "DEBUG", "INFO"]

    def __init__(self, config):
        self.config = config

    def pytest_runtest_setup(self, item):
        if item.get_closest_marker("no_qt_log"):
            return
        m = item.get_closest_marker("qt_log_ignore")
        if m:
            if not set(m.kwargs).issubset({"extend"}):
                raise ValueError(
                    "Invalid keyword arguments in {!r} for "
                    "qt_log_ignore mark.".format(m.kwargs)
                )
            if m.kwargs.get("extend", True):
                config_regexes = self.config.getini("qt_log_ignore")
                ignore_regexes = config_regexes + list(m.args)
            else:
                ignore_regexes = m.args
        else:
            ignore_regexes = self.config.getini("qt_log_ignore")
        item.qt_log_capture = _QtMessageCapture(ignore_regexes)
        item.qt_log_capture._start()

    @pytest.mark.hookwrapper
    def pytest_runtest_makereport(self, item, call):
        """Add captured Qt messages to test item report if the call failed."""
        outcome = yield
        if not hasattr(item, "qt_log_capture"):
            return

        if call.when == "call":
            report = outcome.get_result()

            m = item.get_closest_marker("qt_log_level_fail")
            if m:
                log_fail_level = m.args[0]
            else:
                log_fail_level = self.config.getini("qt_log_level_fail")
            assert log_fail_level in QtLoggingPlugin.LOG_FAIL_OPTIONS

            # make test fail if any records were captured which match
            # log_fail_level
            if report.outcome != "failed":
                for rec in item.qt_log_capture.records:
                    is_modeltest_error = (
                        rec.context is not None
                        and rec.context.category == "qt.modeltest"
                        and rec.matches_level("WARNING")
                    )
                    if (
                        rec.matches_level(log_fail_level) and not rec.ignored
                    ) or is_modeltest_error:
                        report.outcome = "failed"
                        if report.longrepr is None:
                            report.longrepr = _QtLogLevelErrorRepr(
                                item, log_fail_level, is_modeltest_error
                            )
                        break

            # if test has failed, add recorded messages to its terminal
            # representation
            if not report.passed:
                long_repr = getattr(report, "longrepr", None)
                if hasattr(long_repr, "addsection"):  # pragma: no cover
                    log_format = self.config.getoption("qt_log_format")
                    context_format = None
                    if log_format is None:
                        if prettyqt.qt.API.startswith("pyqt"):
                            context_format = (
                                "{rec.context.file}:{rec.context.function}:"
                                "{rec.context.line}:\n"
                            )
                            log_format = "    {rec.type_name}: {rec.message}"
                        else:
                            context_format = None
                            log_format = "{rec.type_name}: {rec.message}"
                    lines = []
                    for rec in item.qt_log_capture.records:
                        suffix = " (IGNORED)" if rec.ignored else ""

                        if (
                            rec.context is not None
                            and (
                                rec.context.file is not None
                                or rec.context.function is not None
                                or rec.context.line != 0
                            )
                            and context_format is not None
                        ):
                            context_line = context_format.format(rec=rec)
                            lines.append(context_line)

                        line = log_format.format(rec=rec) + suffix
                        lines.append(line)
                    if lines:
                        long_repr.addsection("Captured Qt messages", "\n".join(lines))

            item.qt_log_capture._stop()
            del item.qt_log_capture


class _QtMessageCapture:
    """Capture Qt messages when its `handle` method is installed using qInstallMsgHandler.

    Stores them into `records` attribute.

    :attr _records: list of Record instances.
    :attr _ignore_regexes: list of regexes (as strings) that define if a record
        should be ignored.
    """

    def __init__(self, ignore_regexes):
        self._records = []
        self._ignore_regexes = ignore_regexes or []
        self._previous_handler = None

    def _start(self):
        """Start receiving messages from Qt."""
        previous_handler = core.install_message_handler(self._handle_with_context)
        self._previous_handler = previous_handler

    def _stop(self):
        """Stop receiving messages from Qt, restoring the previously installed handler."""
        core.install_message_handler(self._previous_handler)

    @contextmanager
    def disabled(self):
        """Context manager that temporarily disables logging capture while inside it."""
        self._stop()
        try:
            yield
        finally:
            self._start()

    _Context = namedtuple("_Context", "file function line category")

    def _append_new_record(self, msg_type, message, context):
        """Create a new Record instance and stores it.

        :param msg_type: Qt message typ
        :param message: message string, if bytes it will be converted to str.
        :param context: QMessageLogContext object or None
        """

        def to_unicode(s):
            if isinstance(s, bytes):
                s = s.decode("utf-8", "replace")
            return s

        message = to_unicode(message)

        ignored = False
        for regex in self._ignore_regexes:
            if re.search(regex, message) is not None:
                ignored = True
                break

        if context is not None:
            context = self._Context(
                to_unicode(context.file),
                to_unicode(context.function),
                context.line,
                to_unicode(context.category),
            )

        self._records.append(Record(msg_type, message, ignored, context))

    def _handle_with_context(self, msg_type, context, message):
        """Method to be installed using qInstallMessageHandler, stores each message."""
        self._append_new_record(msg_type, message, context=context)

    @property
    def records(self):
        """Access messages captured so far.

        :rtype: list of `Record` instances.
        """
        return self._records[:]


class Record:
    """Hold information about a message sent by one of Qt log functions.

    :ivar str message: message contents.
    :ivar Qt.QtMsgType type: enum that identifies message type
    :ivar str type_name: ``type`` as string: ``"QtInfoMsg"``, ``"QtDebugMsg"``,
        ``"QtWarningMsg"`` or ``"QtCriticalMsg"``.
    :ivar str log_type_name:
        type name similar to the logging package: ``INFO``, ``DEBUG``,
        ``WARNING`` and ``CRITICAL``.
    :ivar datetime.datetime when: when the message was captured
    :ivar bool ignored: If this record matches a regex from the "qt_log_ignore"
        option.
    :ivar context: a namedtuple containing the attributes ``file``,
        ``function``, ``line``. Only available in Qt5, otherwise is None.
    """

    _type_name_map = {
        core.DebugMsg: "QtDebugMsg",
        core.WarningMsg: "QtWarningMsg",
        core.CriticalMsg: "QtCriticalMsg",
        core.FatalMsg: "QtFatalMsg",
        core.InfoMsg: "QtInfoMsg",
    }

    _log_type_name_map = {
        core.DebugMsg: "DEBUG",
        core.WarningMsg: "WARNING",
        core.CriticalMsg: "CRITICAL",
        core.FatalMsg: "FATAL",
        core.InfoMsg: "INFO",
    }

    def __init__(self, msg_type, message: str, ignored: bool, context):
        self._type = msg_type
        self._message = message
        self._type_name = self._get_msg_type_name(msg_type)
        self._log_type_name = self._get_log_type_name(msg_type)
        self._when = datetime.datetime.now()
        self._ignored = ignored
        self._context = context

    message = property(lambda self: self._message)
    type = property(lambda self: self._type)
    type_name = property(lambda self: self._type_name)
    log_type_name = property(lambda self: self._log_type_name)
    when = property(lambda self: self._when)
    ignored = property(lambda self: self._ignored)
    context = property(lambda self: self._context)

    @classmethod
    def _get_msg_type_name(cls, msg_type):
        """Return a string representation of the given QtMsgType enum value."""
        return cls._type_name_map[msg_type]

    @classmethod
    def _get_log_type_name(cls, msg_type):
        """Return a string repr of the given QtMsgType enum value.

        Use style used by the builtin logging package.
        """
        return cls._log_type_name_map[msg_type]

    def matches_level(self, level):
        assert level in QtLoggingPlugin.LOG_FAIL_OPTIONS
        if level == "NO":
            return False
        elif level == "INFO":
            return self.log_type_name in ("INFO", "DEBUG", "WARNING", "CRITICAL")
        elif level == "DEBUG":
            return self.log_type_name in ("DEBUG", "WARNING", "CRITICAL")
        elif level == "WARNING":
            return self.log_type_name in ("WARNING", "CRITICAL")
        elif level == "CRITICAL":
            return self.log_type_name in ("CRITICAL",)
        else:  # pragma: no cover
            raise ValueError(f"log_fail_level unknown: {level}")


class _QtLogLevelErrorRepr(TerminalRepr):
    """TerminalRepr of a test which emitted messages at or above the allowed level."""

    def __init__(self, item, level, is_modeltest_error):
        if is_modeltest_error:
            msg = "Qt modeltester errors"
        else:
            msg = "Failure: Qt messages with level {0} or above emitted"
        path, line_index, _ = item.location
        self.fileloc = ReprFileLocation(
            path, lineno=line_index + 1, message=msg.format(level.upper())
        )
        self.sections = []

    def addsection(self, name, content, sep="-"):
        self.sections.append((name, content, sep))

    def toterminal(self, out):
        self.fileloc.toterminal(out)
        for name, content, sep in self.sections:
            out.sep(sep, name)
            out.line(content)
