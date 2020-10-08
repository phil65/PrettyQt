#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import sys
import pathlib
import pickle

import pytest

from qtpy import QtCore
from prettyqt import core, widgets
from prettyqt.utils import InvalidParamError


def test_animationgroup():
    group = core.AnimationGroup()
    anim = core.PropertyAnimation()
    anim2 = core.PropertyAnimation()
    group += anim
    group += anim2
    assert group[0] == anim
    assert len(group) == 2
    del group[0]
    assert len(group) == 1
    group[1] = core.PropertyAnimation()


def test_abstracttablemodel():
    class Test(core.AbstractTableModel):
        def rowCount(self, parent=None):
            return 0

        def columnCount(self, parent=None):
            return 0

    model = Test()
    assert model.rowCount() == 0
    assert model.columnCount() == 0
    with model.change_layout():
        pass
    with model.reset_model():
        pass
    with model.remove_rows():
        pass
    with model.remove_columns():
        pass
    with model.insert_rows():
        pass
    with model.append_rows(1):
        pass
    with model.insert_columns():
        pass
    # qtmodeltester.check(model, force_py=True)


def test_buffer():
    buf = core.Buffer()
    with buf.open_file("read_only"):
        pass


def test_coreapplication(qapp):
    def test():
        pass

    core.CoreApplication.call_on_exit(test)


def test_datastream():
    stream = core.DataStream()
    stream.set_float_precision("double")
    with pytest.raises(InvalidParamError):
        stream.set_float_precision("test")
    assert stream.get_float_precision() == "double"
    stream.set_byte_order("big_endian")
    with pytest.raises(InvalidParamError):
        stream.set_byte_order("test")
    assert stream.get_byte_order() == "big_endian"


def test_date():
    date = core.Date(1, 1, 2000)
    with open("data.pkl", "wb") as jar:
        pickle.dump(date, jar)
    with open("data.pkl", "rb") as jar:
        new = pickle.load(jar)
    assert date == new


def test_datetime():
    date = core.Date(2000, 11, 11)
    dt = core.DateTime(date)
    with open("data.pkl", "wb") as jar:
        pickle.dump(dt, jar)
    with open("data.pkl", "rb") as jar:
        new = pickle.load(jar)
    assert dt == new
    dt.set_timezone("Europe/Berlin")
    tz = core.TimeZone("Europe/Berlin")
    dt.set_timezone(tz)
    assert dt.get_timezone() == tz
    assert dt.to_format("iso") == "2000-11-11T00:00:00+01:00"
    repr(dt)
    dt.get_date()
    dt.get_time()
    dt.set_time_spec("utc")
    with pytest.raises(InvalidParamError):
        dt.set_time_spec("test")
    assert dt.get_time_spec() == "utc"


def test_dir():
    directory = core.Dir()
    assert pathlib.Path(str(directory)) == directory.to_path()
    assert directory.to_path() / "test" == (directory / "test").to_path()
    repr(directory)


def test_diriterator():
    for i in core.DirIterator(str(pathlib.Path.cwd())):
        pass


def test_easingcurve():
    c = core.EasingCurve()
    c.set_type("in_cubic")
    assert c.get_type() == "in_cubic"
    assert c[0] == 0
    assert c[1] == 1

    def custom(val):
        return 1

    c.set_custom_type(custom)
    assert c.get_custom_type() == custom
    assert c.get_type() == "custom"
    with pytest.raises(InvalidParamError):
        c.set_type("test")


def test_file():
    buf = core.File()
    with buf.open_file("read_only"):
        pass
    str(buf)
    repr(buf)


def test_historystate():
    state = core.HistoryState()
    state.set_history_type("deep")
    assert state.get_history_type() == "deep"
    with pytest.raises(InvalidParamError):
        state.set_history_type("test")


def test_line():
    line = core.Line()
    p1 = core.Point(0, 0)
    p2 = core.Point(1, 0)
    line[0] = p1
    line[1] = p2
    assert line[0] == p1
    assert line[1] == p2
    line2 = core.Line(1, 0, 0, 0)
    assert line2 == reversed(line)
    assert abs(line) == 1
    repr(line)
    for p in line:
        pass


def test_linef():
    line = core.LineF()
    p1 = core.PointF(0, 0)
    p2 = core.PointF(1, 0)
    line[0] = p1
    line[1] = p2
    assert line[0] == p1
    assert line[1] == p2
    line2 = core.LineF(1, 0, 0, 0)
    assert line2 == reversed(line)
    assert abs(line) == 1
    repr(line)
    for p in line:
        pass


