# -*- coding: utf-8 -*-

"""Gui module.

Contains QtGui-based classes
"""

from qtpy.QtGui import QKeyEvent as KeyEvent
from qtpy.QtGui import QMouseEvent as MouseEvent
from qtpy.QtGui import QWheelEvent as WheelEvent
from qtpy.QtGui import QActionEvent as ActionEvent
from qtpy.QtGui import QShowEvent as ShowEvent
from qtpy.QtGui import QDropEvent as DropEvent
from qtpy.QtGui import QFocusEvent as FocusEvent
from qtpy.QtGui import QDragEnterEvent as DragEnterEvent
from qtpy.QtGui import QContextMenuEvent as ContextMenuEvent

from .keysequence import KeySequence
from .surface import Surface
from .window import Window
from .icon import Icon
from .paintdevice import PaintDevice
from .paintdevicewindow import PaintDeviceWindow
from .pixmap import Pixmap
from .image import Image
from .openglwindow import OpenGLWindow
from .rasterwindow import RasterWindow
from .clipboard import Clipboard
from .guiapplication import GuiApplication
from .validator import Validator
from .regexpvalidator import RegExpValidator

try:
    from .regularexpressionvalidator import RegularExpressionValidator
except AttributeError:
    from .regularexpressionvalidator_pyside import (  # type: ignore
        RegularExpressionValidator,
    )
from .textoption import TextOption
from .textblock import TextBlock
from .textdocument import TextDocument
from .intvalidator import IntValidator
from .doublevalidator import DoubleValidator
from .brush import Brush
from .textblockuserdata import TextBlockUserData
from .color import Color
from .gradient import Gradient
from .lineargradient import LinearGradient
from .radialgradient import RadialGradient
from .conicalgradient import ConicalGradient
from .pagesize import PageSize
from .pagelayout import PageLayout
from .font import Font
from .fontmetrics import FontMetrics
from .fontmetricsf import FontMetricsF
from .fontinfo import FontInfo
from .fontdatabase import FontDatabase
from .region import Region
from .movie import Movie
from .transform import Transform
from .pagedpaintdevice import PagedPaintDevice
from .pen import Pen
from .picture import Picture
from .painter import Painter
from .painterpath import PainterPath
from .painterpathstroker import PainterPathStroker
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
from .matrix4x4 import Matrix4x4
from .vector4d import Vector4D
from .imageiohandler import ImageIOHandler
from .imagereader import ImageReader
from .imagewriter import ImageWriter

__all__ = [
    "KeyEvent",
    "MouseEvent",
    "WheelEvent",
    "ActionEvent",
    "ShowEvent",
    "ContextMenuEvent",
    "DropEvent",
    "DragEnterEvent",
    "FocusEvent",
    "Gradient",
    "LinearGradient",
    "RadialGradient",
    "ConicalGradient",
    "PageSize",
    "PageLayout",
    "Clipboard",
    "GuiApplication",
    "Validator",
    "RegExpValidator",
    "TextOption",
    "TextBlock",
    "TextDocument",
    "RegularExpressionValidator",
    "IntValidator",
    "DoubleValidator",
    "Brush",
    "TextBlockUserData",
    "Color",
    "Font",
    "FontMetrics",
    "FontMetricsF",
    "FontInfo",
    "FontDatabase",
    "Region",
    "Movie",
    "PaintDevice",
    "Transform",
    "PagedPaintDevice",
    "Icon",
    "Image",
    "Pen",
    "Picture",
    "Pixmap",
    "Painter",
    "PainterPath",
    "PainterPathStroker",
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
    "Surface",
    "Window",
    "DesktopServices",
    "Matrix4x4",
    "Vector4D",
    "PaintDeviceWindow",
    "OpenGLWindow",
    "RasterWindow",
    "ImageIOHandler",
    "ImageReader",
    "ImageWriter",
]
