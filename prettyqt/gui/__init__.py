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
from qtpy.QtGui import QResizeEvent as ResizeEvent
from qtpy.QtGui import QNativeGestureEvent as NativeGestureEvent
from qtpy.QtGui import QMoveEvent as MoveEvent
from qtpy.QtGui import QInputMethodEvent as InputMethodEvent
from qtpy.QtGui import QInputMethodQueryEvent as InputMethodQueryEvent
from qtpy.QtGui import QCloseEvent as CloseEvent
from qtpy.QtGui import QDragLeaveEvent as DragLeaveEvent
from qtpy.QtGui import QHelpEvent as HelpEvent
from qtpy.QtGui import QHideEvent as HideEvent
from qtpy.QtGui import QHoverEvent as HoverEvent
from qtpy.QtGui import QDragMoveEvent as DragMoveEvent
from qtpy.QtGui import QEnterEvent as EnterEvent
from qtpy.QtGui import QExposeEvent as ExposeEvent
from qtpy.QtGui import QFileOpenEvent as FileOpenEvent
from qtpy.QtGui import QIconDragEvent as IconDragEvent
from qtpy.QtGui import QInputEvent as InputEvent
from qtpy.QtGui import QPaintEvent as PaintEvent
from qtpy.QtGui import QShortcutEvent as ShortcutEvent
from qtpy.QtGui import QStatusTipEvent as StatusTipEvent
from qtpy.QtGui import QTouchEvent as TouchEvent
from qtpy.QtGui import QTabletEvent as TabletEvent
from qtpy.QtGui import QWindowStateChangeEvent as WindowStateChangeEvent
from qtpy.QtGui import QWhatsThisClickedEvent as WhatsThisClickedEvent
from qtpy.QtGui import QScrollEvent as ScrollEvent
from qtpy.QtGui import QScrollPrepareEvent as ScrollPrepareEvent

# not available in PySide2
# from qtpy.QtGui import QPlatformSurfaceEvent as PlatformSurfaceEvent

from .screen import Screen
from .keysequence import KeySequence
from .surface import Surface
from .window import Window
from .icon import Icon
from .paintdevice import PaintDevice
from .paintdevicewindow import PaintDeviceWindow
from .pixmap import Pixmap
from .pixmapcache import PixmapCache
from .bitmap import Bitmap
from .image import Image
from .openglwindow import OpenGLWindow
from .rasterwindow import RasterWindow
from .clipboard import Clipboard
from .inputmethod import InputMethod
from .sessionmanager import SessionManager
from .validator import Validator
from .regexpvalidator import RegExpValidator
from .regularexpressionvalidator import RegularExpressionValidator
from .textoption import TextOption
from .textblock import TextBlock
from .textdocument import TextDocument
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

from prettyqt import core

if core.VersionNumber.get_qt_version() >= (5, 13, 0):
    from .colorspace import ColorSpace


def app():
    if GuiApplication.instance() is not None:
        return GuiApplication.instance()
    return GuiApplication([])


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
    "RegExpValidator",
    "TextOption",
    "TextBlock",
    "TextBlockGroup",
    "TextDocument",
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
    "OpenGLWindow",
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
