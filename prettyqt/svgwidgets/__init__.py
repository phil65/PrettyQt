"""Widgets for displaying SVG files."""

from prettyqt.qt.QtSvgWidgets import *  # noqa: F403

from .graphicssvgitem import GraphicsSvgItem
from .svgwidget import SvgWidget
from prettyqt.qt import QtSvgWidgets

QT_MODULE = QtSvgWidgets

__all__ = ["GraphicsSvgItem", "SvgWidget"]
