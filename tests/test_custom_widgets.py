"""Tests for `prettyqt` package."""

import logging
import re

import pytest

from prettyqt import constants, core, custom_widgets, gui, widgets


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


def test_commandpalette(qtbot):
    palette = custom_widgets.CommandPalette()
    qtbot.addWidget(palette)
    first = [gui.Action(text="Open"), gui.Action(text="Save")]
    palette.add_actions(first)
    assert palette.get_actions() == first
    proxy = palette._table._proxy
    assert proxy.rowCount() == 2  # noqa: PLR2004
    second = [gui.Action(text="Filter rows")]
    palette.set_actions(second)
    assert palette.get_actions() == second
    assert proxy.rowCount() == 1
    assert proxy.index(0, 0).data() == "Filter rows"
    second[0].setText("Zeilen filtern")
    palette.set_actions(palette.get_actions())
    assert proxy.index(0, 0).data() == "Zeilen filtern"
    palette.clear()
    assert palette.get_actions() == []
    assert proxy.rowCount() == 0


def test_commandpalette_subwindow_and_click(qtbot):
    from prettyqt import debugging

    win = widgets.MainWindow()
    qtbot.addWidget(win)
    win.resize(900, 600)
    win.show()
    debugging.pump(ms=20)

    palette = custom_widgets.CommandPalette()
    palette.install_to(win)
    triggered: list[str] = []
    action = gui.Action(
        text="Run command",
        tool_tip="Runs the command",
        shortcut="Ctrl+R",
        triggered=lambda: triggered.append("ran"),
    )
    palette.set_actions([action])

    # Default columns: Name, ToolTip, Shortcut visible; metadata columns hidden
    table = palette._table
    assert not table.isColumnHidden(0)
    assert not table.isColumnHidden(1)
    assert not table.isColumnHidden(2)
    assert all(table.isColumnHidden(c) for c in range(3, table._model.columnCount()))

    palette.show()
    debugging.pump(ms=20)
    assert palette.isVisible()
    exp_w = min(680, max(420, win.width() - 80))
    exp_h = min(380, max(240, win.height() - 120))
    assert (palette.width(), palette.height()) == (exp_w, exp_h)
    assert palette.x() == max(12, (win.width() - exp_w) // 2)
    assert palette.y() == max(36, int(win.height() * 0.12))
    _, warnings = debugging.inspect_tree(win)
    assert not any(w.kind == "out-of-bounds" for w in warnings)

    # Responsive sizing on a smaller parent window
    win.resize(560, 400)
    debugging.pump(ms=20)
    palette.show()
    debugging.pump(ms=20)
    exp_w = min(680, max(420, win.width() - 80))
    exp_h = min(380, max(240, win.height() - 120))
    assert (palette.width(), palette.height()) == (exp_w, exp_h)
    assert palette.x() == max(12, (win.width() - exp_w) // 2)
    assert palette.y() == max(36, int(win.height() * 0.12))

    # Clicking an action triggers it and hides the palette
    table._on_clicked(table._proxy.index(0, 0))
    assert triggered == ["ran"]
    assert not palette.isVisible()

    # Standalone (top-level) palette keeps its default top-level size
    standalone = custom_widgets.CommandPalette()
    qtbot.addWidget(standalone)
    standalone.show()
    assert (standalone.width(), standalone.height()) == (1000, 300)
    standalone.close()


def test_colorchooserbutton(qtbot):
    btn = custom_widgets.ColorChooserButton()
    qtbot.addWidget(btn)
    btn.set_current_color("green")
    assert btn.get_value() == gui.Color("green")
    btn.set_value("blue")
    assert btn.is_valid()


def test_regexeditor(qtbot):
    from prettyqt.custom_widgets import regexeditor

    widget = regexeditor.RegexEditorWidget()
    qtbot.addWidget(widget)
    widget.regex = "[0-9]"
    assert widget.regex == "[0-9]"
    widget.string = "test123"
    assert widget.string == "test123"
    widget.compile_flags = re.IGNORECASE


def test_regexinput_invalid_pattern(qtbot):
    widget = custom_widgets.RegexInput()
    qtbot.addWidget(widget)
    widget.set_pattern("[0-9]")
    with qtbot.wait_signal(widget.value_changed):
        widget._on_value_change()
    widget.set_pattern("[")
    with qtbot.assert_not_emitted(widget.value_changed):
        widget._on_value_change()


def test_flagselectionwidget(qtbot):
    widget = custom_widgets.FlagSelectionWidget()
    qtbot.addWidget(widget)
    items = {0: "MultiLine", 2: "Ignore case"}
    widget.add_items(items)
    assert widget.get_value() == 0


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
    assert len(tl) == 2  # noqa: PLR2004
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
    btn.set_value("/")
    btn.get_value()


# Segfault with PySide6
# def test_objectbrowser(qtbot):
#     struct = dict(a={1, 2, frozenset([1, 2])})
#     browser = custom_widgets.ObjectBrowser(struct)
#     browser.show()
#     browser.close()


# Segfault with PySide6
# def test_fontchooserbutton(qtbot):
#     btn = custom_widgets.FontChooserButton()
#     qtbot.addWidget(btn)
#     btn.set_font("Consolas")


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
    assert w.get_value() == 5  # noqa: PLR2004
    w.set_step_size(2)
    assert w.is_valid()


def test_codeeditor(qtbot):
    editor = custom_widgets.CodeEditor()
    qtbot.addWidget(editor)
    assert not editor.text()
    editor.line_area_width()
    editor.set_syntaxhighlighter("python")
    event = gui.QResizeEvent(core.Size(10, 10), core.Size(20, 20))
    editor.resizeEvent(event)
    editor.repaint()


def test_codeeditor_line_area_width(qtbot):
    editor = custom_widgets.CodeEditor()
    qtbot.addWidget(editor)
    advance = editor.fontMetrics().horizontalAdvance("9")
    # Single-digit line count still reserves at least 2 digits + 10px padding
    assert editor.line_area_width() == 10 + advance * 2
    editor.set_text("\n".join(f"x = {i}" for i in range(100)))
    assert editor.line_area_width() == 10 + advance * 3
    assert editor.line_area_width() > 10 + advance * 2


def test_codeeditor_python_highlighting(qtbot):
    from prettyqt import syntaxhighlighters

    editor = custom_widgets.CodeEditor(language="python")
    qtbot.addWidget(editor)
    assert isinstance(editor._hl, syntaxhighlighters.PygmentsHighlighter)
    old = editor._hl
    editor.set_syntaxhighlighter("python")
    assert old.document() is None  # previous highlighter detached
    editor.set_text("def foo():\n    return 1\n")
    block = editor.document().firstBlock()
    assert block.layout().formats()  # keywords got formats


def test_codeeditor_line_markers(qtbot):
    editor = custom_widgets.CodeEditor()
    qtbot.addWidget(editor)
    editor.set_text("a = 1\nb = (\nc = 3\n")
    editor.add_line_marker(2, "SyntaxError: '(' was never closed")
    editor.add_line_marker(2, "second message", kind="warning")
    assert editor.get_line_marker_text(2) == (
        "SyntaxError: '(' was never closed\nsecond message"
    )
    assert len(editor.extraSelections()) == 1
    editor.set_line_markers({1: "first", 3: "third"}, kind="info")
    assert [(m.line, m.kind) for m in editor.get_line_markers()] == [
        (1, "info"),
        (3, "info"),
    ]
    assert editor.get_line_marker_text(2) == ""
    assert len(editor.extraSelections()) == 2  # noqa: PLR2004
    editor.set_line_markers([custom_widgets.codeeditor.LineMarker(9, "out of range")])
    assert editor.extraSelections() == []  # line does not exist
    editor.clear_line_markers(9)
    assert editor.get_line_markers() == []
    editor.set_line_markers([(1, "x")])
    editor.clear_line_markers()
    assert editor.get_line_markers() == []
    with pytest.raises(ValueError, match="Invalid marker kind"):
        editor.add_line_marker(1, "x", kind="fatal")  # type: ignore[arg-type]
    editor.add_line_marker(1, "boom")
    editor.show()
    editor.repaint()
    block = editor.document().firstBlock()
    geom = editor.blockBoundingGeometry(block).translated(editor.contentOffset())
    pos = geom.center().toPoint()
    assert editor.show_marker_tooltip(pos, editor.mapToGlobal(pos))
    assert not editor.show_marker_tooltip(core.QPoint(1, 5000), core.QPoint(1, 1))


def test_codeeditor_read_only(qtbot):
    editor = custom_widgets.CodeEditor()
    qtbot.addWidget(editor)
    editor.set_text("x = 1")
    editor.set_read_only()
    assert editor.isReadOnly()
    qtbot.keyClicks(editor, "abc")
    assert editor.text() == "x = 1"
    editor.set_text("y = 2")  # programmatic changes still work
    assert editor.text() == "y = 2"


def test_codeeditor_set_text_keeps_position(qtbot):
    editor = custom_widgets.CodeEditor()
    qtbot.addWidget(editor)
    editor.resize(300, 100)
    editor.show()
    text = "\n".join(f"line_{i} = {i}" for i in range(200))
    editor.set_text(text)
    cursor = editor.textCursor()
    cursor.setPosition(500)
    editor.setTextCursor(cursor)
    editor.verticalScrollBar().setValue(50)
    editor.set_text(text.replace("line_0 ", "line_zero "))
    assert editor.textCursor().position() == 500  # noqa: PLR2004
    assert editor.verticalScrollBar().value() == 50  # noqa: PLR2004
    assert editor.text().startswith("line_zero")
    editor.undo()  # change is undoable
    assert editor.text() == text
    editor.set_text("short")
    assert editor.textCursor().position() == len("short")
    editor.set_text("reset", keep_position=False)
    assert editor.textCursor().position() == 0
    editor.set_value("via value")
    assert editor.get_value() == "via value"


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
    assert len(layout) == 5  # noqa: PLR2004
    layout.get_children()


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
        raise Exception  # noqa: TRY002, TRY301
    except Exception:
        logger.exception("Exception!")
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
    assert bar.maximum() == 100  # noqa: PLR2004
    bar.set_value(50)
    assert bar.get_value() == 50  # noqa: PLR2004
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
    assert slider.lower_value == 15  # noqa: PLR2004
    assert slider.upper_value == 25  # noqa: PLR2004
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
    assert spinner.get_line_num() == 2  # noqa: PLR2004
    spinner.set_line_length(2)
    assert spinner.get_line_length() == 2  # noqa: PLR2004
    spinner.set_line_width(2)
    assert spinner.get_line_width() == 2  # noqa: PLR2004
    spinner.set_inner_radius(2)
    assert spinner.get_inner_radius() == 2  # noqa: PLR2004
    spinner.set_color("black")
    spinner.set_revolutions_per_second(2)
    spinner.set_trail_fade_percentage(2)
    spinner.set_minimum_trail_opacity(2)
    spinner._rotate()
    spinner.start()
    spinner.stop()
    spinner._update_position()


def test_astviewer_rename_variable(qtbot):
    viewer = custom_widgets.AstViewer()
    qtbot.addWidget(viewer)
    viewer.set_ast("a = 1\nb = a + 1\n")
    viewer.rename_variable("a", "x")
    assert viewer.textedit.text() == "x = 1\nb = x + 1"


def test_localeedit_is_valid(qtbot):
    edit = custom_widgets.LocaleEdit()
    qtbot.addWidget(edit)
    edit.set_current_locale("de_DE")
    assert edit.is_valid()


def test_subsequencecompleter(qtbot):
    completer = custom_widgets.SubsequenceCompleter()
    model = core.StringListModel(["apple", "banana", "pineapple"])
    completer.setModel(model)
    completer.proxy_model.set_search_term("ple")
    assert completer.proxy_model.rowCount() == 2  # noqa: PLR2004


def test_widgeteditor_and_details_dialog(qtbot):
    from prettyqt import debugging

    button = widgets.PushButton()
    qtbot.addWidget(button)
    editor = custom_widgets.WidgetEditor(button)
    qtbot.addWidget(editor)
    dialog = debugging.QObjectDetailsDialog(button)
    qtbot.addWidget(dialog)


def test_smoothscrollbar_easing(qtbot):
    area = widgets.ScrollArea()
    qtbot.addWidget(area)
    bar = custom_widgets.SmoothScrollBar(parent=area)
    assert isinstance(bar.animationEasing(), core.QEasingCurve.Type)


def test_sectionautospan_eventfilter(qtbot):
    from prettyqt import eventfilters, gui

    table = widgets.TableView()
    qtbot.addWidget(table)
    table.set_model(gui.StandardItemModel.from_dict(dict(a=[1, 1], b=[2, 3])))
    event_filter = eventfilters.SectionAutoSpanEventFilter(table)
    event_filter._update_spans(force=True)


def test_svgbuffericonengine_disabled(qapp):
    from prettyqt import gui
    from prettyqt.iconprovider import svgbuffericonengine

    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><rect width="1" height="1" fill="currentColor"/></svg>'  # noqa: E501
    engine = svgbuffericonengine.SVGBufferIconEngine(svg)
    pixmap = gui.Pixmap(8, 8)
    painter = gui.Painter(pixmap)
    engine.paint(
        painter, core.QRect(0, 0, 8, 8), gui.QIcon.Mode.Disabled, gui.QIcon.State.Off
    )
    painter.end()


@pytest.mark.parametrize("mode", ["multi", "single"])
def test_scrollareatocwidget_scroll(qtbot, mode):
    from prettyqt.custom_widgets import scrollareatocwidget

    window = widgets.Widget()
    qtbot.addWidget(window)
    layout = window.set_layout("horizontal")
    scrollarea = widgets.ScrollArea(parent=window, widget_resizable=True)
    widget = widgets.Widget()
    scrollarea.setWidget(widget)
    toc = scrollareatocwidget.ScrollAreaTocWidget(
        scrollarea, widget_class=scrollareatocwidget.SectionWidget
    )
    toc.set_scroll_mode(mode)
    layout.add(toc)
    scroll_layout = widget.set_layout("vertical")
    layout.add(scrollarea)
    for i in range(3):
        scroll_layout.add(scrollareatocwidget.SectionWidget(window_title=f"s{i}"))
    window.show()
    toc._on_scroll()


def test_accordionwidget(qtbot):
    from prettyqt.custom_widgets.accordionwidget import AccordionWidget

    accordion = AccordionWidget()
    qtbot.addWidget(accordion)
    first = widgets.Label("first")
    accordion.addItem("First", first)
    accordion.addItem("Second", widgets.Label("second"), collapsed=True)
    assert accordion.count() == 2  # noqa: PLR2004
    assert accordion.indexOf(first) == 0
    accordion.move_item_down(0)
    assert accordion.indexOf(first) == 1
    accordion.move_item_up(1)
    assert accordion.takeAt(0) is not None
    accordion.clear()
    assert accordion.count() == 0


def test_smoothscrollbar_properties_and_eventfilter(qtbot):
    area = widgets.ScrollArea()
    qtbot.addWidget(area)
    bar = custom_widgets.SmoothScrollBar("horizontal", parent=area)
    bar.animation_duration = 250
    assert bar.animation_duration == 250  # noqa: PLR2004
    bar.animation_easing = "linear"
    assert bar.get_animation_easing() == "linear"
    v_bar = widgets.ScrollBar("vertical", parent=area)
    area.setVerticalScrollBar(v_bar)
    v_bar.setRange(0, 1000)
    wheel_ev = gui.QWheelEvent(
        core.PointF(0, 0),
        core.PointF(0, 0),
        core.Point(0, 0),
        core.Point(0, -120),
        constants.MouseButton.NoButton,
        constants.KeyboardModifier.NoModifier,
        constants.ScrollPhase.NoScrollPhase,
        False,
    )
    assert bar.eventFilter(area.viewport(), wheel_ev) is True
    assert v_bar.value() == 120  # noqa: PLR2004


def test_accordionwidget_drag_scroll(qtbot):
    from prettyqt.custom_widgets.accordionwidget import AccordionWidget

    accordion = AccordionWidget()
    qtbot.addWidget(accordion)
    for i in range(5):
        lbl = widgets.Label(f"item {i}")
        lbl.setMinimumHeight(200)
        accordion.addItem(f"Item {i}", lbl)
    accordion.resize(200, 150)
    accordion.show()
    press = gui.QMouseEvent(
        core.QEvent.Type.MouseButtonPress,
        core.PointF(10, 10),
        core.PointF(10, 10),
        constants.MouseButton.LeftButton,
        constants.MouseButton.LeftButton,
        constants.KeyboardModifier.NoModifier,
    )
    move = gui.QMouseEvent(
        core.QEvent.Type.MouseMove,
        core.PointF(10, 50),
        core.PointF(10, 50),
        constants.MouseButton.LeftButton,
        constants.MouseButton.LeftButton,
        constants.KeyboardModifier.NoModifier,
    )
    release = gui.QMouseEvent(
        core.QEvent.Type.MouseButtonRelease,
        core.PointF(10, 50),
        core.PointF(10, 50),
        constants.MouseButton.LeftButton,
        constants.MouseButton.NoButton,
        constants.KeyboardModifier.NoModifier,
    )
    accordion.mousePressEvent(press)
    accordion.mouseMoveEvent(move)
    accordion.mouseReleaseEvent(release)


def test_iconedit_and_paletteedit_defaults(qtbot):
    icon_edit = custom_widgets.IconEdit()
    qtbot.addWidget(icon_edit)
    assert isinstance(icon_edit.get_value(), gui.Icon)

    palette_edit = custom_widgets.PaletteEdit()
    qtbot.addWidget(palette_edit)
    assert isinstance(palette_edit.get_value(), gui.Palette)


def test_sliceedit(qtbot):
    edit = custom_widgets.SliceEdit()
    qtbot.addWidget(edit)
    assert edit.get_value() == slice(None, None, None)
    edit.set_value(slice(1, 10, 2))
    assert edit.get_value() == slice(1, 10, 2)
    with qtbot.wait_signal(edit.value_changed):
        edit.checkbox_start.setChecked(False)
    assert edit.get_value() == slice(None, 10, 2)
    with qtbot.wait_signal(edit.value_changed):
        edit.checkbox_step.setChecked(False)
    assert edit.get_value() == slice(None, 10, None)
    assert edit.spinbox_step.minimum() >= 1


def test_enumflagwidget_clears_bits(qtbot):
    widget = custom_widgets.EnumFlagWidget()
    qtbot.addWidget(widget)
    both = constants.AlignmentFlag.AlignLeft | constants.AlignmentFlag.AlignTop
    widget.set_value(both)
    assert widget.get_value() == both
    widget.set_value(constants.AlignmentFlag.AlignLeft)
    assert widget.get_value() == constants.AlignmentFlag.AlignLeft
    widget.set_value(constants.AlignmentFlag(0))
    assert widget.get_value() == constants.AlignmentFlag(0)


def test_numfilterwidget_intermediate_input(qtbot):
    widget = custom_widgets.NumFilterWidget()
    qtbot.addWidget(widget)
    fn = widget.get_filter_fn()
    assert fn is not None
    assert fn(42) is True
    for intermediate in ("-", ".", "1e"):
        widget.lineedit.setText(intermediate)
        assert widget.get_filter_fn() is None
    widget.lineedit.setText("5.5")
    fn = widget.get_filter_fn()
    assert fn is not None
    assert fn(5.5) is True
    assert fn(6.0) is False


def test_actiongridbutton_no_default_action(qtbot):
    from prettyqt.custom_widgets import actiongrid

    assert actiongrid.AcionGridButton is actiongrid.ActionGridButton
    btn = actiongrid.ActionGridButton()
    qtbot.addWidget(btn)
    btn._update_text()
    btn.resize(80, 40)


def test_overlayborder_fill_color_property(qtbot):
    from prettyqt.custom_widgets.overlayborder import OverlayBorder

    parent = widgets.Widget()
    qtbot.addWidget(parent)
    overlay = OverlayBorder(parent)
    original_border = overlay.get_border_color()
    overlay.setProperty("fill_color", gui.QColor("blue"))
    assert overlay.get_fill_color() == gui.Color("blue")
    assert overlay.get_border_color() == original_border


def test_filterheader_editors_parent_and_visibility(qtbot):
    view = widgets.TableView()
    qtbot.addWidget(view)
    model = gui.StandardItemModel.from_dict(dict(a=["x"], b=[object()]))
    view.set_model(model)
    header = custom_widgets.FilterHeader(parent=view)
    view.setHorizontalHeader(header)
    assert len(header._editors) == 2  # noqa: PLR2004
    assert all(ed.parent() is header for ed in header._editors)
    assert all(not ed.isVisible() for ed in header._editors)
    header.set_editors_visible(True)
    assert header.are_editors_visible() is True


def test_crossfadewidget_and_imageviewer_str_path(qtbot, tmp_path):
    img_path = tmp_path / "test.png"
    pm = gui.Pixmap(16, 16)
    pm.fill(gui.Color("red"))
    assert pm.save(str(img_path))

    cf = custom_widgets.CrossFadeWidget(str(img_path), img_path)
    qtbot.addWidget(cf)
    assert cf.pixmap_1 is not None
    assert not cf.pixmap_1.isNull()
    assert cf.pixmap_2 is not None
    assert not cf.pixmap_2.isNull()

    viewer = custom_widgets.ImageViewer(str(img_path))
    qtbot.addWidget(viewer)
    assert not viewer.pixmap().isNull()


def test_gridsplitter_empty_and_indexing(qtbot):
    from prettyqt.custom_widgets.gridsplitter import GridSplitter

    splitter = GridSplitter()
    qtbot.addWidget(splitter)
    assert splitter.columnCount() == 0
    w00 = widgets.Label("0,0")
    w01 = widgets.Label("0,1")
    w10 = widgets.Label("1,0")
    w11 = widgets.Label("1,1")
    splitter[0, 0] = w00
    splitter[0, 1] = w01
    splitter[1, 0] = w10
    splitter[1, 1] = w11
    assert splitter.columnCount() == 2  # noqa: PLR2004
    assert splitter[0] is w00
    assert splitter[3] is w11
    assert splitter[-1] is w11
    assert list(splitter[1:3]) == [w01, w10]
    with pytest.raises(IndexError):
        _ = splitter[4]


def test_misc_custom_widgets_fixes(qtbot):
    from prettyqt.custom_widgets.joystickbutton import JoystickButton
    from prettyqt.custom_widgets.twolistsselectionwidget import TwoListsSelectionWidget

    # TwoListsSelectionWidget
    two = TwoListsSelectionWidget()
    qtbot.addWidget(two)
    two.add_items_left(["a", "b"])
    two.right_list.addItem("r0")
    two.right_list.setCurrentRow(0)
    two.left_list.item(0).setSelected(True)
    assert two.to_right_btn.isEnabled()

    # BorderLayout & FlowLayout negative index
    bl = custom_widgets.BorderLayout()
    assert bl.itemAt(-1) is None
    assert bl.takeAt(-1) is None
    fl = custom_widgets.FlowLayout()
    assert fl.itemAt(-1) is None
    assert fl.takeAt(-1) is None

    # JoystickButton resize keeps state and move before press is safe
    jb = JoystickButton()
    qtbot.addWidget(jb)
    jb.set_state((100.0, 0.0))
    state_before = jb.get_state()
    jb.resizeEvent(gui.QResizeEvent(core.Size(60, 60), core.Size(50, 50)))
    assert jb.get_state() == state_before

    # PopupInfo text kwarg
    popup = custom_widgets.PopupInfo(text="Hello")
    qtbot.addWidget(popup)
    assert popup.label.text() == "Hello"

    # UrlLineEdit object_name
    url_edit = custom_widgets.UrlLineEdit()
    qtbot.addWidget(url_edit)
    assert url_edit.objectName() == "url_lineedit"

    # SidebarWidget add_tab(show=True)
    sb = custom_widgets.SidebarWidget()
    qtbot.addWidget(sb)
    p1 = widgets.Widget()
    p2 = widgets.Widget()
    sb.add_tab(p1, "One")
    sb.add_tab(p2, "Two", show=True)
    assert sb.button_map[p2].isChecked()
    assert not sb.button_map[p1].isChecked()
