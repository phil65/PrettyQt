"""Tests for `prettyqt` package."""

from prettyqt import itemdelegates, widgets
from prettyqt.qt import QtCore


def test_buttondelegate(qtbot):
    table = widgets.TableView()
    widget = itemdelegates.ButtonDelegate(parent=table)
    widget.setEditorData(widgets.Widget(), None)
    widget.createEditor(None, None, QtCore.QModelIndex())
    # widget.currentIndexChanged()


def test_radiodelegate(qtbot, tablewidget):
    delegate = itemdelegates.RadioDelegate(tablewidget, ["a", "b"])
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.openPersistentEditor(tablewidget[0, 0])
    tablewidget.hide()


def test_icondelegate(qtbot, tablewidget):
    delegate = itemdelegates.IconDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_nofocusdelegate(qtbot, tablewidget):
    delegate = itemdelegates.NoFocusDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_stardelegate(qtbot, tablewidget):
    delegate = itemdelegates.StarDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_progressbardelegate(qtbot, tablewidget):
    delegate = itemdelegates.ProgressBarDelegate()
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_editordelegate(qtbot, tablewidget):
    delegate = itemdelegates.EditorDelegate(parent=tablewidget)
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()


def test_widgetdelegate(qtbot, tablewidget):
    delegate = itemdelegates.EditorDelegate(parent=tablewidget)
    tablewidget.show()
    tablewidget.setItemDelegateForColumn(0, delegate)
    tablewidget.hide()
