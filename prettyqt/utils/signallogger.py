from __future__ import annotations

import logging

from prettyqt import core


class LineSignalLogger(logging.Handler, core.Object):
    log_line = core.Signal(str)

    def __init__(self):
        super().__init__()
        core.Object.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        self.log_line.emit(msg)


class Signals(core.Object):
    log_record = core.Signal(logging.LogRecord)


class RecordSignalLogger(logging.Handler):
    def __init__(self):
        super().__init__()
        self.signals = Signals()

    def emit(self, record):
        self.signals.log_record.emit(record)
