"""Text editor component for Qt."""

from .sciscintilla import SciScintilla
from prettyqt.qt import Qsci

QT_MODULE = Qsci

__all__ = ["SciScintilla"]
