"""Tests for `prettyqt` package."""

import importlib.util
import itertools
import pathlib
import pickle
import sys

import pytest

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import InvalidParamError


def pickle_roundtrip(something):
    path = pathlib.Path("data.pkl")
    with path.open("wb") as jar:
        pickle.dump(something, jar)
    with path.open("rb") as jar:
        return pickle.load(jar)


def test_action(qtbot):
    action = gui.Action()
    action.set_tooltip("test")
    action.set_enabled()
    action.set_disabled()
    action.set_icon(None)
    action.set_icon("mdi.timer")
    action.set_shortcut("Ctrl+A")
    assert action.shortcut().toString() == "Ctrl+A"
    assert action.toolTip() == "test"
    action.set_priority("low")
    with pytest.raises(InvalidParamError):
        action.set_priority("test")
    assert action.get_priority() == "low"
    action.set_menu_role("preferences")
    with pytest.raises(InvalidParamError):
        action.set_menu_role("test")
    assert action.get_menu_role() == "preferences"
    action.set_shortcut_context("widget_with_children")
    with pytest.raises(InvalidParamError):
        action.set_shortcut_context("test")
    assert action.get_shortcut_context() == "widget_with_children"
    action.show_shortcut_in_contextmenu()
    action.set_menu(widgets.Menu())


def test_actiongroup(qtbot):
    group = gui.ActionGroup(None)
    group.set_exclusion_policy(None)
    group.set_exclusion_policy("exclusive")
    with pytest.raises(InvalidParamError):
        group.set_exclusion_policy("test")
    assert group.get_exclusion_policy() == "exclusive"
    act = gui.Action()
    group.addAction(act)
    assert group[0] == act
    assert act in group
    assert len(group) == 1


def test_brush():
    brush = gui.Brush()
    bytes(brush)
    brush.set_style("cross")
    with pytest.raises(InvalidParamError):
        brush.set_style("test")
    assert brush.get_style() == "cross"


@pytest.mark.skipif(sys.platform == "darwin", reason="Somehow fails on OSX")
def test_clipboard(qapp):
    mimedata = core.QMimeData()
    pixmap = gui.Pixmap(100, 100)
    image = pixmap.toImage()
    cb = qapp.get_clipboard()
    cb.set_mimedata(mimedata)
    cb.set_image(image)
    cb.set_pixmap(pixmap)
    assert cb.get_mimedata()
    assert cb.get_image() == image
    assert cb.get_pixmap().size() == pixmap.size()


def test_color(qapp):
    color = gui.Color()
    assert color.get_spec() == "invalid"
    color.set_color("gray")
    color = pickle_roundtrip(color)
    assert str(color) == "#808080"
    color.convert_to("rgb")
    color.convert_to("hsv")
    color.convert_to("cmyk")
    color.convert_to("hsl")
    color.convert_to("extended_rgb")
    # color.as_qt()


def test_colorspace():
    space = gui.ColorSpace()
    bytes(space)
    assert not bool(space)
    space = pickle_roundtrip(space)
    space.set_primaries("dci_p3_d65")
    with pytest.raises(InvalidParamError):
        space.set_primaries("test")
    assert space.get_primaries() == "dci_p3_d65"
    space.set_transfer_function("pro_photo_rgb")
    with pytest.raises(InvalidParamError):
        space.set_transfer_function("test")
    assert space.get_transfer_function() == "pro_photo_rgb"


def test_cursor(qapp):
    cursor = gui.Cursor()
    cursor.set_shape("arrow")
    with pytest.raises(InvalidParamError):
        cursor.set_shape("test")
    assert cursor.get_shape() == "arrow"
    cursor = pickle_roundtrip(cursor)
    bytes(cursor)
    cursor.get_pos()


# def test_desktopservices():
#     gui.DesktopServices.open_url("test")


def test_doublevalidator():
    val = gui.DoubleValidator()
    val.setRange(0, 9)
    val = pickle_roundtrip(val)
    assert val.is_valid_value("4")
    assert not val.is_valid_value("10")


