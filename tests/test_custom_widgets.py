"""Tests for `prettyqt` package."""

import logging
import pickle
import re
import pytest

import prettyqt
from prettyqt import constants, core, custom_widgets, gui, widgets
import prettyqt.custom_widgets.dataset as fo
from prettyqt.qt import QtGui


def test_booldicttoolbutton(qtbot):
    dct = dict(a="test", b="test2")
    w = custom_widgets.BoolDictToolButton(text="Title", dct=dct)
    qtbot.addWidget(w)
    w["a"] = True
    assert w["a"] is True
    assert w.as_dict() == dict(a=True, b=False)


def test_collapsibleframe(qtbot):
    frame = custom_widgets.CollapsibleFrame()
    qtbot.addWidget(frame)
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    frame.add_widget(widget)
    frame.set_title("CollapsibleFrame")
    frame.expand()
    assert frame.is_expanded() is True
    frame.collapse()
    frame.remove_widget(widget)


def test_elidedlabel(qtbot):
    label = custom_widgets.ElidedLabel()
    label.set_text("test")
    assert label.get_text() == "test"
    label.show()


# def test_expandableline(qtbot):
#     layout = widgets.VBoxLayout()
#     textbrowser = widgets.TextBrowser()
#     # qtbot.addWidget(textbrowser)
#     layout.addWidget(textbrowser)
#     widget = custom_widgets.ExpandableLine("Test")
#     qtbot.addWidget(widget)
#     widget.set_layout(layout)
#     widget.show()


def test_colorchooserbutton(qtbot):
    btn = custom_widgets.ColorChooserButton()
    qtbot.addWidget(btn)
    btn.set_current_color("green")
    assert btn.get_value() == gui.Color("green")
    btn.set_value("blue")
    assert btn.is_valid()

@pytest.mark.skipif(prettyqt.qt.API == "pyside6", reason="Segmentation fault")
def test_regexeditor(qtbot):
    widget = custom_widgets.regexeditor.RegexEditorWidget()
    qtbot.addWidget(widget)
    widget.regex = "[0-9]"
    assert widget.regex == "[0-9]"
    widget.string = "test123"
    assert widget.string == "test123"
    widget.compile_flags = re.IGNORECASE


def test_dataset(qtbot):
    class Test(fo.DataSet):
        i1 = fo.Bool(label="My first one")
        string1 = fo.String(label="My first one", regex="[0-9]")
        string2 = fo.String(label="My second one", notempty=True)
        choiceitem = fo.Enum(label="A", choices=["A", "B"], disabled_on="i1")
        mchoiceitem = fo.MultipleChoice(label="A", choices=["A", "B"])
        floatitem = fo.Float(label="FloatItem", enabled_on="i1")
        intitem = fo.Int(label="IntItem", enabled_on="i1")
        coloritem = fo.Color(label="ColorItem", value="green")
        fileitem = fo.File(label="File")
        folderitem = fo.Folder(label="File", optional="Test")
        stringornumber = fo.StringOrNumber(label="Test")
        buttonitem = fo.Button(label="Button", callback=print)
        intlist = fo.IntList(label="Button", value=[1, 2, 3])
        floatlist = fo.FloatList(label="Button", value=[1.1, 2, 3])
        code = fo.Code(label="Test", value="class Test")

    settings = Test(icon="mdi.timer")
    settings.create_dialog()
    settings.to_dict()


def test_flagselectionwidget(qtbot):
    widget = custom_widgets.FlagSelectionWidget()
    qtbot.addWidget(widget)
    items = {0: "MultiLine", 2: "Ignore case"}
    widget.add_items(items)
    assert widget.get_value() == 0


def test_hiearchicalheaderview(qtbot):
    widget = widgets.TableView()
    view = custom_widgets.HierarchicalHeaderView("horizontal", widget)
    assert view is not None


def test_iconbrowser(qtbot):
    browser = custom_widgets.IconBrowser()
    qtbot.addWidget(browser)
    browser.show()
    browser.hide()


def test_stringornumberwidget(qtbot):
    widget = custom_widgets.StringOrNumberWidget()
    qtbot.addWidget(widget)
    widget.get_value()
    widget.on_value_change()


def test_optionalwidget(qtbot):
    w = widgets.RadioButton()
    qtbot.addWidget(w)
    container = custom_widgets.OptionalWidget(w, "Test")
    qtbot.addWidget(container)
    container.get_value()
    container.enabled = False
    assert container.enabled is False


