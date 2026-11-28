"""Text editor component for Qt."""

from prettyqt.qt.Qsci import *  # noqa: F403

from .sciscintilla import SciScintilla
from prettyqt.qt import Qsci

QT_MODULE = Qsci

__all__ = ["SciScintilla"]
