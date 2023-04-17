"""Gui module.

Contains QtGui-based classes
"""
from __future__ import annotations
import sys

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


from .stylehints import StyleHints
from .textobjectinterface import TextObjectInterface
from .drag import Drag
from .screen import Screen
from .keysequence import KeySequence
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
from .painter import Painter, PainterMixin
from .painterpath import PainterPath
from .painterpathstroker import PainterPathStroker
from .palette import Palette
from .guiapplication import GuiApplication, GuiApplicationMixin
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
from .textformat import TextFormat, TextFormatMixin
from .textlength import TextLength
from .textframeformat import TextFrameFormat
from .textcharformat import TextCharFormat, TextCharFormatMixin
from .textimageformat import TextImageFormat
from .textlistformat import TextListFormat
from .texttablecellformat import TextTableCellFormat
from .textobject import TextObject, TextObjectMixin
from .textblockgroup import TextBlockGroup
from .textframe import TextFrame
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


def app(args: list[str] | None = None) -> GuiApplication:
    if (instance := GuiApplication.instance()) is not None:
        return instance
    return GuiApplication(sys.argv if args is None else args)


__all__ = [
    "app",
    "StyleHints",
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
    "GradientMixin",
    "LinearGradient",
    "RadialGradient",
    "ConicalGradient",
    "PageSize",
    "PageLayout",
    "Clipboard",
    "GuiApplication",
    "GuiApplicationMixin",
    "Validator",
    "ValidatorMixin",
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
    "PaintDeviceMixin",
    "Transform",
    "PagedPaintDevice",
    "PagedPaintDeviceMixin",
    "Icon",
    "Image",
    "Pen",
    "Picture",
    "Pixmap",
    "PixmapMixin",
    "IconEngine",
    "PixmapCache",
    "Bitmap",
    "Painter",
    "PainterMixin",
    "PainterPath",
    "PainterPathStroker",
    "Palette",
    "Cursor",
    "Polygon",
    "PolygonF",
    "StandardItem",
    "StandardItemModel",
    "TextCharFormat",
    "TextCharFormatMixin",
    "TextImageFormat",
    "TextListFormat",
    "TextTableCellFormat",
    "TextCursor",
    "SyntaxHighlighter",
    "UndoCommand",
    "UndoStack",
    "UndoGroup",
    "PdfWriter",
    "KeySequence",
    "Surface",
    "SurfaceMixin",
    "Window",
    "WindowMixin",
    "DesktopServices",
    "Matrix4x4",
    "Vector3D",
    "Vector4D",
    "PaintDeviceWindow",
    "PaintDeviceWindowMixin",
    "RasterWindow",
    "ImageIOHandler",
    "ImageReader",
    "ImageWriter",
    "TextObject",
    "TextObjectMixin",
    "TextLength",
    "TextFormat",
    "TextFormatMixin",
    "TextFrameFormat",
    "TextFrame",
    "AbstractFileIconProvider",
    "AbstractFileIconProviderMixin",
    "AbstractTextDocumentLayout",
    "AbstractTextDocumentLayoutMixin",
    "InputMethod",
    "ColorSpace",
]
