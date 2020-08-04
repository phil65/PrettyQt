# -*- coding: utf-8 -*-
"""Module containing helper functions."""

import sys
from typing import Mapping, Union, Iterable
import traceback
import logging

import bidict as bdct

logger = logging.getLogger(__name__)


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

    def __init__(self, value, valid_options: Union[Iterable, Mapping, bidict]):
        self.value = value
        if isinstance(valid_options, Mapping):
            self.valid_options = valid_options.keys()
        else:
            self.valid_options = valid_options
        opts = " / ".join(repr(opt) for opt in valid_options)
        self.message = f"Invalid value: {value!r}. Allowed options are {opts}."
        super().__init__(self.message)


def install_exceptionhook(debug=False):
    def handleException(exc_type, exc_value, exc_traceback):
        """Causes the application to quit in case of an unhandled exception.

        Shows an error dialog before quitting when not in debugging mode.
        """
        logger.critical(
            "Bug: uncaught {}".format(exc_type.__name__),
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
                detail_text="".join(lst),
            )
            msgBox.exec_()
            sys.exit(1)

    sys.excepthook = handleException
