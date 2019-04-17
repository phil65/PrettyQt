#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import widgets

app = widgets.Application.create_default_app()


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return widgets.Callout()


def test_textbrowser():
    reader = widgets.TextBrowser()
    reader.show()
    reader.close()
    assert True


def test_action():
    action = widgets.Action()
    action.set_tooltip("test")
    return True


def test_application():
    return True


def test_boxlayout():
    layout = widgets.BoxLayout("horizontal")
    layout.addWidget(widgets.Widget())
    return True


def test_buttongroup():
    group = widgets.ButtonGroup()
    return True


def test_checkbox():
    chk = widgets.CheckBox()
    chk.show()
    chk.close()


def test_colordialog():
    dlg = widgets.ColorDialog()
    dlg.show()
    dlg.close()


def test_combobox():
    box = widgets.ComboBox()
    box.show()
    box.close()


def test_desktopwidget():
    box = widgets.DesktopWidget()
    return True


def test_dialog():
    dlg = widgets.Dialog()
    dlg.show()
    dlg.close()


def test_dialogbuttonbox():
    box = widgets.DialogButtonBox()
    box.show()
    box.close()


def test_dockwidget():
    widget = widgets.DockWidget()
    widget.show()
    widget.close()


def test_doublespinbox():
    widget = widgets.DoubleSpinBox()
    widget.show()
    widget.close()


def test_filedialog():
    dlg = widgets.FileDialog()
    dlg.show()
    dlg.close()


def test_fontdialog():
    dlg = widgets.FontDialog()
    dlg.show()
    dlg.close()


def test_formlayout():
    widget = widgets.FormLayout()
    widget.set_size_mode("maximum")
    return True


def test_frame():
    widget = widgets.Frame()
    widget.show()
    widget.close()


def test_groupbox():
    widget = widgets.GroupBox()
    widget.show()
    widget.close()


def test_headerview():
    widget = widgets.HeaderView(parent=None)
    widget.show()
    widget.close()


def test_label():
    widget = widgets.Label()
    widget.show()
    widget.close()


def test_lineedit():
    widget = widgets.LineEdit("Test")
    widget.set_regex_validator("[0-9]")
    widget.show()
    widget.close()


def test_listview():
    widget = widgets.ListView()
    widget.show()
    widget.close()


def test_mainwindow():
    widget = widgets.MainWindow()
    widget.show()
    widget.close()


def test_menu():
    menu = widgets.Menu("1")
    action = widgets.Action("test")
    menu.addAction(action)
    menu.show()


def test_menubar():
    menu = widgets.MenuBar()
    menu.show()


def test_messagebox():
    widget = widgets.MessageBox()
    widget.show()


def test_plaintextedit():
    widget = widgets.PlainTextEdit()
    widget.set_text("hallo")
    widget.show()


def test_progressbar():
    widget = widgets.ProgressBar()
    widget.show()


def test_progressdialog():
    widget = widgets.ProgressDialog()
    widget.show()


def test_pushbutton():
    widget = widgets.PushButton("Test")
    widget.show()


def test_radiobutton():
    widget = widgets.RadioButton("Test")
    widget.show()


def test_slider():
    widget = widgets.Slider()
    widget.show()


def test_spinbox():
    widget = widgets.SpinBox()
    widget.show()


def test_splitter():
    widget = widgets.Splitter("vertical")
    widget.show()