def test_font(qapp):
    font = gui.Font("Consolas")
    assert font.metrics
    font = gui.Font.mono()
    with pytest.raises(InvalidParamError):
        font.set_style_hint("test")
    font.set_style_hint("monospace")
    font.set_weight("thin")
    with pytest.raises(InvalidParamError):
        font.set_weight("test")
    assert font.get_weight() == "thin"
    font.set_capitalization("small_caps")
    with pytest.raises(InvalidParamError):
        font.set_capitalization("test")
    assert font.get_capitalization() == "small_caps"
    font.set_style("oblique")
    with pytest.raises(InvalidParamError):
        font.set_style("test")
    assert font.get_style() == "oblique"
    font.set_hinting_preference("vertical")
    with pytest.raises(InvalidParamError):
        font.set_hinting_preference("test")
    assert font.get_hinting_preference() == "vertical"
    font.set_letter_spacing("absolute", 20)
    with pytest.raises(InvalidParamError):
        font.set_letter_spacing("test", 20)
    assert font.get_letter_spacing_type() == "absolute"


def test_fontdatabase():
    p = pathlib.Path()
    gui.FontDatabase.add_fonts_from_folder(p)
    gui.FontDatabase.get_system_font("smallest_readable")
    with pytest.raises(InvalidParamError):
        gui.FontDatabase.get_system_font("test")


def test_fontinfo():
    font = gui.Font("Consolas")
    fontinfo = gui.FontInfo(font)
    assert fontinfo.get_style_hint() == "any"


def test_fontmetrics():
    font = gui.Font("Consolas")
    fontmetrics = gui.FontMetrics(font)
    val = fontmetrics.elided_text("This is a test", mode="right", width=40)
    with pytest.raises(InvalidParamError):
        val = fontmetrics.elided_text("This is a test", mode="test", width=40)
    assert len(val) < 10  # noqa: PLR2004
    fontmetrics.get_bounding_rect("test")
    fontmetrics.get_tight_bounding_rect("test")


def test_fontmetricsf():
    font = gui.Font("Consolas")
    fontmetrics = gui.FontMetricsF(font)
    val = fontmetrics.elided_text("This is a test", mode="right", width=40)
    with pytest.raises(InvalidParamError):
        val = fontmetrics.elided_text("This is a test", mode="test", width=40)
    assert len(val) < 10  # noqa: PLR2004
    fontmetrics.get_bounding_rect("test")
    fontmetrics.get_tight_bounding_rect("test")


def test_gradient():
    grad = gui.Gradient()
    grad.set_coordinate_mode("object")
    assert grad.get_coordinate_mode() == "object"
    with pytest.raises(InvalidParamError):
        grad.set_coordinate_mode("test")
    grad.set_spread("repeat")
    assert grad.get_spread() == "repeat"
    with pytest.raises(InvalidParamError):
        grad.set_spread("test")
    assert grad.get_type() == "none"


def test_guiapplication():
    with gui.GuiApplication.override_cursor("forbidden"):
        pass


def test_icon(qapp):
    icon = gui.Icon()
    icon.for_color("black")
    icon = pickle_roundtrip(icon)
    with pytest.raises(InvalidParamError):
        icon.get_available_sizes(mode="test")
    with pytest.raises(InvalidParamError):
        icon.get_available_sizes(state="test")
    icon.get_available_sizes()
    icon.add_pixmap(b"a")
    icon.get_actual_size((256, 256))


def test_iconengine(qapp):
    engine = gui.IconEngine()
    engine.get_available_sizes()
    engine.get_actual_size((100, 100))
    engine.get_actual_size(100)
    with pytest.raises(InvalidParamError):
        engine.get_actual_size(100, state="test")
    with pytest.raises(InvalidParamError):
        engine.get_actual_size(100, mode="test")
    px = gui.Pixmap()
    engine.add_pixmap(px, mode="normal", state="off")


def test_image(qapp):
    img = gui.Image()
    img = pickle_roundtrip(img)
    bytes(img)


@pytest.mark.skipif(importlib.util.find_spec("PIL") is None, reason="PIL not installed")
def test_image_pil(qapp):
    image = gui.Pixmap(100, 100).to_image()
    pil_image = image.to_pil()
    assert gui.Image.from_pil(pil_image)


def test_imageiohandler():
    handler = gui.ImageIOHandler()
    handler.get_format()
    handler.set_option("gamma", 0.5)
    assert handler.get_option("gamma") is None
    handler["quality"] = 0.6
    assert handler["quality"] is None
    assert handler.supports_option("animation") is False