def test_sidebarwidget(qtbot):
    ex = custom_widgets.SidebarWidget(show_settings=True)
    qtbot.addWidget(ex)
    page_1 = widgets.PlainTextEdit()
    page_2 = widgets.ColorDialog()
    page_3 = widgets.FileDialog()
    qtbot.addWidget(page_1)
    qtbot.addWidget(page_2)
    qtbot.addWidget(page_3)
    ex.add_tab(page_1, "Text", "mdi.timer")
    ex.add_tab(page_2, "Color", "mdi.format-color-fill", area="bottom")
    ex.add_tab(page_3, "Help", "mdi.help-circle-outline")
    ex.set_marker(page_3)
    ex.set_tab(page_2)


def test_singlelinetextedit(qtbot):
    w = custom_widgets.SingleLineTextEdit()
    qtbot.addWidget(w)
    w.set_text("test")


def test_timeline(qtbot):
    tl = custom_widgets.Timeline(60, 60)
    qtbot.addWidget(tl)
    tl.show()
    sample = custom_widgets.VideoSample(20)
    tl += sample
    tl.add_sample(30)
    sample_3 = custom_widgets.VideoSample(20)
    tl[1] = sample_3
    assert tl[1] == sample_3
    assert len(tl) == 2
    tl.close()


def test_mappedcheckbox(qtbot):
    widget = custom_widgets.MappedCheckBox(true_value=0, false_value=1)
    qtbot.addWidget(widget)
    widget.set_value(0)
    assert widget.get_value() == 0
    widget.setChecked(False)
    assert widget.get_value() == 1


def test_filechooserbutton(qtbot):
    btn = custom_widgets.FileChooserButton()
    qtbot.addWidget(btn)
    with open("data.pkl", "wb") as jar:
        pickle.dump(btn, jar)
    with open("data.pkl", "rb") as jar:
        btn = pickle.load(jar)
    btn.set_value("/")
    btn.get_value()


def test_objectbrowser(qtbot):
    struct = dict(a={1, 2, frozenset([1, 2])})
    browser = custom_widgets.ObjectBrowser(struct)
    browser.show()
    browser.close()


def test_fontchooserbutton(qtbot):
    btn = custom_widgets.FontChooserButton()
    qtbot.addWidget(btn)
    with open("data.pkl", "wb") as jar:
        pickle.dump(btn, jar)
    with open("data.pkl", "rb") as jar:
        btn = pickle.load(jar)
    btn.set_font("Consolas")
    repr(btn)


def test_iconlabel(qtbot):
    w = custom_widgets.IconLabel()
    qtbot.addWidget(w)
    w.set_text("test")
    assert w.text() == "test"
    repr(w)


def test_inputandslider(qtbot):
    w = custom_widgets.InputAndSlider()
    qtbot.addWidget(w)
    w.set_range(0, 10)
    w.set_value(5)
    assert w.get_value() == 5
    w.set_step_size(2)
    assert w.is_valid()

# something related to syntaxhighlighting...
@pytest.mark.skipif(
    prettyqt.qt.API == "pyside6", reason="Windows fatal exception: access violation"
)
def test_codeeditor(qtbot):
    editor = custom_widgets.CodeEditor()
    qtbot.addWidget(editor)
    assert editor.text() == ""
    editor.line_area_width()
    editor.set_syntaxhighlighter("python")
    event = QtGui.QResizeEvent(core.Size(10, 10), core.Size(20, 20))
    editor.resizeEvent(event)
    editor.repaint()


def test_flowlayout(qtbot):
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    layout = custom_widgets.FlowLayout(margin=1)
    btn = widgets.PushButton("Short")
    qtbot.addWidget(btn)
    layout += btn
    layout += widgets.PushButton("Longer")
    layout += widgets.PushButton("Different text")
    layout += widgets.PushButton("More text")
    layout += widgets.PushButton("Even longer button text")
    layout._do_layout(core.Rect(), False)
    layout.sizeHint()
    widget.set_layout(layout)
    assert layout[0] == btn
    for _i in layout:
        pass
    assert len(layout) == 5
    layout.get_children()
    with open("data.pkl", "wb") as jar:
        pickle.dump(layout, jar)
    with open("data.pkl", "rb") as jar:
        layout = pickle.load(jar)


def test_labeledslider(qtbot, qttester):
    slider = custom_widgets.LabeledSlider(["test1", "test2"], "vertical")
    slider_2 = custom_widgets.LabeledSlider(["test1", "test2"])
    qtbot.addWidget(slider)
    qtbot.addWidget(slider_2)
    slider.show()
    qtbot.add_widget(slider)
    qttester.send_mousepress(slider.sl, constants.MouseButton.LeftButton)
    qttester.send_mousemove(slider.sl, core.PointF(20, 20))
    slider.repaint()
    slider.hide()


