# -*- coding: utf-8 -*-

"""Gui module.

Contains QtGui-based classes
"""

from qtpy.QtGui import QKeyEvent as KeyEvent
from qtpy.QtGui import QMouseEvent as MouseEvent
from qtpy.QtGui import QWheelEvent as WheelEvent
from qtpy.QtGui import QActionEvent as ActionEvent
from qtpy.QtGui import QShowEvent as ShowEvent
from qtpy.QtGui import QContextMenuEvent as ContextMenuEvent

from .keysequence import KeySequence
from .gradient import Gradient
from .icon import Icon
from .guiapplication import GuiApplication
from .validator import Validator
from .regexpvalidator import RegExpValidator

try:
    from .regularexpressionvalidator import RegularExpressionValidator
except AttributeError:
    from .regularexpressionvalidator_pyside import (  # type: ignore
        RegularExpressionValidator,
    )
from .intvalidator import IntValidator
from .doublevalidator import DoubleValidator
from .brush import Brush
from .textblockuserdata import TextBlockUserData
from .color import Color
from .font import Font
from .fontmetrics import FontMetrics
from .fontdatabase import FontDatabase
from .region import Region
from .paintdevice import PaintDevice
from .pagedpaintdevice import PagedPaintDevice
from .image import Image
from .pen import Pen
from .picture import Picture
from .pixmap import Pixmap
from .painter import Painter
from .painterpath import PainterPath
from .palette import Palette
from .cursor import Cursor
from .polygon import Polygon
from .polygonf import PolygonF
from .standarditem import StandardItem
from .standarditemmodel import StandardItemModel
from .textcharformat import TextCharFormat
from .textcursor import TextCursor
from .syntaxhighlighter import SyntaxHighlighter
from .pdfwriter import PdfWriter
from .desktopservices import DesktopServices


__all__ = [
    "KeyEvent",
    "MouseEvent",
    "WheelEvent",
    "ActionEvent",
    "ShowEvent",
    "ContextMenuEvent",
    "Gradient",
    "GuiApplication",
    "Validator",
    "RegExpValidator",
    "RegularExpressionValidator",
    "IntValidator",
    "DoubleValidator",
    "Brush",
    "TextBlockUserData",
    "Color",
    "Font",
    "FontMetrics",
    "FontDatabase",
    "Region",
    "PaintDevice",
    "PagedPaintDevice",
    "Icon",
    "Image",
    "Pen",
    "Picture",
    "Pixmap",
    "Painter",
    "PainterPath",
    "Palette",
    "Cursor",
    "Polygon",
    "PolygonF",
    "StandardItem",
    "StandardItemModel",
    "TextCharFormat",
    "TextCursor",
    "SyntaxHighlighter",
    "PdfWriter",
    "KeySequence",
    "DesktopServices",
]
