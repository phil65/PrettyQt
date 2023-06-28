"""svg module.

contains QtSvg-based classes
"""

from prettyqt.qt.QtSvg import *  # noqa: F403

from .svggenerator import SvgGenerator
from .svgrenderer import SvgRenderer


__all__ = ["SvgGenerator", "SvgRenderer"]
