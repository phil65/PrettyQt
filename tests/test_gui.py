#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle
import pytest
import pathlib
import inspect

from qtpy import QtCore
import qtpy

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
    gui.Brush()


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
    assert len(val) < 5
    fontmetrics.get_bounding_rect("test")
    fontmetrics.get_tight_bounding_rect("test")


def test_fontmetricsf():
    font = gui.Font("Consolas")
    fontmetrics = gui.FontMetricsF(font)
    val = fontmetrics.elided_text("This is a test", mode="right", width=40)
    with pytest.raises(InvalidParamError):
        val = fontmetrics.elided_text("This is a test", mode="test", width=40)
    assert len(val) < 5
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


def test_image():
    img = gui.Image()
    with open("data.pkl", "wb") as jar:
        pickle.dump(img, jar)
    with open("data.pkl", "rb") as jar:
        img = pickle.load(jar)


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


def test_standarditem():
    s = gui.StandardItem()
    with open("data.pkl", "wb") as jar:
        pickle.dump(s, jar)
    with open("data.pkl", "rb") as jar:
        s = pickle.load(jar)
    s.set_icon("mdi.timer")
    s.clone()


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
                painter.set_pen("test")
            with painter.backup_state():
                pass

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
    assert len(pal.get_colors()) == 11
    pal.highlight_inactive()
    pal.set_color("background", "red")
    color = gui.Color("red")
    pal["button"] = color
    assert pal["button"] == color


def test_pdfwriter():
    writer = gui.PdfWriter("test")
    writer.setup(core.RectF())


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


def test_picture():
    gui.Picture()


def test_pixmap():
    gui.Pixmap()


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
    assert union == expected
    sub = union - intersect
    xor = poly ^ poly2
    assert sub == xor
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


def test_regexpvalidator():
    val = gui.RegExpValidator()
    val.set_regex("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.get_regex() == "[0-9]"
    assert val.is_valid_value("0")


@pytest.mark.skipif(qtpy.API == "pyside2", reason="Only supported in PyQt5")
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


def test_textobject():
    doc = gui.TextDocument()
    obj = gui.TextObject(doc)
    repr(obj)
    obj.get_format()


def test_textlength():
    length = gui.TextLength()
    assert length.get_type() == "variable"
    repr(length)


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


def test_validator():
    gui.Validator()


def test_vector4d():
    vector = gui.Vector4D(0, 0, 0, 1)
    assert abs(vector) == 1.0
    assert bool(vector) is True
    vector.to_point()
    vector.to_pointf()
