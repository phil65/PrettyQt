"""Tests for `prettyqt` package."""

import pathlib
import pickle
import tempfile

import pytest

from prettyqt import constants, core, gui, widgets
import prettyqt.qt
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


def pickle_roundtrip(something):
    path = pathlib.Path("data.pkl")
    with path.open("wb") as jar:
        pickle.dump(something, jar)
    with path.open("rb") as jar:
        return pickle.load(jar)


def test_animationgroup():
    group = core.AnimationGroup()
    anim = core.PropertyAnimation()
    anim2 = core.PropertyAnimation()
    group += anim
    group += anim2
    assert group[0] == anim
    assert group[0:2] == [anim, anim2]
    group[1] = core.PropertyAnimation()
    assert len(group) == 2  # noqa: PLR2004
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

    class Wide(core.AbstractTableModel):
        def rowCount(self, parent=None):
            return 1

        def columnCount(self, parent=None):
            return 3

    wide = Wide()
    assert wide[0, 2].column() == 2  # noqa: PLR2004
    with pytest.raises(IndexError):
        wide[0, 3]
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
    assert core.CryptographicHash.get_hash_length("sha_256") == 32  # noqa: PLR2004
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
    new = pickle_roundtrip(date)
    assert date == new


def test_datetime():
    dt = core.DateTime(2000, 11, 11, 0, 0, 0)
    new = pickle_roundtrip(dt)
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
    with tempfile.NamedTemporaryFile() as tf:
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
    doc = core.JsonDocument.from_variant([1, 2, 3])
    doc[0] = 5
    assert doc.toVariant() == [5, 2, 3]


def test_jsonvalue():
    val = core.JsonValue("b")
    assert str(val) == "b"


def test_keycombination():
    comb = core.KeyCombination("a")
    assert comb.get_key() == "a"
    event = gui.QKeyEvent(
        core.QEvent.Type.KeyPress,
        constants.Key.Key_A,
        constants.KeyboardModifier.ControlModifier,
    )
    comb = core.KeyCombination(event)
    assert comb.key() == constants.Key.Key_A
    assert comb.keyboardModifiers() == constants.KeyboardModifier.ControlModifier


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
    match line2:
        case core.Line(1, 0, 0, 0):
            pass
        case _:
            pytest.fail("Line pattern did not match")


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
    match line2:
        case core.LineF(1.0, 0.0, 0.0, 0.0):
            pass
        case _:
            pytest.fail("LineF pattern did not match")


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
    assert metaobj.get_properties(only_with_notifiers=True) is not None


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
    obj = pickle_roundtrip(obj)
    w = widgets.Splitter("horizontal")
    w1 = widgets.PushButton(object_name="w1")
    w2 = widgets.PlainTextEdit(object_name="w2")
    w3 = widgets.MainWindow(object_name="w3")
    w4 = widgets.TableView(object_name="w4")
    w.add([w1, w2, w3, w4])
    assert w.find_children(widgets.PushButton, recursive=False) == [w1]
    assert w.find_children(name="w2", recursive=False) == [w2]
    assert w.find_child(widgets.PlainTextEdit, recursive=True) == w2
    assert w.find_child(name="w2", recursive=False) == w2
    assert w2.find_parent(widgets.Splitter) == w
    layout = widgets.VBoxLayout()
    layout.add(w)

    # cannot override __init__ anymore with PySide6 6.8
    # TypeError: PySide6.QtCore.QOperatingSystemVersionBase isn't
    #  a direct base class of OperatingSystemVersion

    # def test_operatingsystemversion():
    #     os_type = core.QOperatingSystemVersion.OSType.Android
    #     version = core.OperatingSystemVersion(os_type, 11, 0, 0)
    # version2 = core.OperatingSystemVersion(os_type, 11, 0, 0)
    # assert version == version2
    # assert version.get_versionnumber() == core.VersionNumber(11, 0, 0)
    # assert version.get_type() == "android"


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
    assert len(animation) == 100  # noqa: PLR2004
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
    regex = pickle_roundtrip(regex)
    match = regex.match("123")
    assert match.span() == (0, 1)
    for _match in regex.finditer("123"):
        pass
    matches = regex.findall("123")
    assert len(matches) == 3  # noqa: PLR2004
    regex = core.RegularExpression("[0-9]+")
    assert regex.fullmatch("123") is not None
    assert regex.fullmatch("123a") is None
    assert regex.fullmatch("a123", pos=1) is not None


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
    for _, __ in settings.write_array("test", list()):
        pass
    for _ in settings.read_array("test"):
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
    assert settings["test"][0] == 1  # pyright: ignore[reportOptionalSubscript]
    assert settings["test"][1] == "b"  # pyright: ignore[reportOptionalSubscript]
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
    assert name in ["Cache", "Caches", "test"]


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
    tz = pickle_roundtrip(tz)
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


