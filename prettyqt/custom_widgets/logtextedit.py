# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys
import collections
import logging

from prettyqt import gui, widgets
from prettyqt.utils import signallogger


Point = collections.namedtuple('Point', ['x', 'y'])


class HighlightRule(object):
    placeholder: str
    color = "black"
    italic = False
    bold = False

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.format = cls.create_format()

    @classmethod
    def create_format(cls):
        fmt = gui.TextCharFormat()
        fmt.setFontItalic(cls.italic)
        fmt.set_foreground_color(cls.color)
        if cls.font_size:
            fmt.setFontPointSize(cls.font_size)
        if cls.bold:
            fmt.set_font_weight("bold")
        return fmt

    def get_format(self, value):
        return self.format


class AscTime(HighlightRule):
    placeholder = "%(asctime)s"
    color = "green"


class Message(HighlightRule):
    placeholder = "%(message)s"
    color = "blue"


class LevelName(HighlightRule):
    placeholder = "%(levelname)s"
    color = "red"


class LogTextEdit(widgets.PlainTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_font("Consolas")
        self.append_text(f"Python version: {sys.version}")
        logger = logging.getLogger()
        # self.handler = signallogger.LineSignalLogger()
        # self.handler.log_line.connect(self.append_text)
        self.handler = signallogger.RecordSignalLogger()
        self.handler.log_record.connect(self.append_record)
        logger.addHandler(self.handler)
        self.handler.setLevel(logging.WARNING)
        self.formatter = logging.Formatter('%(asctime)s - %(message)s')
        self.handler.setFormatter(self.formatter)

    def append_record(self, record):
        print(self.formatter.formatTime(record))
        dct = {"%(asctime)s": self.formatter.formatTime(record),
               # "%(created)f": record.created,
               # "%(filename)s": record.filename,
               # "%(funcName)s": record.funcName,
               "%(levelname)s": record.levelname,
               "%(levelno)s": record.levelno,
               # "%(lineno)d": record.lineno,
               "%(message)s": record.msg,
               # "%(module)s": record.module,
               # "%(msecs)d": record.msecs,
               # "%(name)s": record.name,
               # "%(pathname)s": record.pathname,
               # "%(process)d": record.process,
               # "%(processName)s": record.processName,
               # "%(relativeCreated)s": record.relativeCreated,
               # "%(thread)d": record.thread,
               "%(threadName)s": record.threadName}
        template = self.formatter._fmt
        replacements = dict()
        for placeholder, value in dct.items():
            pos = template.find(placeholder)
            if pos > -1:
                template = template.replace(placeholder, str(value))
                replacements[placeholder] = (pos, pos + len(value))
        print(replacements)
        self.append_text(template)


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.Widget()
    w.set_layout("vertical")
    widget = LogTextEdit()
    logger = logging.getLogger()
    w.box.add(widgets.PushButton("Debug", callback=lambda: logger.debug("Debug")))
    w.box.add(widgets.PushButton("Info", callback=lambda: logger.info("Info")))
    w.box.add(widgets.PushButton("Warning", callback=lambda: logger.warning("Warning")))
    w.box.add(widgets.PushButton("Critical",
                                 callback=lambda: logger.critical("Critical")))
    w.box.add(widget)
    w.show()
    app.exec_()
