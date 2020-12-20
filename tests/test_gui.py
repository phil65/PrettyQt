"""Tests for `prettyqt` package."""

import inspect
import pathlib
import pickle

import pytest
from qtpy import QtCore

from prettyqt import core, gui, widgets
from prettyqt.utils import InvalidParamError


clsmembers = inspect.getmembers(gui, inspect.isclass)
clsmembers = [tpl for tpl in clsmembers if not tpl[0].startswith("Abstract")]

# logger = logging.getLogger(__name__)


@pytest.mark.parametrize("name, cls", clsmembers)
def test_repr(name, cls):
    try:
        item = cls()
    except Exception:
        return None
    repr(item)


def test_brush():
    brush = gui.Brush()
    bytes(brush)


def test_clipboard(qapp):
    cb = qapp.get_clipboard()
    mimedata = QtCore.QMimeData()
    image = gui.Image()
    pixmap = gui.Pixmap()
    cb.set_mimedata(mimedata)
    cb.set_image(image)
    cb.set_pixmap(pixmap)
    assert cb.get_mimedata()
    assert cb.get_image() == image
    assert cb.get_pixmap().size() == pixmap.size()


def test_color():
    color = gui.Color()
    color.set_color("gray")
    with open("data.pkl", "wb") as jar:
        pickle.dump(color, jar)
    with open("data.pkl", "rb") as jar:
        color = pickle.load(jar)
    assert str(color) == "#808080"
    # color.as_qt()


def test_colorspace():
    space = gui.ColorSpace()
    bytes(space)
    assert bool(space) is False
    with open("data.pkl", "wb") as jar:
        pickle.dump(space, jar)
    with open("data.pkl", "rb") as jar:
        space = pickle.load(jar)
    space.set_primaries("dci_p3_d65")
    with pytest.raises(InvalidParamError):
        space.set_primaries("test")
    assert space.get_primaries() == "dci_p3_d65"
    space.set_transfer_function("pro_photo_rgb")
    with pytest.raises(InvalidParamError):
        space.set_transfer_function("test")
    assert space.get_transfer_function() == "pro_photo_rgb"


def test_cursor():
    cursor = gui.Cursor()
    cursor.set_shape("arrow")
    with pytest.raises(InvalidParamError):
        cursor.set_shape("test")
    assert cursor.get_shape() == "arrow"
    with open("data.pkl", "wb") as jar:
        pickle.dump(cursor, jar)
    with open("data.pkl", "rb") as jar:
        cursor = pickle.load(jar)
    bytes(cursor)
    cursor.get_position()


# def test_desktopservices():
#     gui.DesktopServices.open_url("test")


def test_doublevalidator():
    val = gui.DoubleValidator()
    val.setRange(0, 9)
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value("4")
    assert not val.is_valid_value("10")


def test_font():
    font = gui.Font("Consolas")
    font.metrics
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
    db = gui.FontDatabase()
    p = pathlib.Path()
    db.add_fonts_from_folder(p)
    db.get_system_font("smallest_readable")
    with pytest.raises(InvalidParamError):
        db.get_system_font("test")


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
    assert len(val) < 10
    fontmetrics.get_bounding_rect("test")
    fontmetrics.get_tight_bounding_rect("test")


def test_fontmetricsf():
    font = gui.Font("Consolas")
    fontmetrics = gui.FontMetricsF(font)
    val = fontmetrics.elided_text("This is a test", mode="right", width=40)
    with pytest.raises(InvalidParamError):
        val = fontmetrics.elided_text("This is a test", mode="test", width=40)
    assert len(val) < 10
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
    assert len(grad.get_stops()) == 2


def test_guiapplication():
    with gui.GuiApplication.override_cursor("forbidden"):
        pass


