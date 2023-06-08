"""Tests for `prettyqt` package."""


import inspect
import pathlib
import pickle
import tempfile

import pytest

from prettyqt import constants, core, gui, widgets
import prettyqt.qt
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


clsmembers = [
    tpl
    for tpl in inspect.getmembers(core, inspect.isclass)
    if not tpl[0].startswith("Abstract")
    and not tpl[0].endswith("Mixin")
    and tpl[0] != "SignalInstance"
]


@pytest.mark.parametrize("name, cls", clsmembers)
def test_repr(name, cls):
    try:
        item = cls()
    except Exception:
        return None
    repr(item)
    str(item)


@pytest.mark.parametrize("name, cls", clsmembers)
def test_parent(name, cls):
    try:
        obj = cls()
    except Exception:
        return None
    else:
        if isinstance(obj, QtCore.QObject):
            obj.parent()


def test_animationgroup():
    group = core.AnimationGroup()
    anim = core.PropertyAnimation()
    anim2 = core.PropertyAnimation()
    group += anim
    group += anim2
    assert group[0] == anim
    assert group[0:2] == [anim, anim2]
    group[1] = core.PropertyAnimation()
    assert len(group) == 2
    del group[0]
    assert len(group) == 1


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
    model.force_reset()
    model.force_layoutchange()
    model.check_index(
        QtCore.QModelIndex(),
        index_is_valid=True,
        do_not_use_parent=True,
        parent_is_invalid=True,
    )
    # qtmodeltester.check(model, force_py=True)


def test_basictimer():
    obj = core.Object()
    timer = core.BasicTimer()
    timer.start_timer(200, obj, "coarse")
    with pytest.raises(InvalidParamError):
        timer.start_timer(200, obj, "test")
    timer.stop()


def test_buffer():
    buf = core.Buffer()
    with buf.open_file("read_only"):
        pass


def test_calendar():
    calendar = core.Calendar("gregorian")
    # assert bool(calendar) is True
    calendar.get_date_from_parts(2000, 10, 28)


# def test_commandlineoption():
#     option = core.CommandLineOption()


def test_commandlineparser():
    parser = core.CommandLineParser()
    parser.add_option("test")
    parser.set_options_after_positional_arguments_mode("options")
    with pytest.raises(InvalidParamError):
        parser.set_options_after_positional_arguments_mode("test")
    parser.set_single_dash_word_option_mode("long")
    with pytest.raises(InvalidParamError):
        parser.set_single_dash_word_option_mode("test")


def test_collator():
    collator = core.Collator()
    collator.set_case_sensitive(True)
    assert collator.is_case_sensitive()
    collator.get_locale()
    collator.get_sort_key("test")


def test_coreapplication(qapp):
    def test():
        pass

    core.CoreApplication.call_on_exit(test)


def test_cryptographichash():
    cryptohash = core.CryptographicHash("sha_1")
    assert core.CryptographicHash.get_hash_length("sha_256") == 32
    assert bytes(cryptohash) == cryptohash.get_result()


def test_datastream():
    stream = core.DataStream()
    stream.set_floating_point_precision("double")
    with pytest.raises(InvalidParamError):
        stream.set_floating_point_precision("test")
    assert stream.get_floating_point_precision() == "double"
    stream.set_byte_order("big_endian")
    with pytest.raises(InvalidParamError):
        stream.set_byte_order("test")
    assert stream.get_byte_order() == "big_endian"
    stream.set_status("read_corrupt_data")
    with pytest.raises(InvalidParamError):
        stream.set_status("test")
    assert stream.get_status() == "read_corrupt_data"


def test_date():
    date = core.Date(1, 1, 2000)
    with open("data.pkl", "wb") as jar:
        pickle.dump(date, jar)
    with open("data.pkl", "rb") as jar:
        new = pickle.load(jar)
    assert date == new