def test_locale_to_time():
    locale = core.Locale("en_US")
    assert locale.to_time("10:11", "HH:mm") == core.QTime(10, 11)


def test_operatingsystemversion_match_args():
    try:
        version = core.OperatingSystemVersion("android", 11, 2, 3)
    except TypeError:
        pytest.skip("binding cannot subclass QOperatingSystemVersion")
    match version:
        case core.OperatingSystemVersion("android", 11, 2, 3):
            pass
        case _:
            pytest.fail("OperatingSystemVersion pattern did not match")


def test_coreapplication_run_async_available():
    if not prettyqt.qt.PYSIDE6:
        pytest.skip("QtAsyncio is PySide6-only")
    from prettyqt.qt import QtAsyncio

    assert callable(QtAsyncio.run)


def test_propertyanimation_str_init():
    obj = core.Object()
    anim = core.PropertyAnimation(obj, "objectName")
    assert anim.get_property_name() == "objectName"


def test_line_and_linef_pickle():
    line = core.Line(core.Point(1, 2), core.Point(3, 4))
    restored = pickle_roundtrip(line)
    assert restored == line
    assert restored.get_p1() == core.Point(1, 2)
    assert restored.get_p2() == core.Point(3, 4)

    linef = core.LineF(core.PointF(1.5, 2.5), core.PointF(3.5, 4.5))
    restored_f = pickle_roundtrip(linef)
    assert restored_f == linef
    assert restored_f.get_p1() == core.PointF(1.5, 2.5)
    assert restored_f.get_p2() == core.PointF(3.5, 4.5)


def test_sharedmemory_pickle():
    mem = core.SharedMemory("prettyqt_test_key")
    restored = pickle_roundtrip(mem)
    assert restored.key() == "prettyqt_test_key"


def test_calendar_pickle():
    for name in ("gregorian", "julian", "islamic_civil"):
        cal = core.Calendar(name)
        restored = pickle_roundtrip(cal)
        assert restored.name() == cal.name()


def test_metatype_invalid_name():
    invalid = core.MetaType()
    assert invalid.get_name() is None or invalid.get_name() == ""
    assert repr(invalid)


def test_object_property_selector_and_bind():
    parent = core.Object()
    c1 = core.Object(parent, object_name="child1")
    c1.setProperty("a", 1)
    c1.setProperty("b", 2)
    c2 = core.Object(parent, object_name="child2")
    c2.setProperty("a", 1)
    c2.setProperty("b", 99)

    found = parent.find_children(property_selector={"a": 1, "b": 2})
    assert found == [c1]

    class Host(core.Object):
        child_a = core.ObjectMixin.bind_property(None, "child1", "a")  # type: ignore[arg-type]

    host = Host()
    sub = core.Object(host, object_name="child1")
    sub.setProperty("a", 42)
    assert host.child_a == 42  # noqa: PLR2004
    host.child_a = 100
    assert sub.property("a") == 100  # noqa: PLR2004


