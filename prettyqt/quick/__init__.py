"""A declarative framework for building dynamic apps with custom user interfaces."""

from __future__ import annotations

from prettyqt.qt.QtQuick import *  # noqa: F403

from .quicktextdocument import QuickTextDocument
from .quickrendercontrol import QuickRenderControl
from .quickimageresponse import QuickImageResponse
from .quickimageprovider import QuickImageProvider, QuickImageProviderMixin
from .quickasyncimageprovider import QuickAsyncImageProvider
from .quickitemgrabresult import QuickItemGrabResult
from .quickitem import QuickItem, QuickItemMixin
from .quickpainteditem import QuickPaintedItem
from .quickwindow import QuickWindow
from .quickview import QuickView
from .sgnode import SGNode
from prettyqt.qt import QtQuick

QT_MODULE = QtQuick

__all__ = [
    "SGNode",
    "QuickView",
    "QuickItem",
    "QuickItemMixin",
    "QuickWindow",
    "QuickPaintedItem",
    "QuickTextDocument",
    "QuickRenderControl",
    "QuickImageResponse",
    "QuickImageProvider",
    "QuickImageProviderMixin",
    "QuickAsyncImageProvider",
    "QuickItemGrabResult",
]
