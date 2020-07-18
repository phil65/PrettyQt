# -*- coding: utf-8 -*-

"""gui module

contains QtGui-based classes
"""

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
from .palette import Palette
from .cursor import Cursor
from .polygonf import PolygonF
from .standarditem import StandardItem
from .standarditemmodel import StandardItemModel
from .textcharformat import TextCharFormat
from .textcursor import TextCursor
from .syntaxhighlighter import SyntaxHighlighter
from .pdfwriter import PdfWriter
from .keysequence import KeySequence


__all__ = [
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
    "Palette",
    "Cursor",
    "PolygonF",
    "StandardItem",
    "StandardItemModel",
    "TextCharFormat",
    "TextCursor",
    "SyntaxHighlighter",
    "PdfWriter",
    "KeySequence",
]
