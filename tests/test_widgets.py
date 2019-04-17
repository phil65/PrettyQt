#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from qtpy import QtGui
from prettyqt import widgets, core

app = widgets.Application.create_default_app()


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return widgets.Callout()


def test_action():
    action = widgets.Action()
    action.set_tooltip("test")
    return True


def test_application():
    app.set_icon("mdi.timer")
    app.set_metadata(app_name="test",
                     app_version="1.0.0",
                     org_name="test",
                     org_domain="test")
    app.get_mainwindow()
    return True


def test_boxlayout():
    layout = widgets.BoxLayout("horizontal")
    widget = widgets.Widget()
    layout.addWidget(widget)
    layout.set_size_mode("maximum")
    assert(len(layout) == 1)
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
    dlg = widgets.Dialog(layout="horizontal")
    dlg.set_modality()
    dlg.delete_on_close()
    dlg.add_widget(widgets.Widget())
    dlg.set_icon("mdi.timer")
    dlg.add_buttonbox()
    dlg.show()
    dlg.close()


def test_dialogbuttonbox():
    box = widgets.DialogButtonBox()
    box.set_horizontal()
    box.set_vertical()
    box.add_buttons(["apply"])
    box.show()
    box.close()


def test_dockwidget():
    widget = widgets.DockWidget()
    widget.setup_title_bar()
    widget.maximise()
    widget.show()
    widget.close()


def test_doublespinbox():
    widget = widgets.DoubleSpinBox()
    widget.show()
    widget.close()


def test_filedialog():
    dlg = widgets.FileDialog()
    dlg.set_label_text("accept", "test")
    dlg.set_accept_mode("open")
    dlg.set_accept_mode("save")
    dlg.set_filter(dict(a=[".csv"]))
    dlg.show()
    dlg.close()


def test_fontdialog():
    dlg = widgets.FontDialog()
    dlg.show()
    dlg.close()


def test_formlayout():
    widget = widgets.FormLayout()
    widget.set_size_mode("maximum")
    widget.set_label_widget(0, "test")
    widget.set_label_widget(0, widgets.Widget())
    widget.set_field_widget(0, "test")
    widget.set_field_widget(0, widgets.Widget())
    widget.set_spanning_widget(0, "test")
    widget.set_spanning_widget(0, widgets.Widget())
    widget = widgets.FormLayout.from_dict({"2": "4"})
    assert(len(widget) == 2)
    return True


def test_frame():
    widget = widgets.Frame()
    widget.show()
    widget.close()


def test_gridlayout():
    layout = widgets.GridLayout()
    widget = widgets.Widget()
    layout[0:1, 0:3] = widget
    layout.set_size_mode("maximum")
    layout.set_alignment("left")
    assert len(layout) == len(list(layout)) == 1


def test_groupbox():
    widget = widgets.GroupBox()
    widget.show()
    widget.close()


def test_headerview():
    widget = widgets.HeaderView(parent=None)
    widget.show()
    widget.close()


def test_label():
    label = widgets.Label()
    label.set_image("")
    label.set_alignment(horizontal="left", vertical="top")
    label.show()
    label.close()


def test_lineedit():
    widget = widgets.LineEdit("Test")
    widget.set_regex_validator("[0-9]")
    widget.set_font("Consolas")
    widget.setText("0")
    widget.append("a")
    widget.show()
    widget.close()


def test_listview():
    widget = widgets.ListView()
    widget.show()
    widget.close()


def test_mainwindow():
    window = widgets.MainWindow()
    window.set_icon("mdi.timer")
    window.add_dockwidget("test", "Test")
    window.toggle_fullscreen()
    window.show()
    window.close()


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


def test_tabwidget():
    widget = widgets.TabWidget()
    widget.add_tab(widgets.Widget(), "mdi.timer")
    widget.insert_tab(0, widgets.Widget(), "test", "mdi.timer")
    widget.detach_tab(0, core.Point())
    widget.remove_tab(0)
    widget.show()
    widget.close()
    assert True


def test_textbrowser():
    reader = widgets.TextBrowser()
    reader.show()
    reader.close()
    assert True


def test_textedit():
    widget = widgets.TextEdit()
    widget.set_text("test")
    widget.append(" this")
    assert(widget.text() == "test\n this")
    widget.set_font("Consolas")
    widget.set_enabled()
    widget.set_read_only()
    widget.scroll_to_end()
    widget.set_disabled()
    widget.show()


def test_toolbar():
    widget = widgets.Toolbar()
    widget.show()


def test_treeview():
    widget = widgets.TreeView()
    widget.show()


def test_widget():
    widget = widgets.Widget()
    with widget.block_signals():
        pass
    widget.set_enabled()
    widget.set_disabled()