def test_logtextedit(qtbot):
    textedit = custom_widgets.LogTextEdit()
    qtbot.addWidget(textedit)
    textedit.show()
    logger = logging.getLogger()
    fmt = logging.Formatter(
        "%(asctime)s  %(levelname)s %(levelno)i  %(message)s %(filename)s "
        "%(funcName)s %(module)s %(created)f %(lineno)d %(msecs)d "
        "%(process)d %(thread)d %(threadName)s %(processName)s "
        "%(relativeCreated)s %(name)s %(pathname)s"
    )
    textedit.set_formatter(fmt)
    logger.info("Test")
    try:
        raise Exception
    except Exception as e:
        logger.exception(e)
    textedit.hide()


def test_popupinfo(qtbot):
    popup = custom_widgets.PopupInfo()
    qtbot.addWidget(popup)
    popup.show_popup("test")


def test_roundprogressbar(qtbot):
    bar = custom_widgets.RoundProgressBar()
    qtbot.addWidget(bar)
    bar.show()
    assert bar.minimum() == 0
    assert bar.maximum() == 100
    bar.set_value(50)
    assert bar.get_value() == 50
    bar.set_null_position(40)
    bar.hide()
    bar.set_bar_style("donut")
    bar.set_outline_pen_width(3)
    bar.set_data_pen_width(5)
    bar.set_format(r"%p")
    bar.set_decimals(3)
    bar.set_range(20, 80)


def test_selectionwidget(qtbot):
    widget = custom_widgets.SelectionWidget()
    qtbot.addWidget(widget)

    class Test:
        pass

    test = Test()
    items = {";": "Semicolon", "tab": "Tab", ",": "Comma", test: "class"}
    widget.add_items(items)
    widget.add_items(("a", "b"))
    widget.add_tooltip_icon("test")
    widget.add_custom(label="test", regex=r"\S{1}")
    radiobuttons = [k for k, v in widget.buttons.items()]
    radiobuttons[1].click()
    assert widget.get_value() == "tab"
    radiobuttons[3].click()
    assert widget.current_choice() == test
    for _i in widget:
        pass
    widget.select_radio_by_data(";")
    choice = widget.current_choice()
    assert choice == ";"
    widget.set_value(",")
    assert widget.get_value() == ","
    widget.update_choice(True)


def test_spanslider(qtbot, qttester):
    slider = custom_widgets.SpanSlider()
    qtbot.add_widget(slider)
    slider.show()
    slider.set_lower_value(10)
    slider.set_upper_value(20)
    slider.set_lower_pos(15)
    slider.set_lower_pos(15)
    slider.set_upper_pos(25)
    slider.set_upper_pos(25)
    assert slider.lower_value == 15
    assert slider.upper_value == 25
    slider.set_value((16, 24))
    assert slider.get_value() == (16, 24)
    slider.set_lower_value(12)
    slider.set_upper_pos(20)
    color = gui.Color("blue")
    slider.set_left_color(color)
    slider.set_right_color(color)
    slider._swap_controls()
    slider.trigger_action(slider.SliderAction.SliderNoAction, True)
    slider.trigger_action(slider.SliderAction.SliderSingleStepAdd, True)
    slider.repaint()
    slider._pixel_pos_to_value(100)
    slider._move_pressed_handle()
    qttester.send_mousepress(slider, constants.MouseButton.LeftButton)
    qttester.send_mousemove(slider, core.PointF(20, 20))
    qttester.send_mousemove(slider, core.PointF(0, 0), delay=10)
    assert slider.get_movement_mode() == "no_crossing"
    slider.set_movement_mode("no_overlap")
    slider.close()


def test_waitingspinner(qtbot):
    test_widget = widgets.Widget()
    qtbot.addWidget(test_widget)
    spinner = custom_widgets.WaitingSpinner(parent=test_widget)
    qtbot.addWidget(spinner)
    spinner.repaint()
    spinner.set_line_num(2)
    assert spinner.get_line_num() == 2
    spinner.set_line_length(2)
    assert spinner.get_line_length() == 2
    spinner.set_line_width(2)
    assert spinner.get_line_width() == 2
    spinner.set_inner_radius(2)
    assert spinner.get_inner_radius() == 2
    spinner.set_color("black")
    spinner.set_revolutions_per_second(2)
    spinner.set_trail_fade_percentage(2)
    spinner.set_minimum_trail_opacity(2)
    spinner._rotate()
    spinner.start()
    spinner.stop()
    spinner._update_position()