def test_regularexpression_fixes():
    regex = core.RegularExpression(r"(\w+)=(\d+)")
    res, count = regex.subn(r"\g<2>:\g<1>", "a=1 b=2")
    assert res == "1:a 2:b"
    assert count == 2  # noqa: PLR2004

    res2, count2 = regex.subn(r"\g<2>:\g<1>", "a=1 b=2", count=1)
    assert res2 == "1:a b=2"
    assert count2 == 1

    named = core.RegularExpression(r"(\w+)-(?P<num>\d+)")
    assert named.groupindex == {"num": 2}

    empty_re = core.RegularExpression("")
    assert empty_re.fullmatch("abc", pos=0, endpos=0) is not None

    m = regex.search("xx a=1 yy")
    assert isinstance(m, core.RegularExpressionMatch)
    assert m.group(1) == "a"
    assert m.group(2) == "1"


def test_mutex_and_semaphore_context_managers():
    mutex = core.Mutex()
    with mutex.lock_mutex(0) as acquired:
        assert acquired is True
        with mutex.lock_mutex(0) as acquired_again:
            assert acquired_again is False

    sem = core.Semaphore(1)
    with sem.acquire_resources(1) as acquired:
        assert acquired is True
        with sem.acquire_resources(1) as acquired_again:
            assert acquired_again is False
    assert sem.available() == 1


def test_sortfilterproxymodel_fixes():
    source = gui.StandardItemModel()
    source.appendRow([gui.StandardItem("alpha"), gui.StandardItem("one")])
    source.appendRow([gui.StandardItem(None), gui.StandardItem("two")])
    source.appendRow([gui.StandardItem("beta"), gui.StandardItem(None)])

    proxy = core.SortFilterProxyModel()
    proxy.setSourceModel(source)

    # lessThan strict weak ordering with None
    idx_none = source.index(1, 0)
    idx_alpha = source.index(0, 0)
    assert proxy.lessThan(idx_none, idx_none) is False
    assert proxy.lessThan(idx_none, idx_alpha) is True
    assert proxy.lessThan(idx_alpha, idx_none) is False

    # fuzzy filter with filterKeyColumn == -1 and None cells
    proxy.set_filter_mode("fuzzy")
    proxy.set_filter_key_column(-1)
    proxy.set_search_term("two")
    assert proxy.rowCount() == 1

    # substring mode
    proxy.set_filter_mode("substring")
    proxy.set_search_term("alp")
    assert proxy.rowCount() == 1


def test_abstractitemmodel_fixes():
    class Model(core.AbstractTableModel):
        def rowCount(self, parent=None):
            return 2

        def columnCount(self, parent=None):
            return 2

        def data(self, index, role=constants.DISPLAY_ROLE):
            if role == constants.CHECKSTATE_ROLE:
                return (
                    constants.CheckState.Unchecked
                    if index.row() == 0
                    else constants.CheckState.Checked
                )
            return f"{index.row()},{index.column()}"

    model = Model()
    assert model[-1].row() == 1
    assert model[-1, -1].row() == 1
    assert model[-1, -1].column() == 1
    with pytest.raises(IndexError):
        _ = model[-3]
    with pytest.raises(IndexError):
        _ = model[-3, 0]

    data, _, _ = model.get_table_data(use_checkstate_role=True)
    assert data == [[False, False], [True, True]]


def test_thread_object_mixin():
    thread = core.Thread(object_name="worker_thread")
    assert isinstance(thread, core.ObjectMixin)
    assert thread.objectName() == "worker_thread"


def test_datetime_set_time_spec_enum():
    dt = core.DateTime(2025, 1, 1, 12, 0, 0)
    dt.set_time_spec(constants.TimeSpec.UTC)
    assert dt.get_time_spec() == "utc"
    dt.set_time_spec("local_time")
    assert dt.get_time_spec() == "local_time"


def test_settings_kwargs():
    s = core.Settings("1", "2", object_name="my_settings")
    assert s.objectName() == "my_settings"