def test_icon():
    icon = gui.Icon()
    icon.for_color("black")
    with open("data.pkl", "wb") as jar:
        pickle.dump(icon, jar)
    with open("data.pkl", "rb") as jar:
        icon = pickle.load(jar)
    with pytest.raises(InvalidParamError):
        icon.get_available_sizes(mode="test")
    with pytest.raises(InvalidParamError):
        icon.get_available_sizes(state="test")
    icon.get_available_sizes()
    icon.add_pixmap(b"a")
    icon.get_actual_size((256, 256))


def test_image():
    img = gui.Image()
    with open("data.pkl", "wb") as jar:
        pickle.dump(img, jar)
    with open("data.pkl", "rb") as jar:
        img = pickle.load(jar)
    bytes(img)


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


def test_imagewriter():
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
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value("4")
    assert not val.is_valid_value("10")


def test_keysequence():
    assert gui.KeySequence.to_shortcut_str(0x41, QtCore.Qt.ShiftModifier) == "Shift+A"
    seq = gui.KeySequence("Ctrl+C")
    assert seq.get_matches("Ctrl+C") == "exact"
    with open("data.pkl", "wb") as jar:
        pickle.dump(seq, jar)
    with open("data.pkl", "rb") as jar:
        seq = pickle.load(jar)


def test_movie():
    movie = gui.Movie()
    with pytest.raises(InvalidParamError):
        movie.set_cache_mode("test")
    movie.set_cache_mode("all")
    assert movie.get_cache_mode() == "all"
    with open("data.pkl", "wb") as jar:
        pickle.dump(movie, jar)
    with open("data.pkl", "rb") as jar:
        movie = pickle.load(jar)
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


# def test_sessionmanager():
#     manager = gui.SessionManager()
#     with pytest.raises(InvalidParamError):
#         manager.set_restart_hint("test")
#     manager.set_restart_hint("immediately")
#     assert manager.get_restart_hint() == "immediately"


def test_standarditem():
    item = gui.StandardItem()
    with open("data.pkl", "wb") as jar:
        pickle.dump(item, jar)
    with open("data.pkl", "rb") as jar:
        item = pickle.load(jar)

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


def test_standarditemmodel():
    model = gui.StandardItemModel()
    model.add("test")
    for item in model:
        pass
    with open("data.pkl", "wb") as jar:
        pickle.dump(model, jar)
    with open("data.pkl", "rb") as jar:
        model = pickle.load(jar)
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
    for i in range(3):
        for j in range(3):
            assert transform[i, j] in [0, 1]
    bytes(transform)
    repr(transform)
    assert transform.get_type() == "none"
    transform = gui.Transform.clone_from(transform)


def test_textblock():
    block = gui.TextBlock()
    repr(block)
    assert 1 not in block


def test_textblockgroup():
    doc = gui.TextDocument()
    group = gui.TextBlockGroup(doc)
    repr(group)
    for textblock in group:
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
    assert len(doc) == 2
    doc.set_text("test")
    doc.clear_stacks("undo_and_redo")
    with pytest.raises(InvalidParamError):
        doc.clear_stacks("test")
    # doc.add_resource("html")
    doc.set_default_cursor_move_style("logical")
    assert doc.get_default_cursor_move_style() == "logical"
    with pytest.raises(InvalidParamError):
        doc.set_default_cursor_move_style("test")


def test_paintdevice():
    device = gui.PaintDevice()
    device.get_metric("depth")
    with pytest.raises(InvalidParamError):
        device.get_metric("test")


def test_painter():
    class Test(widgets.Widget):
        def paintEvent(self, event):
            painter = gui.Painter(self)
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
            with pytest.raises(ValueError):
                painter.fill_rect(core.Rect(), "testus")
            painter.set_color("black")
            painter.set_composition_mode("source_atop")
            painter.get_composition_mode() == "source_atop"
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