def test_imagereader():
    reader = gui.ImageReader()
    assert reader.get_error() == "unknown"
    reader.get_background_color()
    reader.get_clip_rect()
    reader.get_current_image_rect()
    reader.get_scaled_clip_rect()
    reader.get_size()
    reader.get_scaled_size()
    reader.get_subtype()
    reader.get_supported_subtypes()
    reader.set_format("xsn")
    assert reader.get_format() == "xsn"
    assert reader.get_transformation() == "none"
    reader.read_image()
    assert reader.supports_option("gamma") is False


def test_imagewriter(qapp):
    writer = gui.ImageWriter()
    writer["test"] = "Test"
    assert writer.get_error() == "unknown"
    writer.set_subtype("xsn")
    assert writer.get_subtype() == "xsn"
    writer.get_supported_image_formats()
    writer.get_supported_subtypes()
    writer.set_format("abc")
    assert writer.get_format() == "abc"
    writer.set_transformation("rotate_270")
    assert writer.get_transformation() == "rotate_270"


def test_inputmethod(qapp):
    input_method = qapp.get_input_method()
    input_method.get_anchor_rectangle()
    input_method.get_cursor_rectangle()
    input_method.get_input_item_clip_rectangle()
    input_method.get_input_item_rectangle()
    input_method.get_keyboard_rectangle()
    input_method.get_locale()
    assert input_method.get_input_direction() == "left_to_right"


def test_intvalidator():
    val = gui.IntValidator()
    val.setRange(0, 9)
    val = pickle_roundtrip(val)
    assert val.is_valid_value("4")
    assert not val.is_valid_value("10")


def test_keysequence():
    assert (
        gui.KeySequence.to_shortcut_str(
            constants.Key.Key_A, constants.KeyboardModifier.ShiftModifier
        )
        == "Shift+A"
    )
    comb = core.KeyCombination(
        constants.KeyboardModifier.ShiftModifier, constants.Key.Key_A
    )
    assert gui.KeySequence.to_shortcut_str(comb) == "Shift+A"
    seq = gui.KeySequence("Ctrl+C")
    assert seq.get_matches("Ctrl+C") == "exact"
    pickle_roundtrip(seq)


def test_movie():
    movie = gui.Movie()
    with pytest.raises(InvalidParamError):
        movie.set_cache_mode("test")
    movie.set_cache_mode("all")
    assert movie.get_cache_mode() == "all"
    movie = pickle_roundtrip(movie)
    repr(movie)


def test_screen(qapp):
    screen = qapp.get_primary_screen()
    screen.get_geometry()
    screen.get_size()
    screen.get_available_geometry()
    screen.get_available_size()
    screen.get_available_virtual_geometry()
    screen.get_available_virtual_size()
    screen.get_virtual_geometry()
    screen.get_virtual_size()
    screen.get_native_orientation()
    screen.get_orientation()
    screen.get_primary_orientation()
    screen.get_physical_size()
    screen.get_angle_between("primary", "landscape")
    w = widgets.Widget()
    screen.grab_window(w.winId())
    screen.get_virtual_siblings()


def test_shortcut(qtbot):
    w = widgets.Widget()
    qtbot.addWidget(w)
    seq = gui.KeySequence("Ctrl+C")
    shortcut = gui.Shortcut(seq, w)
    assert str(shortcut) == "Ctrl+C"
    shortcut.set_context("application")
    with pytest.raises(InvalidParamError):
        shortcut.set_context("test")
    assert shortcut.get_context() == "application"
    assert shortcut.get_key() == seq


# def test_sessionmanager():
#     manager = gui.SessionManager()
#     with pytest.raises(InvalidParamError):
#         manager.set_restart_hint("test")
#     manager.set_restart_hint("immediately")
#     assert manager.get_restart_hint() == "immediately"


def test_standarditem(qapp):
    item = gui.StandardItem()
    item = pickle_roundtrip(item)
    # item[constants.USER_ROLE] = "test"
    # assert item[constants.USER_ROLE] == "test"
    item.set_icon("mdi.timer")
    item.set_checkstate("unchecked")
    with pytest.raises(InvalidParamError):
        item.set_checkstate("test")
    assert item.get_checkstate() == "unchecked"
    item.get_background()
    item.get_foreground()
    item.get_font()
    item.get_icon()
    bytes(item)
    item.clone()
    item.add_item(
        "Test",
        icon="mdi.timer",
        data={1: "Test"},
        foreground=gui.Brush(),
        background=gui.Brush(),
        font=gui.Font(),
        selectable=True,
        status_tip="test",
        tool_tip="test",
        whats_this="test",
        checkstate="unchecked",
        size_hint=core.Size(10, 10),
        is_user_type=True,
    )


