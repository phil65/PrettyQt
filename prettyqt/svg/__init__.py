"""svg module.

contains QtSvg-based classes
"""

from prettyqt.qt.QtSvg import *  # noqa: F403

from .svggenerator import SvgGenerator
from .svgrenderer import SvgRenderer
from prettyqt.qt import QtSvg

QT_MODULE = QtSvg

__all__ = ["SvgGenerator", "SvgRenderer"]
