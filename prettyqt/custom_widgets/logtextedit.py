# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys
import logging
import re

from prettyqt import gui, widgets, constants
from prettyqt.utils import signallogger


class Highlighter(object):
    placeholder: str
    color = "black"
    italic = False
    bold = False
    value = None

    def __init__(self, formatter):
        self.formatter = formatter
        self.format = gui.TextCharFormat(self.color, self.bold, self.italic)
        text = re.escape(self.placeholder)
        self.pattern = re.compile(f"{text[:-1]}(.*?{text[-1]})")
        self.is_included = self.pattern.search(self.formatter._fmt) is not None

    def get_format(self, value):
        return self.format

    def format_string(self):
        raise NotImplementedError()


class AscTime(Highlighter):
    placeholder = "%(asctime)s"
    italic = True

    def format_string(self, record):
        return self.formatter.formatTime(record)


class Message(Highlighter):
    placeholder = "%(message)s"
    bold = True

    def format_string(self, record):
        if isinstance(record.msg, Exception):
            val = self.formatter.formatException(record.exc_info)
        else:
            val = record.msg % record.args
        if "\n" in val:
            val = f"\n{val}"
        return val


class FileName(Highlighter):
    placeholder = "%(filename)s"
    bold = True

    def format_string(self, record):
        return record.filename


class FuncName(Highlighter):
    placeholder = "%(funcName)s"
    bold = True

    def format_string(self, record):
        return record.funcName


class Module(Highlighter):
    placeholder = "%(module)s"
    bold = True

    def format_string(self, record):
        return record.module


class Created(Highlighter):
    placeholder = "%(created)f"
    bold = True

    def format_string(self, record):
        return str(record.created)


class LineNo(Highlighter):
    placeholder = "%(lineno)d"
    bold = True

    def format_string(self, record):
        return str(record.lineno)


class Msecs(Highlighter):
    placeholder = "%(msecs)d"
    bold = True

    def format_string(self, record):
        return str(record.msecs)


class Process(Highlighter):
    placeholder = "%(process)d"
    bold = True

    def format_string(self, record):
        return str(record.process)


class Thread(Highlighter):
    placeholder = "%(thread)d"
    bold = True

    def format_string(self, record):
        return str(record.thread)


class ThreadName(Highlighter):
    placeholder = "%(threadName)s"
    bold = True

    def format_string(self, record):
        return record.threadName


class ProcessName(Highlighter):
    placeholder = "%(processName)s"
    bold = True

    def format_string(self, record):
        return record.processName


class RelativeCreated(Highlighter):
    placeholder = "%(relativeCreated)s"
    bold = True

    def format_string(self, record):
        return record.relativeCreated


class Name(Highlighter):
    placeholder = "%(name)s"
    bold = True

    def format_string(self, record):
        return record.name


class PathName(Highlighter):
    placeholder = "%(pathname)s"
    bold = True

    def format_string(self, record):
        return record.pathname


class LevelName(Highlighter):
    placeholder = "%(levelname)s"
    color = "red"
    formats = dict(DEBUG=gui.TextCharFormat(text_color="green", bold=True),
                   INFO=gui.TextCharFormat(text_color="blue", bold=True),
                   WARNING=gui.TextCharFormat(text_color="orange", bold=True),
                   CRITICAL=gui.TextCharFormat(text_color="darkorange", bold=True),
                   ERROR=gui.TextCharFormat(text_color="red", bold=True))

    def format_string(self, record):
        return record.levelname

    def get_format(self, value):
        return self.formats[value]


class LogTextEdit(widgets.PlainTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_font("Consolas")
        self.formatter = None
        self.append_text(f"Python version: {sys.version}")
        logger = logging.getLogger()
        # self.handler = signallogger.LineSignalLogger()
        # self.handler.log_line.connect(self.append_text)
        self.handler = signallogger.RecordSignalLogger()
        self.handler.log_record.connect(self.append_record)
        self.handler.setLevel(logging.INFO)
        logger.addHandler(self.handler)
        fmt = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')
        self.set_formatter(fmt)

    def wheelEvent(self, event):
        """
        handle wheel event for zooming
        """
        if event.modifiers() & constants.CTRL_MOD:
            self.zoomIn() if event.angleDelta().y() > 0 else self.zoomOut()
        else:
            super().wheelEvent(event)

    def set_formatter(self, formatter):
        self.formatter = formatter
        self.handler.setFormatter(self.formatter)
        rules = [klass(self.formatter) for klass in Highlighter.__subclasses__()]
        self.rules = [r for r in rules if r.is_included]

    def append_record(self, record):
        start_of_line = len(self.text())
        self.append_text(self.formatter._fmt)
        with self.current_cursor() as c:
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
                    value = f"%{m.group(1)}" % fmt_string
                    c.replace_text(pos, end, value)
                    fmt = r.get_format(fmt_string)
                    c.setCharFormat(fmt)
            c.clearSelection()


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.Widget()
    w.set_layout("vertical")
    widget = LogTextEdit()
    logger = logging.getLogger()

    def raise_exc():
        try:
            raise Exception("test")
        except Exception as e:
            logger.exception(e)

    w.box.add(widgets.PushButton("Raise", callback=raise_exc))
    w.box.add(widgets.PushButton("Debug", callback=lambda: logger.debug("Debug")))
    w.box.add(widgets.PushButton("Info", callback=lambda: logger.info("Info")))
    w.box.add(widgets.PushButton("Warning", callback=lambda: logger.warning("Warning")))
    w.box.add(widgets.PushButton("Critical",
                                 callback=lambda: logger.critical("Critical")))
    w.box.add(widget)
    w.show()
    app.exec_()