def test_standarditemmodel(qapp):
    model = gui.StandardItemModel()
    model.add("test")
    for _item in model:
        pass
    model = pickle_roundtrip(model)
    model += gui.StandardItem("Item")
    model[0]
    assert len(model.find_items("test")) == 1
    with pytest.raises(InvalidParamError):
        model.find_items("test", mode="wrong_mode")
    del model[0]
    model.add_item(
        "Test",
        icon="mdi.timer",
        data={1: "Test"},
        foreground=gui.Brush(),
        background=gui.Brush(),
        font=gui.Font(),
        selectable=True,
        status_tip="test",
        tool_tip="test",
        whats_this="test",
        checkstate="unchecked",
        size_hint=core.Size(10, 10),
        is_user_type=True,
    )


def test_statictext():
    text = gui.StaticText("test")
    repr(text)
    assert str(text) == "test"
    text.set_text_format("rich")
    with pytest.raises(InvalidParamError):
        text.set_text_format("test")
    assert text.get_text_format() == "rich"
    text.set_performance_hint("aggressive")
    with pytest.raises(InvalidParamError):
        text.set_performance_hint("test")
    assert text.get_performance_hint() == "aggressive"


def test_transform():
    transform = gui.Transform()
    for i, j in itertools.product(range(3), range(3)):
        assert transform[i, j] in [0, 1]
    bytes(transform)
    repr(transform)
    assert transform.get_type() == "none"
    transform = gui.Transform.clone_from(transform)


def test_textblock():
    block = gui.TextBlock()
    repr(block)
    assert 1 not in block


def test_textblockformat():
    block = gui.TextBlockFormat()
    block.set_alignment("left")
    with pytest.raises(InvalidParamError):
        block.set_alignment("test")
    assert block.get_alignment() == "left"
    block.set_marker("unchecked")
    with pytest.raises(InvalidParamError):
        block.set_marker("test")
    assert block.get_marker() == "unchecked"


def test_textblockgroup():
    doc = gui.TextDocument()
    group = gui.TextBlockGroup(doc)
    repr(group)
    for _textblock in group:
        pass


def test_textcursor():
    cursor = gui.TextCursor()
    cursor.set_position(1, "move")
    cursor.move_position("start", "move", 1)
    cursor.select("document")
    cursor.replace_text(0, 2, "test")
    cursor.select_text(1, 3)
    cursor.span()
    with cursor.edit_block():
        pass


def test_textdocument():
    doc = gui.TextDocument("This is a test\nHello")
    for i in doc:
        repr(i)
    assert doc[1].text() == "Hello"
    assert len(doc) == 2  # noqa: PLR2004
    doc.set_text("test")
    doc.clear_stacks("undo_and_redo")
    with pytest.raises(InvalidParamError):
        doc.clear_stacks("test")
    # doc.add_resource("html")
    doc.set_default_cursor_move_style("logical")
    assert doc.get_default_cursor_move_style() == "logical"
    with pytest.raises(InvalidParamError):
        doc.set_default_cursor_move_style("test")
    doc.set_meta_information("document_title", "test")
    assert doc.get_meta_information("document_title") == "test"
    with pytest.raises(InvalidParamError):
        doc.set_meta_information("test", "test")
    with pytest.raises(InvalidParamError):
        doc.get_meta_information("test")


def test_paintdevice():
    device = gui.PaintDevice()
    device.get_metric("depth")
    with pytest.raises(InvalidParamError):
        device.get_metric("test")