def test_datetime():
    dt = core.DateTime(2000, 11, 11, 0, 0, 0)
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
    dt.get_date()
    dt.get_time()
    dt.set_time_spec("utc")
    with pytest.raises(InvalidParamError):
        dt.set_time_spec("test")
    assert dt.get_time_spec() == "utc"


# def test_debug():
#     debug = core.Debug()
#     debug.set_verbosity("maximum")
#     with pytest.raises(InvalidParamError):
#         debug.set_verbosity("test")
#     assert debug.get_verbosity() == "maximum"


def test_deadlinetimer():
    timer = core.DeadlineTimer()
    timer.set_type("coarse")
    with pytest.raises(InvalidParamError):
        timer.set_type("test")
    assert timer.get_type() == "coarse"


def test_dir():
    directory = core.Dir()
    assert pathlib.Path(str(directory)) == directory.to_path()
    assert directory.to_path() / "test" == (directory / "test")


def test_diriterator():
    for _i in core.DirIterator(str(pathlib.Path.cwd())):
        pass


def test_elapsedtimer():
    timer = core.ElapsedTimer()
    timer.get_clock_type()
    assert bool(timer) is False


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
    tf = tempfile.NamedTemporaryFile()
    buf = core.File(tf.name)
    with buf.open_file("read_only"):
        pass
    assert buf.get_error() in ["none", "open"]


def test_fileinfo():
    info = core.FileInfo()
    info.get_dir()
    info.get_absolute_file_path()
    info.get_birth_time()
    info.get_metadata_change_time()
    info.get_last_modified()
    info.get_last_read()


def test_filesystemwatcher():
    watcher = core.FileSystemWatcher()
    watcher.add_path(core.Dir.tempPath())
    watcher.add_paths([])
    watcher.get_directories()
    watcher.get_files()
    watcher.get_paths()


def test_fileselector():
    selector = core.FileSelector()
    selector.select_path("")
    selector.select_url("")


def test_itemselection():
    selection = core.ItemSelection(core.ModelIndex(), core.ModelIndex())
    index = core.ModelIndex()
    assert index not in selection
    for _idx in selection:
        pass


def test_itemselectionrange():
    selection_range = core.ItemSelectionRange()
    # selection_range_2 = core.ItemSelectionRange()
    # selection_range_3 = selection_range & selection_range_2
    assert core.ModelIndex() in selection_range
    assert bool(selection_range) is False
    assert len(selection_range) == 0
    for _i in selection_range:
        pass


def test_jsondocument():
    doc = core.JsonDocument.from_variant(dict(a="b"))
    assert str(doc) == "{'a': 'b'}"
    doc["k"] = "v"
    assert doc["k"] == "v"
    doc.to_string()


def test_jsonvalue():
    val = core.JsonValue("b")
    assert str(val) == "b"


def test_keycombination():
    comb = core.KeyCombination("a")
    assert comb.get_key() == "a"


def test_library():
    lib = core.Library()
    assert bool(lib) is False
    lib.set_load_hints(deep_bind=True)
    assert lib.get_load_hints() == ["deep_bind"]


def test_libraryinfo():
    core.LibraryInfo.get_location("prefix")
    with pytest.raises(InvalidParamError):
        core.LibraryInfo.get_location("test")
    core.LibraryInfo.get_version()


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
    for _p in line:
        pass


def test_linef():
    line = core.LineF()
    p1 = core.PointF(0, 0)
    p2 = core.PointF(1, 0)
    line[0] = p1
    line[1] = p2
    assert line[0] == p1
    assert line[1] == p2
    assert line.get_center() == core.PointF(0.5, 0)
    line.get_normal_vector()
    line.get_unit_vector()
    line.to_line()
    line2 = core.LineF(1, 0, 0, 0)
    assert line2 == reversed(line)
    assert abs(line) == 1
    for _p in line:
        pass


