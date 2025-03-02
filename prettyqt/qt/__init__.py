"""Provides Qt init stuff."""

import os
import sys

from typing import Literal
import warnings


API_NAMES = {"pyqt6": "PyQt6", "pyside6": "PySide6"}


DEFAULT = "pyqt6"

# Detecting if a binding was specified by the user
binding_specified = "QT_API" in os.environ
API = os.environ.get("QT_API", DEFAULT).lower()

if API.lower() in {"pyqt5", "pyside2"}:
    API = DEFAULT
    binding_specified = False

initial_api = API
if API not in API_NAMES:
    msg = f"Specified QT_API={repr(API)!r} is not in valid options: {API_NAMES}"
    raise ValueError(msg)


PYQT6 = False
PYSIDE6 = False

API_VERSION = None
QT_VERSION = None


if "PyQt6" in sys.modules:
    API = "pyqt6"
elif "PySide6" in sys.modules:
    API = "pyside6"

if API == "pyqt6":
    try:
        from PyQt6.QtCore import (
            PYQT_VERSION_STR as API_VERSION,  # analysis:ignore
            QT_VERSION_STR as QT_VERSION,  # analysis:ignore
        )

        PYQT6 = True

    except ImportError:
        API = "pyside6"
    # else:
    #     os.environ["QT_API"] = API

if API == "pyside6":
    try:
        from PySide6 import (
            __version__ as API_VERSION,  # noqa: F401, N812
        )  # analysis:ignore
        from PySide6.QtCore import (
            __version__ as QT_VERSION,  # noqa: F401, N812
        )  # analysis:ignore

        PYSIDE6 = True

    except ImportError as e:
        raise ImportError(API) from e
    # else:
    #     os.environ["QT_API"] = API


# If a correct API name is passed to QT_API and it could not be found,
# switches to another and informs through the warning
if initial_api != API and binding_specified:
    warnings.warn(
        f"Selected binding {initial_api!r} not found. Falling back to {API!r}",
        ImportWarning,
        stacklevel=2,
    )


# Set display name of the Qt API
API_NAME = API_NAMES[API]
MODULE = sys.modules[API_NAME]


def set_env_vars(qt_binding: Literal["PyQt6", "PySide6"]):
    env_vars = ["QT_API", "USE_QT_API", "PYTEST_QT_API", "PYQTGRAPH_QT_LIB"]
    for var in env_vars:
        os.environ[var] = qt_binding


set_env_vars(API_NAME)


# from prettyqt.qt import QtCore, QtGui, QtWidgets
# from prettyqt import paths
# import inspect
# import pathlib

# module_dict = dict(QtWidgets=QtWidgets, QtGui=QtGui, QtCore=QtCore)

# for module_name, module in module_dict.items():
#     clsmembers = inspect.getmembers(module, inspect.isclass)
#     for klass_name, klass in clsmembers:
#         path = paths.DOCSTRING_PATH /  module_name
#         filepath = path / f"{klass_name}.txt"
#         if filepath.exists():
#             # print(klass_name)
#             text = filepath.read_text()
#             klass.__doc__ = text