def test_painter():
    class Test(widgets.Widget):
        def paintEvent(self, event):
            with gui.Painter(self) as painter:
                painter.use_antialiasing()
                painter.set_pen("none")
                painter.set_transparent_background(False)
                painter.set_transparent_background(True)
                painter.set_brush(gui.Brush())
                with painter.paint_on(widgets.Widget()):
                    pass
                painter.set_brush(gui.Color("red"))
                painter.fill_rect((0, 1, 3, 5), "transparent")
                painter.fill_rect(core.Rect(), "transparent")
                with pytest.raises(InvalidParamError):
                    painter.fill_rect(core.Rect(), "transparent", "test")
                with pytest.raises(ValueError):  # noqa: PT011
                    painter.fill_rect(core.Rect(), "testus")
                painter.set_color("black")
                painter.set_composition_mode("source_atop")
                assert painter.get_composition_mode() == "source_atop"
                with pytest.raises(InvalidParamError):
                    painter.set_composition_mode("test")
                painter.set_clip_path(gui.PainterPath(), "replace")
                with pytest.raises(InvalidParamError):
                    painter.set_clip_path(gui.PainterPath(), "test")
                with pytest.raises(InvalidParamError):
                    painter.set_pen(style="test")
                with painter.backup_state():
                    pass
                assert painter.get_text_rect("test") is not None

    w = Test()
    w.repaint()
    # assert painter.get_composition_mode() == "source_atop"


def test_pagelayout():
    layout = gui.PageLayout()
    with pytest.raises(InvalidParamError):
        layout.set_orientation("test")
    layout.set_orientation("landscape")
    assert layout.get_orientation() == "landscape"
    with pytest.raises(InvalidParamError):
        layout.set_mode("test")
    layout.set_mode("full_page")
    assert layout.get_mode() == "full_page"
    with pytest.raises(InvalidParamError):
        layout.set_units("test")
    layout.set_units("pica")
    assert layout.get_units() == "pica"
    layout.get_page_size()


def test_pagesize():
    size = gui.PageSize()
    assert size.get_id() == "custom"
    with pytest.raises(ValueError):  # noqa: PT011
        size.get_definition_units()
    size = gui.PageSize(gui.PageSize.PageSizeId.A3)
    size = pickle_roundtrip(size)
    assert size.get_definition_units() == "millimeter"


def test_painterpath():
    path = gui.PainterPath()
    rect = core.RectF(0, 0, 1, 1)
    path.addRect(rect)
    assert len(path) == 5  # noqa: PLR2004
    assert bool(path)
    assert core.PointF(0.5, 0.5) in path
    path[1] = (0.5, 0.5)
    path.add_rect(core.QRect(0, 0, 1, 1))


def test_painterpathstroker():
    stroke = gui.PainterPathStroker()
    stroke.set_cap_style("round")
    with pytest.raises(InvalidParamError):
        stroke.set_cap_style("test")
    assert stroke.get_cap_style() == "round"
    stroke.set_join_style("bevel")
    with pytest.raises(InvalidParamError):
        stroke.set_join_style("test")
    assert stroke.get_join_style() == "bevel"


def test_palette():
    pal = gui.Palette()
    assert len(pal.get_colors()) == 21  # noqa: PLR2004
    assert len(pal.get_brushes()) == 21  # noqa: PLR2004
    color = gui.Color("red")
    pal.set_brush("window", "red")
    assert pal.get_brush("window") == color
    pal.highlight_inactive()
    pal.set_color("window", "red")
    pal["button"] = color
    assert pal["button"] == color
    bytes(pal)


def test_pdfwriter():
    writer = gui.PdfWriter("test")
    writer.set_desktop_resolution()
    writer.set_page_margins((0, 0, 0, 0), unit="pica")
    writer.set_pdf_version("v1_6")
    assert writer.get_pdf_version() == "v1_6"
    with pytest.raises(InvalidParamError):
        writer.set_pdf_version("test")


def test_pen():
    pen = gui.Pen()
    pen.set_color("blue")
    pen.set_cap_style("round")
    with pytest.raises(InvalidParamError):
        pen.set_cap_style("test")
    assert pen.get_cap_style() == "round"
    pen.set_join_style("bevel")
    with pytest.raises(InvalidParamError):
        pen.set_join_style("test")
    assert pen.get_join_style() == "bevel"
    pen.set_style("dash_dot")
    with pytest.raises(InvalidParamError):
        pen.set_style("test")
    assert pen.get_style() == "dash_dot"
    bytes(pen)


def test_picture():
    picture = gui.Picture()
    bytes(picture)


def test_pixmap(qapp):
    pix = gui.Pixmap()
    bytes(pix)
    pix.create_dot()
    pix.get_size()
    pix.get_rect()
    pix.to_image()


