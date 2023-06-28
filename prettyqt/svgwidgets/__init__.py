"""svg module.

contains QtSvgWidgets-based classes
"""

from prettyqt.qt.QtSvgWidgets import *  # noqa: F403

from .svgwidget import SvgWidget
from .graphicssvgitem import GraphicsSvgItem


__all__ = ["SvgWidget", "GraphicsSvgItem"]
