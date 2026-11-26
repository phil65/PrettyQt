"""Provides a widget class for displaying a Qt Quick user interface."""

from prettyqt.qt.QtQuickWidgets import *  # noqa: F403

from .quickwidget import QuickWidget
from prettyqt.qt import QtQuickWidgets

QT_MODULE = QtQuickWidgets

__all__ = [
    "QuickWidget",
]