def test_openglwindow(qapp):
    wnd = gui.OpenGLWindow()
    print(bool(wnd))
    wnd.show()
    print(bool(wnd))
    assert wnd.get_update_behaviour() == "no_partial"
    wnd.grab_framebuffer()


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
    with pytest.raises(ValueError):
        size.get_definition_units()
    size = gui.PageSize(gui.PageSize.A3)
    with open("data.pkl", "wb") as jar:
        pickle.dump(size, jar)
    with open("data.pkl", "rb") as jar:
        size = pickle.load(jar)
    assert size.get_definition_units() == "millimeter"


def test_painterpath():
    path = gui.PainterPath()
    rect = core.RectF(0, 0, 1, 1)
    path.addRect(rect)
    assert len(path) == 5
    assert bool(path)
    assert core.PointF(0.5, 0.5) in path
    path[1] = (0.5, 0.5)
    path.add_rect(QtCore.QRect(0, 0, 1, 1))


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
    assert len(pal.get_colors()) == 21
    assert len(pal.get_brushes()) == 21
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
    writer.setup(core.RectF())
    writer.set_page_margins((0, 0, 0, 0), unit="pica")


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


def test_pixmap():
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
    with open("data.pkl", "wb") as jar:
        pickle.dump(poly, jar)
    with open("data.pkl", "rb") as jar:
        poly = pickle.load(jar)
    union = poly | poly2
    intersect = poly & poly2
    sub = union - intersect
    xor = poly ^ poly2
    assert sub == xor
    polygon = poly.to_polygon()
    assert type(polygon) == gui.Polygon
    poly.add_points((0, 1), core.Point(2, 2))
    bytes(poly)


def test_polygon():
    rect1 = core.Rect(0, 0, 2, 1)
    rect2 = core.Rect(1, 0, 2, 1)
    poly = gui.Polygon(rect1, closed=True)
    poly2 = gui.Polygon(rect2, closed=True)
    intersect = poly & poly2
    expected = gui.Polygon(core.Rect(1, 0, 1, 1), closed=True)
    # TODO: breaks PySide2 testing
    # assert intersect == expected
    # assert intersect.get_points() == [
    #     core.Point(1, 0),
    #     core.Point(2, 0),
    #     core.Point(2, 1),
    #     core.Point(1, 1),
    #     core.Point(1, 0),
    # ]
    union = poly | poly2
    expected = gui.Polygon(core.Rect(0, 0, 3, 1), closed=True)
    assert list(union) == list(expected)
    sub = union - intersect
    xor = poly ^ poly2
    assert list(sub) == list(xor)
    # assert sub == xor
    with open("data.pkl", "wb") as jar:
        pickle.dump(poly, jar)
    with open("data.pkl", "rb") as jar:
        poly = pickle.load(jar)
    poly.add_points((0, 1), core.Point(2, 2))
    assert bool(poly) is True
    assert core.Point(1, 0) in poly
    p = core.Point(5, 5)
    poly[5] = p
    assert poly[5] == p
    bytes(poly)


def test_region():
    region = gui.Region()
    bytes(region)


def test_regexpvalidator():
    val = gui.RegExpValidator()
    val.set_regex("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.get_regex() == "[0-9]"
    assert val.is_valid_value("0")


def test_regularexpressionvalidator():
    val = gui.RegularExpressionValidator()
    val.set_regex("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.get_regex() == "[0-9]"
    assert val.is_valid_value("0")


def test_syntaxhighlighter():
    gui.SyntaxHighlighter(None)


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
    assert bool(fmt) is True


def test_textlistformat():
    fmt = gui.TextListFormat()
    fmt.set_style("upper_roman")
    with pytest.raises(InvalidParamError):
        fmt.set_style("test")
    assert fmt.get_style() == "upper_roman"


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
    assert bool(fmt) is False
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
    assert bool(vector) is True
    vector.to_point()
    vector.to_pointf()


def test_vector4d():
    vector = gui.Vector4D(0, 0, 0, 1)
    assert abs(vector) == 1.0
    assert bool(vector) is True
    vector.to_point()
    vector.to_pointf()
