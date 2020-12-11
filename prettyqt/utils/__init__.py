"""Module containing helper functions."""

import sys
from typing import Iterable, TYPE_CHECKING
import traceback
import logging

import bidict as bdct

if TYPE_CHECKING:
    from qtpy import QtCore
    import datetime

logger = logging.getLogger(__name__)


def to_datetime(date: "QtCore.QDateTime") -> "datetime.datetime":
    try:
        return date.toPython()  # pyqt5
    except (AttributeError, TypeError):
        return date.toPyDateTime()


def to_date(date: "QtCore.QDate") -> "datetime.date":
    try:
        return date.toPython()  # pyqt5
    except (AttributeError, TypeError):
        return date.toPyDate()


def to_time(time: "QtCore.QTime") -> "datetime.time":
    try:
        return time.toPython()  # pyqt5
    except (AttributeError, TypeError):
        return time.toPyTime()


class bidict(bdct.bidict):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            super().__init__(args[0])
        else:
            super().__init__(kwargs)


class InvalidParamError(ValueError):
    """Exception raised for invalid params in method calls.

    Args:
        value: param value which caused the error
        valid_options: allowed options
    """

    def __init__(self, value, valid_options: Iterable):
        self.value = value
        opts = " / ".join(repr(opt) for opt in valid_options)
        self.message = f"Invalid value: {value!r}. Allowed options are {opts}."
        super().__init__(self.message)


def install_exceptionhook(debug=False):
    def handleException(exc_type, exc_value, exc_traceback):
        """Causes the application to quit in case of an unhandled exception.

        Shows an error dialog before quitting when not in debugging mode.
        """
        logger.critical(
            f"Bug: uncaught {exc_type.__name__}",
            exc_info=(exc_type, exc_value, exc_traceback),
        )
        if debug:
            sys.exit(1)
        else:
            from prettyqt import widgets

            # Constructing a QApplication in case this hasn't been done yet.
            _ = widgets.app()
            lst = traceback.format_exception(exc_type, exc_value, exc_traceback)
            msgBox = widgets.MessageBox(
                icon="warning",
                text=f"Bug: uncaught {exc_type.__name__}",
                informative_text=str(exc_value),
                details="".join(lst),
            )
            msgBox.exec_()
            sys.exit(1)

    sys.excepthook = handleException
