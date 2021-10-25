"""svg module.

contains QtSvg-based classes
"""

from prettyqt import core

from .svggenerator import SvgGenerator
from .svgrenderer import SvgRenderer

if core.VersionNumber.get_qt_version() < (6, 0, 0):
    from .graphicssvgitem import GraphicsSvgItem
    from .svgwidget import SvgWidget


__all__ = ["GraphicsSvgItem", "SvgGenerator", "SvgRenderer", "SvgWidget"]