def test_lockfile():
    lockfile = core.LockFile("C:/test/file.ext")
    with lockfile.lock_file():
        pass
    assert lockfile.get_error() == "unknown"


def test_margins():
    margin = core.Margins(0, 0, 0, 0)
    assert repr(margin) == "Margins(0, 0, 0, 0)"
    assert bool(margin) is False
    for _length in margin:
        pass


def test_marginsf():
    margin = core.MarginsF(0, 0, 0, 0)
    assert repr(margin) == "MarginsF(0.0, 0.0, 0.0, 0.0)"
    assert bool(margin) is False
    for _length in margin:
        pass


def test_metaenum():
    metaobj = core.AbstractItemModel.get_static_metaobject()
    enum = metaobj.get_enum(0)
    assert enum.get_name() == "LayoutChangeHint"
    assert enum.get_scope() == "QAbstractItemModel"
    assert enum.get_enum_name() == "LayoutChangeHint"
    assert enum["NoLayoutChangeHint"] == 0
    assert bool(enum) is True
    assert len(enum) > 0
    repr(enum)


def test_metamethod():
    metaobj = core.AbstractItemModel.get_static_metaobject()
    method = metaobj.get_method(0)
    assert method.get_access() == "public"
    assert method.get_method_type() == "signal"
    method.get_method_signature()
    repr(method)


def test_metaobject():
    metaobj = core.AbstractItemModel.get_static_metaobject()
    metaobj.get_enums()
    metaobj.get_constructors()
    metaobj.get_super_class()
    metaobj.get_class_info()
    with pytest.raises(KeyError):
        metaobj.get_method("test")
    with pytest.raises(KeyError):
        metaobj.get_enum("test")
    with pytest.raises(KeyError):
        metaobj.get_property("test")
    with pytest.raises(KeyError):
        metaobj.get_constructor("test")
    metaobj.get_methods()
    metaobj.get_methods(type_filter="slot")
    metaobj.get_signals()
    metaobj.get_meta_type()


def test_mimedata():
    mime_data = core.MimeData()
    mime_data.set_data("type a", "data")
    assert "type a" in mime_data
    assert mime_data.get_data("type a") == "data"
    dct = dict(a=2, b="test")
    mime_data.set_json_data("type a", dct)
    assert mime_data.get_json_data("type a") == dct
    # mime_data["test"] = "hallo"
    # assert mime_data["test"] == "hallo"
    # del mime_data["test"]
    assert len(mime_data) == 1
    assert mime_data.keys() == ["type a"]


def test_mimedatabase():
    db = core.MimeDatabase()
    db.get_mime_type_for_file("")


def test_mimetype():
    mime_type = core.MimeType()
    assert bool(mime_type) is False
    assert not str(mime_type)


def test_modelindex():
    core.ModelIndex()


def test_object(qapp):
    obj = core.Object()
    obj.set_id("test")
    with open("data.pkl", "wb") as jar:
        pickle.dump(obj, jar)
    with open("data.pkl", "rb") as jar:
        obj = pickle.load(jar)
    assert obj.get_id() == "test"
    w = widgets.Splitter("horizontal")
    w1 = widgets.PushButton()
    w1.set_id("w1")
    w2 = widgets.PlainTextEdit()
    w2.set_id("w2")
    w3 = widgets.MainWindow()
    w3.set_id("w3")
    w4 = widgets.TableView()
    w4.set_id("w4")
    w.add([w1, w2, w3, w4])
    assert w.find_children(widgets.PushButton, recursive=False) == [w1]
    assert w.find_children(name="w2", recursive=False) == [w2]
    assert w.find_child(widgets.PlainTextEdit, recursive=True) == w2
    assert w.find_child(name="w2", recursive=False) == w2
    assert w2.find_parent(widgets.Splitter) == w
    layout = widgets.VBoxLayout()
    layout.add(w)


