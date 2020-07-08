# -*- coding: utf-8 -*-
"""

for full list, see:
- https://cdn.materialdesignicons.com/3.0.39/
"""

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


class RecordSignalLogger(logging.Handler, core.Object):
    log_record = core.Signal(logging.LogRecord)

    def __init__(self):
        super().__init__()
        core.Object.__init__(self)

    def emit(self, record):
        self.log_record.emit(record)
