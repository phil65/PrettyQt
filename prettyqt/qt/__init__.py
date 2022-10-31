"""Provides Qt init stuff."""

from typing import Callable, Literal
import operator
import os
import importlib


class PythonQtError(ImportError):
    pass


def set_env_vars(qt_binding: Literal["PyQt5", "PyQt6", "PySide2", "PySide6"]):
    ENV_VARS = ["QT_API", "USE_QT_API", "PYTEST_QT_API", "PYQTGRAPH_QT_LIB"]
    for var in ENV_VARS:
        os.environ[var] = qt_binding


# the order in the tuple represents the search order when importing the package
packages = {
    "pyside6": "PySide6",
    "pyqt6": "PyQt6",
    "pyside2": "PySide2",
    "pyqt5": "PyQt5",
}

qt_api = os.getenv("QT_API")

# one can create a QT_API environment variable to select which Qt API to use
if qt_api:
    qt_api = qt_api.lower()
    if qt_api not in packages.keys():
        raise ValueError(f"Invalid QT_API environment variable {qt_api!r}")
else:
    for name, pkg_name in packages.items():
        try:
            importlib.import_module(pkg_name)
        except ImportError:
            continue
        else:
            qt_api = name
            break

if not qt_api:
    pkg_str = ", ".join(packages)
    raise ImportError(f"One of the following Qt packages must be installed: {pkg_str}")

# os.environ.setdefault("QT_API", "pyqt6")

API = qt_api
QT_VERSION = 6 if API.endswith("6") else 5

PYQT5 = API == "pyqt5"
PYQT6 = API == "pyqt6"
PYSIDE2 = API == "pyside2"
PYSIDE6 = API == "pyside6"


flag_to_int: Callable = (
    operator.attrgetter("value") if API.endswith("6") else int  # type: ignore
)