# def test_pixmapcache():
#     cache = gui.PixmapCache()
#     pix = gui.Pixmap()
#     cache["test"] = pix
#     cached = cache["test"]
#     assert pix.size() == cached.size()


def test_polygonf():
    poly = gui.PolygonF()
    poly.add_points((0, 0), (2, 0), (2, 1), (0, 1))
    poly2 = gui.PolygonF()
    poly2.add_points((1, 0), (3, 0), (3, 1), (1, 1))
    poly = pickle_roundtrip(poly)
    union = poly | poly2
    intersect = poly & poly2
    sub = union - intersect
    xor = poly ^ poly2
    assert sub == xor
    polygon = poly.to_polygon()
    assert type(polygon) is gui.Polygon
    poly.add_points((0, 1), core.PointF(2, 2))
    bytes(poly)


def test_polygon():
    rect1 = core.Rect(0, 0, 2, 1)
    rect2 = core.Rect(1, 0, 2, 1)
    poly = gui.Polygon(rect1, closed=True)
    poly2 = gui.Polygon(rect2, closed=True)
    intersect = poly & poly2
    expected = gui.Polygon(core.Rect(1, 0, 1, 1), closed=True)
    assert intersect == expected
    assert intersect.get_points() == [
        core.Point(1, 0),
        core.Point(2, 0),
        core.Point(2, 1),
        core.Point(1, 1),
        core.Point(1, 0),
    ]
    union = poly | poly2
    expected = gui.Polygon(core.Rect(0, 0, 3, 1), closed=True)
    assert list(union) == list(expected)
    sub = union - intersect
    xor = poly ^ poly2
    assert list(sub) == list(xor)
    # assert sub == xor
    poly = pickle_roundtrip(poly)
    poly.add_points((0, 1), core.Point(2, 2))
    assert bool(poly)
    assert core.Point(1, 0) in poly
    p = core.Point(5, 5)
    poly[5] = p
    assert poly[5] == p
    bytes(poly)


def test_region():
    region = gui.Region()
    bytes(region)


def test_regularexpressionvalidator():
    val = gui.RegularExpressionValidator()
    val.set_regex("[0-9]")
    val = pickle_roundtrip(val)
    assert val.get_regex() == "[0-9]"
    assert val.is_valid_value("0")


def test_syntaxhighlighter():
    doc = gui.TextDocument()
    gui.SyntaxHighlighter(doc)


def test_textcharformat():
    fmt = gui.TextCharFormat()
    fmt.set_font_weight("bold")
    assert fmt.get_font_weight() == "bold"
    fmt.set_foreground_color("yellow")
    fmt.set_background_color("yellow")
    with pytest.raises(InvalidParamError):
        fmt.set_font_weight("test")
    fmt = gui.TextCharFormat(bold=True)
    assert fmt.get_font_weight() == "bold"
    fmt.select_full_width()
    fmt.set_underline_style("dash")
    with pytest.raises(InvalidParamError):
        fmt.set_underline_style("test")
    assert fmt.get_underline_style() == "dash"
    fmt.set_font_style_hint("serif")
    with pytest.raises(InvalidParamError):
        fmt.set_font_style_hint("test")
    fmt.set_vertical_alignment("baseline")
    with pytest.raises(InvalidParamError):
        fmt.set_vertical_alignment("test")
    assert fmt.get_vertical_alignment() == "baseline"
    fmt.get_font()


def test_textimageformat():
    fmt = gui.TextImageFormat()
    assert bool(fmt)


def test_textlistformat():
    fmt = gui.TextListFormat()
    fmt.set_style("upper_roman")
    with pytest.raises(InvalidParamError):
        fmt.set_style("test")
    assert fmt.get_style() == "upper_roman"


def test_texttable():
    doc = gui.TextDocument()
    table = gui.TextTable(doc)
    with pytest.raises(IndexError):
        table[0, 0]
    with pytest.raises(IndexError):
        table[0]


def test_texttablecell():
    cell = gui.TextTableCell()
    assert cell
    # cell.get_format()


def test_texttableformat():
    fmt = gui.TextTableFormat()
    fmt.set_alignment("left")
    with pytest.raises(InvalidParamError):
        fmt.set_alignment("test")
    assert fmt.get_alignment() == "left"
    fmt.get_column_width_constraints()


