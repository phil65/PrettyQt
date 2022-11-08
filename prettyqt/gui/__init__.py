"""Gui module.

Contains QtGui-based classes
"""
from __future__ import annotations

from prettyqt.qt.QtGui import (
    QKeyEvent as KeyEvent,
    QMouseEvent as MouseEvent,
    QWheelEvent as WheelEvent,
    QActionEvent as ActionEvent,
    QShowEvent as ShowEvent,
    QDropEvent as DropEvent,
    QFocusEvent as FocusEvent,
    QDragEnterEvent as DragEnterEvent,
    QContextMenuEvent as ContextMenuEvent,
    QResizeEvent as ResizeEvent,
    QNativeGestureEvent as NativeGestureEvent,
    QMoveEvent as MoveEvent,
    QInputMethodEvent as InputMethodEvent,
    QInputMethodQueryEvent as InputMethodQueryEvent,
    QCloseEvent as CloseEvent,
    QDragLeaveEvent as DragLeaveEvent,
    QHelpEvent as HelpEvent,
    QHideEvent as HideEvent,
    QHoverEvent as HoverEvent,
    QDragMoveEvent as DragMoveEvent,
    QEnterEvent as EnterEvent,
    QExposeEvent as ExposeEvent,
    QFileOpenEvent as FileOpenEvent,
    QIconDragEvent as IconDragEvent,
    QInputEvent as InputEvent,
    QPaintEvent as PaintEvent,
    QShortcutEvent as ShortcutEvent,
    QStatusTipEvent as StatusTipEvent,
    QTouchEvent as TouchEvent,
    QTabletEvent as TabletEvent,
    QWindowStateChangeEvent as WindowStateChangeEvent,
    QWhatsThisClickedEvent as WhatsThisClickedEvent,
    QScrollEvent as ScrollEvent,
    QScrollPrepareEvent as ScrollPrepareEvent,
)

# not available in PySide2
# from prettyqt.qt.QtGui import QPlatformSurfaceEvent as PlatformSurfaceEvent

from .textobjectinterface import TextObjectInterface
from .drag import Drag
from .screen import Screen
from .keysequence import KeySequence
from .surface import Surface
from .window import Window
from .icon import Icon
from .paintdevice import PaintDevice
from .paintdevicewindow import PaintDeviceWindow
from .pixmap import Pixmap
from .iconengine import IconEngine
from .pixmapcache import PixmapCache
from .bitmap import Bitmap
from .image import Image

from .rasterwindow import RasterWindow
from .clipboard import Clipboard
from .inputmethod import InputMethod
from .sessionmanager import SessionManager
from .validator import Validator

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
from .guiapplication import GuiApplication
from .cursor import Cursor
from .polygon import Polygon
from .polygonf import PolygonF
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
from .textformat import TextFormat
from .textlength import TextLength
from .textframeformat import TextFrameFormat
from .textcharformat import TextCharFormat
from .textimageformat import TextImageFormat
from .textlistformat import TextListFormat
from .texttablecellformat import TextTableCellFormat
from .textobject import TextObject
from .textblockgroup import TextBlockGroup
from .textframe import TextFrame
from .abstracttextdocumentlayout import AbstractTextDocumentLayout
from .syntaxhighlighter import SyntaxHighlighter

from .colorspace import ColorSpace


def app(args: list[str] | None = None) -> GuiApplication:
    instance = GuiApplication.instance()
    if instance is not None:
        return instance
    return GuiApplication([] if args is None else args)


__all__ = [
    "app",
    "KeyEvent",
    "MouseEvent",
    "WheelEvent",
    "ActionEvent",
    "ShowEvent",
    "ContextMenuEvent",
    "ResizeEvent",
    "NativeGestureEvent",
    "InputMethodQueryEvent",
    "InputMethodEvent",
    "TextObjectInterface",
    "SessionManager",
    "CloseEvent",
    "DragLeaveEvent",
    "MoveEvent",
    "HelpEvent",
    "HideEvent",
    "HoverEvent",
    "DragMoveEvent",
    "TouchEvent",
    "TabletEvent",
    "WindowStateChangeEvent",
    "FileOpenEvent",
    "IconDragEvent",
    "InputEvent",
    "PaintEvent",
    "ShortcutEvent",
    "StatusTipEvent",
    "EnterEvent",
    "ExposeEvent",
    "WhatsThisClickedEvent",
    "ScrollEvent",
    "ScrollPrepareEvent",
    "PlatformSurfaceEvent",
    "DropEvent",
    "DragEnterEvent",
    "FocusEvent",
    "Drag",
    "Screen",
    "Gradient",
    "LinearGradient",
    "RadialGradient",
    "ConicalGradient",
    "PageSize",
    "PageLayout",
    "Clipboard",
    "GuiApplication",
    "Validator",
    "TextLayout",
    "TextLine",
    "TextOption",
    "TextBlock",
    "TextBlockGroup",
    "TextDocumentWriter",
    "TextDocument",
    "TextDocumentFragment",
    "StaticText",
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
    "IconEngine",
    "PixmapCache",
    "Bitmap",
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
    "TextImageFormat",
    "TextListFormat",
    "TextTableCellFormat",
    "TextCursor",
    "SyntaxHighlighter",
    "PdfWriter",
    "KeySequence",
    "Surface",
    "Window",
    "DesktopServices",
    "Matrix4x4",
    "Vector3D",
    "Vector4D",
    "PaintDeviceWindow",
    "RasterWindow",
    "ImageIOHandler",
    "ImageReader",
    "ImageWriter",
    "TextObject",
    "TextLength",
    "TextFormat",
    "TextFrameFormat",
    "TextFrame",
    "AbstractTextDocumentLayout",
    "InputMethod",
    "ColorSpace",
]
