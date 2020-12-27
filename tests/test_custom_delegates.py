"""Tests for `prettyqt` package."""

from prettyqt import custom_delegates, widgets
from prettyqt.qt import QtCore


def test_buttondelegate(qtbot):
    widget = custom_delegates.ButtonDelegate(parent=None)
    widget.setEditorData(widgets.Widget(), None)
    widget.createEditor(None, None, QtCore.QModelIndex())
    widget.currentIndexChanged()


def test_radiodelegate(qtbot, tablewidget):
    delegate = custom_delegates.RadioDelegate(tablewidget, ["a", "b"])
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.openPersistentEditor(tablewidget[0, 0])
    tablewidget.hide()


def test_icondelegate(qtbot, tablewidget):
    delegate = custom_delegates.IconDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_nofocusdelegate(qtbot, tablewidget):
    delegate = custom_delegates.NoFocusDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_stardelegate(qtbot, tablewidget):
    delegate = custom_delegates.StarDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_progressbardelegate(qtbot, tablewidget):
    delegate = custom_delegates.ProgressBarDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()