def test_mimedata():
    mime_data = core.MimeData()
    mime_data.set_data("type a", "data")
    assert "type a" in mime_data
    assert mime_data.get_data("type a") == "data"
    dct = dict(a=2, b="test")
    mime_data.set_json_data("type a", dct)
    assert mime_data.get_json_data("type a") == dct
    mime_data["test"] = "hallo"
    assert mime_data["test"] == "hallo"
    del mime_data["test"]
    assert len(mime_data) == 1
    assert mime_data.keys() == ["type a"]


def test_modelindex():
    core.ModelIndex()


def test_object(qapp):
    obj = core.Object()
    obj.set_id("test")
    with open("data.pkl", "wb") as jar:
        pickle.dump(obj, jar)
    with open("data.pkl", "rb") as jar:
        obj = pickle.load(jar)
    assert obj.id == "test"
    w = widgets.Splitter("horizontal")
    w1 = widgets.PushButton()
    w1.set_id("w1")
    w2 = widgets.PlainTextEdit()
    w2.set_id("w2")
    w3 = widgets.MainWindow()
    w3.set_id("w3")
    w4 = widgets.TableView()
    w4.set_id("w4")
    w.add(w1, w2, w3, w4)
    assert w.find_children(widgets.PushButton, recursive=False) == [w1]
    assert w.find_children(core.Object, name="w2", recursive=False) == [w2]
    assert w.find_child(widgets.PlainTextEdit, recursive=True) == w2
    assert w.find_child(core.Object, name="w2", recursive=False) == w2
    assert w2.find_parent(widgets.Splitter) == w
    layout = widgets.BoxLayout("vertical")
    layout.add(w)
    layout.store_widget_states()
    layout.restore_widget_states()


def test_point():
    p = core.Point()
    repr(p)


def test_pointf():
    p = core.PointF()
    repr(p)


def test_process():
    process = core.Process()
    process.set_read_channel("error")
    with pytest.raises(InvalidParamError):
        process.set_read_channel("test")
    assert process.get_read_channel() == "error"
    process.set_input_channel_mode("forwarded")
    with pytest.raises(InvalidParamError):
        process.set_input_channel_mode("test")
    assert process.get_input_channel_mode() == "forwarded"
    process.set_process_channel_mode("forwarded_error")
    with pytest.raises(InvalidParamError):
        process.set_process_channel_mode("test")
    assert process.get_process_channel_mode() == "forwarded_error"
    process.set_state("starting")
    with pytest.raises(InvalidParamError):
        process.set_state("test")
    assert process.get_state() == "starting"


def test_propertyanimation():
    animation = core.PropertyAnimation()
    button = widgets.PushButton()
    animation.set_easing("in_cubic")
    assert animation.get_easing() == "in_cubic"
    animation.set_direction("forward")
    with pytest.raises(InvalidParamError):
        animation.set_direction("test")
    assert animation.get_direction() == "forward"
    assert animation.get_state() == "stopped"
    animation.setDuration(100)
    assert len(animation) == 100
    animation.apply_to(button, "geometry")
    assert animation.get_property_name() == "geometry"
    with pytest.raises(InvalidParamError):
        animation.start_animation("test")
    animation.start_animation("keep")
    animation[0] = 1
    assert animation[0] == 1

    def test(val):
        return val

    animation.set_easing(test)
    assert animation.get_easing() == test


def test_rect():
    rect = core.Rect()
    repr(rect)


def test_rectf():
    rect = core.RectF()
    repr(rect)