def test_operatingsystemversion():
    version = core.OperatingSystemVersion("android", 11, 0, 0)
    version2 = core.OperatingSystemVersion("android", 11, 0, 0)
    assert version == version2
    assert version.get_versionnumber() == core.VersionNumber(11, 0, 0)
    assert version.get_type() == "android"


def test_persistentmodelindex():
    index = core.PersistentModelIndex()
    assert bool(index) is False
    assert index[constants.USER_ROLE] is None


def test_pluginloader():
    lib = core.PluginLoader()
    lib.set_load_hints(deep_bind=True)
    assert lib.get_load_hints() == ["deep_bind"]


def test_process():
    obj = core.Object()
    process = core.Process(obj)
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
    process.set_state("not_running")
    with pytest.raises(InvalidParamError):
        process.set_state("test")
    assert process.get_state() == "not_running"


def test_processenvironment():
    env = core.ProcessEnvironment.get_system_environment()
    assert bool(env) is True
    env["key"] = "value"
    assert "key" in env
    assert env["key"] == "value"
    with pytest.raises(KeyError):
        env["test"]
    del env["key"]


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
    animation.apply_to(button.geometry)
    assert animation.get_property_name() == "geometry"
    animation.setEndValue(core.Rect(20, 50, 70, 89))
    animation[0] = 1
    assert animation[0] == 1
    with pytest.raises(InvalidParamError):
        animation.start_animation("test")
    animation.start_animation("keep")

    def test(val):
        return val

    animation.set_easing(test)
    # PySide2 looses custom fn here
    if prettyqt.qt.API.startswith("pyqt"):
        assert animation.get_easing() == test
    else:
        with pytest.raises(AttributeError):
            animation.get_easing()


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
    for _i in it:
        pass