def test_texttablecellformat():
    fmt = gui.TextTableCellFormat()
    fmt.set_bottom_border_style("dashed")
    with pytest.raises(InvalidParamError):
        fmt.set_bottom_border_style("test")
    assert fmt.get_bottom_border_style() == "dashed"

    fmt.set_left_border_style("dotted")
    with pytest.raises(InvalidParamError):
        fmt.set_left_border_style("test")
    assert fmt.get_left_border_style() == "dotted"

    fmt.set_right_border_style("solid")
    with pytest.raises(InvalidParamError):
        fmt.set_right_border_style("test")
    assert fmt.get_right_border_style() == "solid"

    fmt.set_top_border_style("double")
    with pytest.raises(InvalidParamError):
        fmt.set_top_border_style("test")
    assert fmt.get_top_border_style() == "double"

    fmt.set_border_style("groove")
    with pytest.raises(InvalidParamError):
        fmt.set_border_style("test")
    assert fmt.get_top_border_style() == "groove"

    fmt.get_bottom_border_brush()
    fmt.get_left_border_brush()
    fmt.get_right_border_brush()
    fmt.get_top_border_brush()


def test_textobject():
    doc = gui.TextDocument()
    obj = gui.TextObject(doc)
    repr(obj)
    obj.get_format()


def test_textlength():
    length = gui.TextLength()
    assert length.get_type() == "variable"
    repr(length)


def test_textframeformat():
    fmt = gui.TextFrameFormat()
    fmt.get_height()
    fmt.get_width()
    fmt.get_border_brush()
    fmt.set_border_style("dashed")
    with pytest.raises(InvalidParamError):
        fmt.set_border_style("test")
    assert fmt.get_border_style() == "dashed"
    fmt.set_page_break_policy("always_after")
    with pytest.raises(InvalidParamError):
        fmt.set_page_break_policy("test")
    assert fmt.get_page_break_policy() == "always_after"
    fmt.set_position("flow_left")
    with pytest.raises(InvalidParamError):
        fmt.set_position("test")
    assert fmt.get_position() == "flow_left"


def test_textformat():
    fmt = gui.TextFormat()
    fmt[1] = "test"
    assert fmt[1] == "test"
    assert 1 in fmt
    assert not bool(fmt)
    repr(fmt)
    fmt.get_background()
    fmt.get_foreground()
    fmt.get_brush_property(1)
    fmt.get_pen_property(1)
    fmt.get_color_property(1)
    fmt.set_layout_direction("right_to_left")
    with pytest.raises(InvalidParamError):
        fmt.set_layout_direction("test")
    assert fmt.get_layout_direction() == "right_to_left"


def test_textframe():
    doc = gui.TextDocument()
    frame = gui.TextFrame(doc)
    repr(frame)
    frame.get_first_cursor_position()
    frame.get_last_cursor_position()


def test_undocommand():
    cmd = gui.UndoCommand()
    cmd2 = gui.UndoCommand(cmd)
    assert cmd[0] == cmd2
    assert len(cmd) == 1


def test_undogroup():
    group = gui.UndoGroup()
    stack = gui.UndoStack()
    group.addStack(stack)
    assert len(group) == 1
    assert group[0] == stack


def test_undostack():
    stack = gui.UndoStack()
    cmd = stack.add_command("test", redo=lambda: print("a"), undo=lambda: print("b"))
    assert stack[0] == cmd
    assert len(stack) == 1
    with stack.create_macro("test"):
        pass


def test_window():
    wnd = gui.Window()
    assert wnd.get_surface_class() == "window"
    assert wnd.get_surface_type() == "raster"
    wnd.set_visibility("maximized")
    with pytest.raises(InvalidParamError):
        wnd.set_visibility("test")
    assert wnd.get_visibility() == "maximized"
    wnd.start_system_resize("right")
    with pytest.raises(InvalidParamError):
        wnd.start_system_resize("test")


def test_validator():
    gui.Validator()


def test_vector3d():
    vector = gui.Vector3D(0, 0, 1)
    assert abs(vector) == 1.0
    assert bool(vector)
    vector.to_point()
    vector.to_pointf()


def test_vector4d():
    vector = gui.Vector4D(0, 0, 0, 1)
    assert abs(vector) == 1.0
    assert bool(vector)
    vector.to_point()
    vector.to_pointf()