def test_update_property_group():
    with core.update_property_group():
        pass


def test_rangemodel():
    if prettyqt.qt.PYQT6:
        pytest.skip(
            "PyQt6 6.12.1 segfaults when subclassing QRangeModel with QApplication"
        )
    model = core.RangeModel([10, 20, 30])
    assert isinstance(model, core.AbstractItemModelMixin)
    assert model.rowCount() == 3  # noqa: PLR2004
    assert model.columnCount() == 1
    assert model.data(model.index(0, 0)) == 10  # noqa: PLR2004
    model.set_auto_connect_policy("full")
    assert model.get_auto_connect_policy() == "full"

    table = core.RangeModel([[1, 2], [3, 4]])
    assert table.rowCount() == 2  # noqa: PLR2004
    assert table.columnCount() == 2  # noqa: PLR2004
    assert table.data(table.index(1, 1)) == 4  # noqa: PLR2004


def test_permissions():
    perm = core.Permission()
    assert perm.get_status() == "undetermined"
    assert isinstance(perm.get_type(), core.MetaType)

    bt = core.BluetoothPermission()
    bt.set_communication_modes("access")
    assert "access" in bt.get_communication_modes()

    cal = core.CalendarPermission()
    cal.set_access_mode("read_write")
    assert cal.get_access_mode() == "read_write"

    core.CameraPermission()

    contacts = core.ContactsPermission()
    contacts.set_access_mode("read_only")
    assert contacts.get_access_mode() == "read_only"

    loc = core.LocationPermission()
    loc.set_accuracy("precise")
    assert loc.get_accuracy() == "precise"
    loc.set_availability("always")
    assert loc.get_availability() == "always"

    core.MicrophonePermission()


def test_nativeipckey():
    key = core.NativeIpcKey("my_key", "posix_realtime")
    assert bool(key) is True
    assert key.get_type() == "posix_realtime"
    assert str(key)
    key.set_type("system_v")
    assert key.get_type() == "system_v"
    parsed = core.NativeIpcKey.from_string(str(key))
    assert parsed.nativeKey() == "my_key"


def test_string_converters():
    assert core.StringConverter.get_name_for_encoding("utf8") == "UTF-8"
    enc = core.StringEncoder("utf8")
    assert bool(enc) is True
    assert enc.get_name() == "UTF-8"
    dec = core.StringDecoder("utf8")
    assert bool(dec) is True
    assert dec.get_name() == "UTF-8"
    if prettyqt.qt.PYSIDE6:
        # PyQt6 6.12.1 has a UAF/segfault in QStringDecoder.decoderForHtml
        html_dec = core.StringDecoder.for_html(b'<meta charset="utf-8"><html></html>')
        assert isinstance(html_dec, core.StringDecoder)
        assert html_dec.get_name() == "UTF-8"


def test_xmlstreamwriter():
    buf = core.Buffer()
    with buf.open_file("write_only"):
        writer = core.XmlStreamWriter(buf)
        with writer.document(), writer.element("root"):
            writer.writeTextElement("item", "value")
        assert writer.get_error() == "none"
    content = bytes(buf.data().data()).decode()
    assert "<root><item>value</item></root>" in content


def test_messageauthenticationcode():
    mac = core.MessageAuthenticationCode("sha_256", b"secret")
    mac.add_data(b"hello")
    result = mac.get_result()
    assert bytes(mac) == result
    assert result == core.MessageAuthenticationCode.compute_hash(
        b"hello", b"secret", "sha_256"
    )


def test_readwritelock():
    lock = core.ReadWriteLock("non_recursive")
    with lock.lock_for_read() as acquired:
        assert acquired is True
        with lock.lock_for_write(0) as write_acquired:
            assert write_acquired is False
    with lock.lock_for_write() as acquired:
        assert acquired is True
        with lock.lock_for_read(0) as read_acquired:
            assert read_acquired is False