def test_regularexpression():
    regex = core.RegularExpression("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(regex, jar)
    with open("data.pkl", "rb") as jar:
        regex = pickle.load(jar)
    match = regex.match("123")
    assert match.span() == (0, 1)
    for _match in regex.finditer("123"):
        pass
    matches = regex.findall("123")
    assert len(matches) == 3


def test_resource():
    resource = core.Resource()
    bytes(resource)
    assert bool(resource) is True
    for _file in resource:
        pass
    assert resource.get_compression_algorithm() == "none"
    resource.get_absolute_file_path()
    resource.get_locale()
    resource.get_last_modified()


def test_runnable():
    core.Runnable()


def test_settings(qapp):
    settings = core.Settings("1", "2")
    settings.clear()
    settings.set_value("test", "value")
    assert settings.get("empty") is None
    assert len(settings) > 0
    assert "test" in settings
    assert settings.get("test") == "value"
    with core.Settings(settings_id="test") as s:
        s.set_value("test2", "xx")
    with settings.write_array("test"):
        pass
    with settings.read_array("test"):
        pass
    with settings.edit_group("test"):
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
    for _i in settings:
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


def test_signalmapper():
    mapper = core.SignalMapper()
    obj = core.Object()
    mapper[obj] = 10
    assert mapper[10] == obj


def test_size():
    size = core.Size(2, 2)
    assert tuple(size) == (2, 2)
    size = size.expanded_to(core.Size(4, 4))


def test_sizef():
    size = core.SizeF(2.5, 2.5)
    assert tuple(size) == (2.5, 2.5)
    size = size.expanded_to(core.SizeF(4, 4))


def test_standardpaths():
    path = core.StandardPaths.get_writable_location("cache")
    assert path is not None
    path = core.StandardPaths.get_standard_locations("cache")
    assert path != []
    name = core.StandardPaths.get_display_name("cache")
    assert name in ["Cache", "Caches"]


def test_sortfilterproxymodel():
    source_model = gui.StandardItemModel()
    model = core.SortFilterProxyModel()
    model.setSourceModel(source_model)
    model.set_sort_case_sensitive(True)
    assert model.is_sort_case_sensitive()
    model.set_sort_case_sensitive(False)

    model.set_filter_case_sensitive(True)
    assert model.is_filter_case_sensitive()
    model.set_filter_case_sensitive(False)

    model.get_filter_regular_expression()
    model.set_sort_role("display")


def storageinfo():
    info = core.StorageInfo()
    assert bool(info) is True
    info.get_device()
    info.get_file_system_type()
    info.get_subvolume()
    info.get_root_path()
    core.StorageInfo.get_root()
    core.StorageInfo.get_mounted_devices()


def test_temporarydir():
    folder = core.TemporaryDir()
    assert bool(folder) is True
    assert folder.to_path() / "test" == folder / "test"


def test_temporaryfile():
    file = core.TemporaryFile()
    with file.open_file("read_only"):
        assert file.get_open_mode() == "read_only"
    date = core.DateTime(2000, 1, 1, 1, 1, 1)
    date.set_timezone("Europe/Berlin")
    # tzinfo=datetime.timezone.utc
    # print(str(date.get_timezone()))
    file.set_file_time(date, "birth")
    # assert file.get_file_time("birth") == date.get_value()
    with pytest.raises(InvalidParamError):
        file.set_file_time(date, "test")


def test_textboundaryfinder():
    finder = core.TextBoundaryFinder("This is a test", boundary_type="word")
    for _boundary in finder:
        pass
    assert finder.get_boundary_type() == "word"
    assert "start_of_item" in finder.get_boundary_reasons()


def test_textstream():
    textstream = core.TextStream()
    textstream.set_field_alignment("accounting_style")
    assert textstream.get_field_alignment() == "accounting_style"
    with pytest.raises(InvalidParamError):
        textstream.set_field_alignment("test")
    textstream.set_status("read_past_end")
    assert textstream.get_status() == "read_past_end"
    with pytest.raises(InvalidParamError):
        textstream.set_status("test")
    textstream.set_real_number_notation("fixed")
    assert textstream.get_real_number_notation() == "fixed"
    with pytest.raises(InvalidParamError):
        textstream.set_real_number_notation("test")


def test_thread():
    core.ThreadPool()


def test_threadpool():
    core.ThreadPool()


def test_timeline():
    timeline = core.TimeLine()
    timeline.set_direction("backward")
    with pytest.raises(InvalidParamError):
        timeline.set_direction("test")
    assert timeline.get_direction() == "backward"
    assert timeline.get_state() == "not_running"


def test_timer():
    def test():
        pass

    timer = core.Timer()
    timer.set_type("coarse")
    with pytest.raises(InvalidParamError):
        timer.set_type("test")
    assert timer.get_type() == "coarse"
    timer.restart()


def test_timezone():
    tz = core.TimeZone("UTC-12:00")
    assert tz.get_id() == "UTC-12:00"
    assert str(tz) == "UTC-12:00"
    assert repr(tz) == "TimeZone('UTC-12:00')"
    with open("data.pkl", "wb") as jar:
        pickle.dump(tz, jar)
    with open("data.pkl", "rb") as jar:
        tz = pickle.load(jar)
    assert tz.get_display_name("standard") == "UTC-12:00"


def test_translator():
    translator = core.Translator()
    assert translator.get_file_path() is None
    assert bool(translator) is False


def test_url():
    path = pathlib.Path.home()
    url = core.Url(path)
    assert url == core.Url.from_local_file(path)
    # TODO: fails on Osx and linux
    # assert str(url) == str(url.to_path())
    assert url.is_local_file()


def test_urlquery():
    query = core.UrlQuery()
    query += dict(a="test", b="test2")
    assert str(query) == "a=test&b=test2"
    assert repr(query) == "UrlQuery('a=test&b=test2')"
    assert "a" in query


def test_uuid():
    uuid = core.Uuid.create_uuid()
    assert uuid.get_variant() == "dce"
    assert uuid.get_version() == "random"
    assert uuid


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
