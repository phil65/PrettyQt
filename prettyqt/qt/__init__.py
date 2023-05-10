"""Provides Qt init stuff."""

from typing import Literal

import os
import qtpy


class PythonQtError(ImportError):
    pass


def set_env_vars(qt_binding: Literal["PyQt6", "PySide6"]):
    ENV_VARS = ["QT_API", "USE_QT_API", "PYTEST_QT_API", "PYQTGRAPH_QT_LIB"]
    for var in ENV_VARS:
        os.environ[var] = qt_binding


API = qtpy.API

if API not in {"pyqt6", "pyside6"}:
    raise RuntimeError("Error when detecting Qt Bindings.")

API_NAME = "PyQt6" if API == "pyqt6" else "PySide6"
set_env_vars(API_NAME)


PYQT6 = API.lower() == "pyqt6"
PYSIDE6 = API.lower() == "pyside6"