def test_regexp():
    regex = core.RegExp("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(regex, jar)
    with open("data.pkl", "rb") as jar:
        regex = pickle.load(jar)
    repr(regex)


def test_regularexpressionmatch():
    match = core.RegularExpressionMatch()
    match.group()
    match.groups()
    match.groupdict()
    match.start()
    match.end()
    match.span()
    assert match.pos is None
    assert match.endpos is None


def test_regularexpressionmatchiterator():
    it = core.RegularExpressionMatchIterator()
    for i in it:
        pass


def test_regularexpression():
    regex = core.RegularExpression("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(regex, jar)
    with open("data.pkl", "rb") as jar:
        regex = pickle.load(jar)
    repr(regex)
    match = regex.match("123")
    assert match.span() == (0, 1)
    for match in regex.finditer("123"):
        pass
    matches = regex.findall("123")
    assert len(matches) == 3


def test_runnable():
    core.Runnable()


def test_settings(qapp):
    settings = core.Settings("1", "2")
    settings.clear()
    settings.set_value("test", "value")
    assert settings.get("empty") is None
    assert len(settings) == 1
    assert "test" in settings
    assert settings.get("test") == "value"
    with core.Settings(settings_id="test") as s:
        s.set_value("test2", "xx")
    with settings.write_array("test"):
        pass
    with settings.read_array("test"):
        pass
    with settings.group("test"):
        pass
    with pytest.raises(KeyError):
        del settings["some value"]
    with pytest.raises(KeyError):
        settings.pop("some value2")
    settings["test2"] = "xyz"
    assert settings["test2"] == "xyz"
    settings.setdefault("test3", "abc")
    assert settings.get("test3") == "abc"
    del settings["test3"]
    path = pathlib.Path.cwd()
    for i in settings:
        pass
    settings["test"] = True
    assert settings["test"] is True
    settings["test"] = "test"
    assert settings["test"] == "test"
    settings["test"] = dict(a="b")
    assert settings["test"] == dict(a="b")
    settings["test"] = (1, "b")
    assert settings["test"] == (1, "b")
    settings["test"] = QtCore.QByteArray(b"test")
    assert settings["test"] == QtCore.QByteArray(b"test")
    settings["test"] = b"test"
    assert settings["test"] == b"test"

    settings.set_default_format("ini")
    assert settings.get_default_format() == "ini"
    with pytest.raises(InvalidParamError):
        settings.set_default_format("ino")
    assert settings.get_scope() == "user"
    settings.set_path("native", "user", path)
    with pytest.raises(InvalidParamError):
        settings.set_path("error", "user", path)
    with pytest.raises(InvalidParamError):
        settings.set_path("native", "error", path)
    s = core.Settings.build_from_dict(dict(a="b"))
    repr(s)


def test_signaltransition():
    trans = core.SignalTransition()
    trans.set_transition_type("parallel")
    assert trans.get_transition_type() == "parallel"
    with pytest.raises(InvalidParamError):
        trans.set_transition_type("test")


def test_size():
    size = core.Size()
    repr(size)


def test_sizef():
    size = core.SizeF()
    repr(size)


def test_standardpaths():
    path = core.StandardPaths.get_writable_location("cache")
    assert path is not None
    path = core.StandardPaths.get_standard_locations("cache")
    assert path != []
    if sys.version_info >= (3, 7):
        path = core.StandardPaths["cache"]
        assert path != []
    name = core.StandardPaths.get_display_name("cache")
    assert name == "Cache"


def test_state():
    state = core.State()
    state.set_child_mode("parallel")
    assert state.get_child_mode() == "parallel"
    with pytest.raises(InvalidParamError):
        state.set_child_mode("test")


def test_sortfilterproxymodel():
    core.SortFilterProxyModel()


def test_textboundaryfinder():
    finder = core.TextBoundaryFinder("This is a test", boundary_type="word")
    for boundary in finder:
        pass
    repr(finder)
    assert finder.get_boundary_type() == "word"
    assert finder.get_boundary_reasons() == ["break_opportunity", "start_of_item"]


def test_thread():
    core.ThreadPool()


def test_threadpool():
    core.ThreadPool()


def test_timer():
    def test():
        pass

    core.Timer.single_shot(test)
    timer = core.Timer()
    timer.set_type("coarse")
    with pytest.raises(InvalidParamError):
        timer.set_type("test")
    assert timer.get_type() == "coarse"


def test_timezone():
    tz = core.TimeZone("UTC-12:00")
    assert tz.get_id() == "UTC-12:00"
    assert str(tz) == "UTC-12:00"
    assert repr(tz) == "TimeZone('UTC-12:00')"
    with open("data.pkl", "wb") as jar:
        pickle.dump(tz, jar)
    with open("data.pkl", "rb") as jar:
        tz = pickle.load(jar)


def test_translator():
    core.Translator()


def test_url():
    path = pathlib.Path.home()
    url = core.Url(path)
    assert str(url) == str(url.to_path())
    assert url.is_local_file()
    repr(url)


def test_urlquery():
    query = core.UrlQuery()
    query += dict(a="test", b="test2")
    assert str(query) == "a=test&b=test2"
    assert repr(query) == "UrlQuery('a=test&b=test2')"
    assert "a" in query


def test_versionnumber():
    a = core.VersionNumber(1, 2, 3)
    b = core.VersionNumber("1.2.4")
    c = core.VersionNumber((1, 2, 5))
    assert a < b
    assert b <= c
    assert a == str(a)
    assert c > b
    assert b >= a
    assert a < str(b)
    assert b <= str(c)
    assert c > str(b)
    assert b >= str(a)
    assert repr(a) == "VersionNumber(1, 2, 3)"
    assert core.VersionNumber.get_qt_version() > (5, 12, 0)
    assert core.VersionNumber.get_python_version() > (3, 6, 0)
