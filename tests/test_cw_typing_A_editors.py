# ruff: noqa: N999
"""Regression tests for bugs found while typing custom_widgets editors."""

import enum

from prettyqt import constants, core, custom_widgets, gui, widgets


def test_brushedit_accepts_qbrush(qtbot):
    brush = gui.QBrush(gui.QColor("red"), constants.BrushStyle.DiagCrossPattern)
    widget = custom_widgets.BrushEdit(color=brush)
    qtbot.addWidget(widget)
    assert widget.get_value().color() == gui.QColor("red")
    assert widget.get_value().style() == constants.BrushStyle.DiagCrossPattern

    other = gui.QBrush(gui.QColor("blue"), constants.BrushStyle.Dense4Pattern)
    widget.set_value(other)
    assert widget.get_value().color() == gui.QColor("blue")
    assert widget.get_value().style() == constants.BrushStyle.Dense4Pattern


def test_cursoredit_get_value_when_cleared(qtbot):
    widget = custom_widgets.CursorEdit()
    qtbot.addWidget(widget)
    widget.clear()
    cursor = widget.get_value()
    assert isinstance(cursor, gui.Cursor)


def test_enumcombobox_set_enum_class_none(qtbot):
    class Color(enum.Enum):
        RED = 1
        BLUE = 2

    widget = custom_widgets.EnumComboBox(Color.RED)
    qtbot.addWidget(widget)
    widget._set_enum_class(None)
    assert widget.get_enum_class() is None
    assert widget.get_value() is None
    assert widget.count() == 0


def test_enumflagwidget_set_enum_class_none(qtbot):
    class Perm(enum.Flag):
        NONE = 0
        READ = 1
        WRITE = 2

    widget = custom_widgets.EnumFlagWidget()
    qtbot.addWidget(widget)
    widget.set_value(Perm.READ)
    widget._set_enum_class(None)
    assert widget.get_enum_class() is None
    assert widget.get_value() is None


def test_enumflagwidget_on_menu_click_without_enum(qtbot):
    widget = custom_widgets.EnumFlagWidget()
    qtbot.addWidget(widget)
    widget._on_menu_click()
    assert widget.get_value() is None


def test_filechooserbutton_extensions_dict(qtbot):
    widget = custom_widgets.FileChooserButton()
    qtbot.addWidget(widget)
    assert widget.get_extensions() == {}
    exts = {"Text files": [".txt"]}
    widget.set_extensions(exts)
    assert widget.get_extensions() == exts
    dlg = widgets.FileDialog()
    qtbot.addWidget(dlg)
    dlg.set_extension_filter(widget.get_extensions())


def test_keycombinationedit_set_and_get_value(qtbot):
    widget = custom_widgets.KeyCombinationEdit()
    qtbot.addWidget(widget)
    widget.set_value("Ctrl+A")
    assert widget.get_value() == "Ctrl+A"
    widget.set_value(gui.QKeySequence("Ctrl+B"))
    assert widget.get_value() == "Ctrl+B"
    widget.set_value("")
    assert widget.get_value() == ""


def test_pointedit_set_value_tuple(qtbot):
    widget = custom_widgets.PointEdit()
    qtbot.addWidget(widget)
    widget.set_value((10, 20))
    assert widget.get_value() == core.Point(10, 20)


def test_rectfedit_float_width_height(qtbot):
    widget = custom_widgets.RectFEdit()
    qtbot.addWidget(widget)
    rect = core.QRectF(1.5, 2.5, 3.5, 4.5)
    widget.set_value(rect)
    assert widget.get_value() == rect


def test_sizeedit_set_value_int(qtbot):
    widget = custom_widgets.SizeEdit()
    qtbot.addWidget(widget)
    widget.set_value(10)
    assert widget.get_value() == core.Size(10, 10)
