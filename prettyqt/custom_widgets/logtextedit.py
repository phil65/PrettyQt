# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys
import logging

from prettyqt import gui, widgets
from prettyqt.utils import signallogger


red_text = gui.TextCharFormat(text_color="red", bold=True)
green_text = gui.TextCharFormat(text_color="green", bold=True)
blue_text = gui.TextCharFormat(text_color="red", bold=True)
orange_text = gui.TextCharFormat(text_color="orange", bold=True)


class Highlighter(object):
    placeholder: str
    color = "black"
    italic = False
    bold = False
    value = None

    def __init__(self, formatter):
        self.formatter = formatter

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.format = gui.TextCharFormat(cls.color, cls.bold, cls.italic)

    def get_format(self, value):
        return self.format

    def get_value(self):
        return str(self.value())


class AscTime(Highlighter):
    placeholder = "%(asctime)s"
    italic = True

    def get_value(self, record):
        return self.formatter.formatTime(record)


class Message(Highlighter):
    placeholder = "%(message)s"
    bold = True

    def get_value(self, record):
        return record.msg


class LevelName(Highlighter):
    placeholder = "%(levelname)s"
    color = "red"
    formats = dict(DEBUG=green_text,
                   INFO=blue_text,
                   WARNING=orange_text,
                   CRITICAL=red_text,
                   ERROR=red_text)

    def get_value(self, record):
        return record.levelname

    def get_format(self, value):
        return self.formats[value]


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
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.rules = [klass(self.formatter) for klass in Highlighter.__subclasses__()]
        logger.addHandler(self.handler)

    def append_record(self, record):
        template = self.formatter._fmt
        start_of_line = len(self.text())
        self.append_text(template)
        with self.current_cursor() as c:
            c.move_position("end")
            for r in self.rules:
                c.move_position("start_of_block")
                c.move_position("end_of_block", "keep")
                line_text = c.selectedText()
                pos = line_text.find(r.placeholder)
                if pos > -1:
                    pos += start_of_line
                    if start_of_line != 0:
                        pos += 1
                    c.set_position(pos)
                    end = pos + len(r.placeholder)
                    c.select_text(pos, end)
                    value = r.get_value(record)
                    # print(f"replacing {r.placeholder} ({pos} - {end}) with {value}")
                    c.insertText(value)
                    c.select_text(pos, pos + len(value))
                    text = c.selectedText()
                    fmt = r.get_format(text)
                    c.setCharFormat(fmt)
            c.clearSelection()


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
