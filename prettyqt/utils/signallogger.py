from __future__ import annotations

import logging

from prettyqt import core


class SignalLogger(core.Object, logging.Handler):
    formatted_line = core.Signal(str)
    log_record = core.Signal(logging.LogRecord)

    def emit(self, record):
        msg = self.format(record)
        self.formatted_line.emit(msg)
        self.log_record.emit(record)
