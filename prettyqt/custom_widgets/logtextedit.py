from __future__ import annotations

import logging
import re
import sys
import traceback
from typing import ClassVar

from prettyqt import core, gui, widgets
from prettyqt.utils import signallogger


logger = logging.getLogger(__name__)

# from SublimeText Regex:
# (?x:
#   (?:.? [<>=^])?     # fill align
#   [ +-]?             # sign
#   \#?                # alternate form
#   # technically, octal and hexadecimal integers are also supported as 'width'
#   \d*                # width
#   ,?                 # thousands separator
#   (?:\.\d+)?         # precision
#   [bcdeEfFgGnosxX%]? # type
# )


class Highlighter:
    placeholder: str
    color: str | None = None
    italic: bool = False
    bold: bool = False

    def __init__(self, formatter: logging.Formatter):
        self.formatter = formatter
        self.format = gui.TextCharFormat(self.color, self.bold, self.italic)
        text = re.escape(self.placeholder)
        pat = rf"{text[:-1]}([ +-]?\#?\#?\d*,?(?:\.\d+)?[bcdeEfFgGnosxX%]?)"
        self.pattern = re.compile(pat)
        if self.formatter._fmt is None:
            msg = "Formatter does not contain format string"
            raise TypeError(msg)
        self.is_included = self.pattern.search(self.formatter._fmt) is not None

    def get_format(self, value) -> gui.TextCharFormat:
        return self.format

    def format_string(self, record: logging.LogRecord):
        raise NotImplementedError


class AscTime(Highlighter):
    placeholder = "%(asctime)s"
    italic = True

    def format_string(self, record: logging.LogRecord) -> str:
        return self.formatter.formatTime(record)


class Message(Highlighter):
    placeholder = "%(message)s"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        if record.exc_info is not None:
            val = self.formatter.formatException(record.exc_info)
        elif isinstance(record.msg, Exception):
            val = traceback.format_exc()
        else:
            val = record.msg % record.args
        return f"\n{val}" if "\n" in val else val


class FileName(Highlighter):
    placeholder = "%(filename)s"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return record.filename


class FuncName(Highlighter):
    placeholder = "%(funcName)s"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return record.funcName


class Module(Highlighter):
    placeholder = "%(module)s"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return record.module


class Created(Highlighter):
    placeholder = "%(created)f"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return str(record.created)


class LineNo(Highlighter):
    placeholder = "%(lineno)d"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return str(record.lineno)


class Msecs(Highlighter):
    placeholder = "%(msecs)d"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return str(record.msecs)


class Process(Highlighter):
    placeholder = "%(process)d"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return str(record.process)


class Thread(Highlighter):
    placeholder = "%(thread)d"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return str(record.thread)


class ThreadName(Highlighter):
    placeholder = "%(threadName)s"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        name = record.threadName
        return name or ""


class ProcessName(Highlighter):
    placeholder = "%(processName)s"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        name = record.processName
        return name or ""


class RelativeCreated(Highlighter):
    placeholder = "%(relativeCreated)s"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return str(record.relativeCreated)


class Name(Highlighter):
    placeholder = "%(name)s"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return record.name


class PathName(Highlighter):
    placeholder = "%(pathname)s"
    bold = True

    def format_string(self, record: logging.LogRecord) -> str:
        return record.pathname


class LevelName(Highlighter):
    placeholder = "%(levelname)s"
    color = "red"
    formats: ClassVar = dict(
        DEBUG=gui.TextCharFormat(text_color="green", bold=True),
        INFO=gui.TextCharFormat(text_color="blue", bold=True),
        WARNING=gui.TextCharFormat(text_color="orange", bold=True),
        CRITICAL=gui.TextCharFormat(text_color="darkorange", bold=True),
        ERROR=gui.TextCharFormat(text_color="red", bold=True),
    )

    def format_string(self, record: logging.LogRecord) -> str:
        return record.levelname

    def get_format(self, value) -> gui.TextCharFormat:
        return self.formats[value]


class LogTextEdit(widgets.PlainTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rules = []
        self.allow_wheel_zoom()
        self.set_font(gui.Font.mono(as_qt=True))
        self.append_text(f"Python version: {sys.version}")
        new_logger = logging.getLogger()
        # self.handler = signallogger.LineSignalLogger()
        # self.handler.log_line.connect(self.append_text)
        self.handler = signallogger.SignalLogger()
        self.handler.signals.log_record.connect(self.append_record)
        core.CoreApplication.call_on_exit(lambda: new_logger.removeHandler(self.handler))
        self.handler.setLevel(logging.INFO)
        new_logger.addHandler(self.handler)
        fmt = logging.Formatter("%(asctime)s  %(levelname)s  %(message)s")
        self.set_formatter(fmt)

    def set_formatter(self, formatter: logging.Formatter):
        self.formatter = formatter
        rules = [klass(self.formatter) for klass in Highlighter.__subclasses__()]
        self.rules = [r for r in rules if r.is_included]
        self.handler.setFormatter(formatter)

    def append_record(self, record: logging.LogRecord):
        start_of_line = len(self.text())
        if self.formatter._fmt is None:
            msg = "Formatter does not contain format string"
            raise TypeError(msg)
        self.append_text(self.formatter._fmt)
        old_fmt = self.textCursor().charFormat()
        with self.selecter.create_cursor() as c:
            c.move_position("end")
            c.move_position("start_of_block")
            start_pos = c.position()
            for r in self.rules:
                line_text = c.select_text(start_pos, "end_of_block")
                matches = list(r.pattern.finditer(line_text))
                for m in reversed(matches):
                    pos = m.start(0) + start_of_line
                    if start_of_line != 0:
                        pos += 1
                    end = pos + m.end(0) - m.start(0)
                    fmt_string = r.format_string(record)
                    try:
                        value = f"%{m.group(1)}" % fmt_string
                    except (TypeError, ValueError):
                        value = fmt_string
                    c.replace_text(pos, end, value)
                    fmt = r.get_format(fmt_string)
                    c.setCharFormat(fmt)
                    c.clearSelection()
                    c.setCharFormat(old_fmt)


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.Widget()
    w.set_layout("vertical")
    widget = LogTextEdit()
    logger = logging.getLogger()

    def raise_exc():
        try:
            msg = "test"
            raise Exception(msg)  # noqa: TRY002, TRY301
        except Exception:
            logger.exception("Exception!")

    w.box.add(widgets.PushButton("Raise", clicked=raise_exc))
    w.box.add(widgets.PushButton("Debug", clicked=lambda: logger.debug("Debug")))
    w.box.add(widgets.PushButton("Info", clicked=lambda: logger.info("Info")))
    w.box.add(widgets.PushButton("Warning", clicked=lambda: logger.warning("Warning")))
    w.box.add(widgets.PushButton("Critical", clicked=lambda: logger.critical("Critical")))
    w.box.add(widget)
    w.show()
    app.exec()
