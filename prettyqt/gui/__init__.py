"""Base classes for graphical user interface (GUI) components."""

from __future__ import annotations

import sys

from prettyqt.qt.QtGui import *  # noqa: F403

from .backingstore import BackingStore
from .stylehints import StyleHints
from .pageranges import PageRanges
from .shortcut import Shortcut
from .textobjectinterface import TextObjectInterface
from .drag import Drag
from .screen import Screen
from .keysequence import KeySequence
from .surfaceformat import SurfaceFormat
from .surface import Surface, SurfaceMixin
from .window import Window, WindowMixin
from .icon import Icon
from .paintdevice import PaintDevice, PaintDeviceMixin
from .paintdevicewindow import PaintDeviceWindow, PaintDeviceWindowMixin
from .pixmap import Pixmap, PixmapMixin
from .iconengine import IconEngine
from .pixmapcache import PixmapCache
from .bitmap import Bitmap
from .image import Image

from .rasterwindow import RasterWindow
from .clipboard import Clipboard
from .inputmethod import InputMethod
from .sessionmanager import SessionManager
from .validator import Validator, ValidatorMixin

from .regularexpressionvalidator import RegularExpressionValidator
from .textlayout import TextLayout
from .textline import TextLine
from .textoption import TextOption
from .textblock import TextBlock
from .textdocumentwriter import TextDocumentWriter
from .textdocument import TextDocument
from .textdocumentfragment import TextDocumentFragment
from .statictext import StaticText
from .intvalidator import IntValidator
from .doublevalidator import DoubleValidator
from .color import Color
from .brush import Brush
from .textblockuserdata import TextBlockUserData
from .gradient import Gradient, GradientMixin
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
from .pagedpaintdevice import PagedPaintDevice, PagedPaintDeviceMixin
from .pen import Pen
from .picture import Picture
from .polygon import Polygon
from .polygonf import PolygonF
from .painter import Painter, PainterMixin
from .painterpath import PainterPath
from .painterpathstroker import PainterPathStroker
from .palette import Palette
from .guiapplication import GuiApplication, GuiApplicationMixin
from .cursor import Cursor
from .standarditem import StandardItem
from .standarditemmodel import StandardItemModel
from .textcursor import TextCursor
from .pdfwriter import PdfWriter
from .desktopservices import DesktopServices
from .matrix4x4 import Matrix4x4
from .vector3d import Vector3D
from .vector4d import Vector4D
from .imageiohandler import ImageIOHandler
from .imagereader import ImageReader
from .imagewriter import ImageWriter
from .textformat import TextFormat, TextFormatMixin
from .textlength import TextLength
from .textframeformat import TextFrameFormat
from .textblockformat import TextBlockFormat
from .textcharformat import TextCharFormat, TextCharFormatMixin
from .textimageformat import TextImageFormat
from .textlistformat import TextListFormat
from .texttablecellformat import TextTableCellFormat
from .textobject import TextObject, TextObjectMixin
from .textblockgroup import TextBlockGroup
from .textframe import TextFrame
from .texttablecell import TextTableCell
from .texttableformat import TextTableFormat
from .texttable import TextTable
from .abstracttextdocumentlayout import (
    AbstractTextDocumentLayout,
    AbstractTextDocumentLayoutMixin,
)
from .abstractfileiconprovider import (
    AbstractFileIconProvider,
    AbstractFileIconProviderMixin,
)
from .syntaxhighlighter import SyntaxHighlighter
from .undocommand import UndoCommand
from .undostack import UndoStack
from .undogroup import UndoGroup
from .colorspace import ColorSpace
from .action import Action, ActionMixin
from .actiongroup import ActionGroup
from prettyqt.qt import QtGui

QT_MODULE = QtGui
# might_be_rich_text = Qt.mightBeRichText


def app(args: list[str] | None = None, **kwargs) -> GuiApplication:
    if (instance := GuiApplication.instance()) is not None:
        return instance
    return GuiApplication(sys.argv if args is None else args, **kwargs)


__all__ = [
    "AbstractFileIconProvider",
    "AbstractFileIconProviderMixin",
    "AbstractTextDocumentLayout",
    "AbstractTextDocumentLayoutMixin",
    "Action",
    "ActionGroup",
    "ActionMixin",
    "BackingStore",
    "Bitmap",
    "Brush",
    "Clipboard",
    "Color",
    "ColorSpace",
    "ConicalGradient",
    "Cursor",
    "DesktopServices",
    "DoubleValidator",
    "Drag",
    "Font",
    "FontDatabase",
    "FontInfo",
    "FontMetrics",
    "FontMetricsF",
    "Gradient",
    "GradientMixin",
    "GuiApplication",
    "GuiApplicationMixin",
    "Icon",
    "IconEngine",
    "Image",
    "ImageIOHandler",
    "ImageReader",
    "ImageWriter",
    "InputMethod",
    "IntValidator",
    "KeySequence",
    "LinearGradient",
    "Matrix4x4",
    "Movie",
    "PageLayout",
    "PageRanges",
    "PageSize",
    "PagedPaintDevice",
    "PagedPaintDeviceMixin",
    "PaintDevice",
    "PaintDeviceMixin",
    "PaintDeviceWindow",
    "PaintDeviceWindowMixin",
    "Painter",
    "PainterMixin",
    "PainterPath",
    "PainterPathStroker",
    "Palette",
    "PdfWriter",
    "Pen",
    "Picture",
    "Pixmap",
    "PixmapCache",
    "PixmapMixin",
    "Polygon",
    "PolygonF",
    "RadialGradient",
    "RasterWindow",
    "Region",
    "RegularExpressionValidator",
    "Screen",
    "SessionManager",
    "Shortcut",
    "StandardItem",
    "StandardItemModel",
    "StaticText",
    "StyleHints",
    "Surface",
    "SurfaceFormat",
    "SurfaceMixin",
    "SyntaxHighlighter",
    "TextBlock",
    "TextBlockFormat",
    "TextBlockGroup",
    "TextBlockUserData",
    "TextCharFormat",
    "TextCharFormatMixin",
    "TextCursor",
    "TextDocument",
    "TextDocumentFragment",
    "TextDocumentWriter",
    "TextFormat",
    "TextFormatMixin",
    "TextFrame",
    "TextFrameFormat",
    "TextImageFormat",
    "TextLayout",
    "TextLength",
    "TextLine",
    "TextListFormat",
    "TextObject",
    "TextObjectInterface",
    "TextObjectMixin",
    "TextOption",
    "TextTable",
    "TextTableCell",
    "TextTableCellFormat",
    "TextTableFormat",
    "Transform",
    "UndoCommand",
    "UndoGroup",
    "UndoStack",
    "Validator",
    "ValidatorMixin",
    "Vector3D",
    "Vector4D",
    "Window",
    "WindowMixin",
    "app",
]
