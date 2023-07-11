from __future__ import annotations

import logging

from prettyqt import core


class Signals(core.Object):
    formatted_line = core.Signal(str)
    log_record = core.Signal(logging.LogRecord)


class SignalLogger(logging.Handler):
    # formatted_line = core.Signal(str)
    # log_record = core.Signal(logging.LogRecord)
    # multiple inheritance doesnt work for PySide6 here
    def __init__(self):
        super().__init__()
        # core.Object.__init__(self)
        self.signals = Signals()

    def emit(self, record):
        msg = self.format(record)
        try:
            self.signals.formatted_line.emit(msg)
            self.signals.log_record.emit(record)
        except RuntimeError:
            pass
