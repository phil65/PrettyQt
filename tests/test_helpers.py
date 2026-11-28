"""Tests for `prettyqt` package."""

import pytest

from prettyqt import constants
from prettyqt.utils import helpers


def test_string_to_num_array():
    assert helpers.string_to_num_array("1, 3, 5") == [1, 3, 5]
    with pytest.raises(ValueError):  # noqa: PT011
        helpers.string_to_num_array("1, 2, f")


def test_bidict_tolerates_duplicate_values():
    from prettyqt.utils import bidict

    mapping = bidict(a=constants.ALIGN_LEFT, b=constants.ALIGN_LEFT)
    assert dict(mapping) == {"a": constants.ALIGN_LEFT}
    assert mapping.inverse[constants.ALIGN_LEFT] == "a"


def test_bidict_tolerates_enum_aliases():
    import enum

    from prettyqt.utils import bidict

    class Flag(enum.IntFlag):
        none = 0
        bullet = 1
        all = 1  # alias, like AutoAll on PySide6 6.12 / Windows / Python 3.15

    mapping = bidict(none=Flag.none, bullet_list=Flag.bullet, all=Flag.all)
    assert mapping["bullet_list"] is Flag.bullet
    assert mapping.inverse[Flag.all] == "bullet_list"
    assert "all" not in mapping


def test_datatypes_to_point():
    from prettyqt import core
    from prettyqt.utils import datatypes

    assert datatypes.to_point((1, 2)) == core.QPoint(1, 2)
    assert datatypes.to_point(core.QPointF(1.4, 2.6)) == core.QPoint(1, 3)


def test_datatypes_to_keysequence_standard_key(qapp):
    from prettyqt import gui
    from prettyqt.utils import datatypes

    seq = datatypes.to_keysequence(gui.QKeySequence.StandardKey.Copy)
    assert seq == gui.QKeySequence(gui.QKeySequence.StandardKey.Copy)


@pytest.mark.parametrize("hide_ipython", [False, True])
def test_errormessagebox_tb_formatter(monkeypatch, hide_ipython):
    import sys

    from prettyqt.debugging import errormessagebox

    if hide_ipython:
        monkeypatch.setitem(sys.modules, "IPython.core.ultratb", None)
    else:
        pytest.importorskip("IPython")
    formatter = errormessagebox.get_tb_formatter()
    with pytest.raises(ValueError, match="boom") as info:
        raise ValueError("boom")
    assert "boom" in formatter(info.value, False)
    assert formatter(info.value, True).startswith("<span")


def test_colors_get_color_role(qapp):
    from prettyqt import gui
    from prettyqt.utils import colors

    assert colors.get_color("base_role") == gui.Palette().get_color("base")


def test_qtlogger_emit(qapp):
    import logging

    from prettyqt import debugging

    logger = logging.getLogger("prettyqt.test_qtlogger")
    handler = debugging.QtLogger()
    logger.addHandler(handler)
    try:
        for level in (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR):
            logger.log(level, "message")
    finally:
        logger.removeHandler(handler)


def test_event_transitions_import():
    pytest.importorskip("prettyqt.statemachine")
    from prettyqt.statemachine import keyeventtransition, mouseeventtransition

    assert keyeventtransition.KeyEventTransition()
    assert mouseeventtransition.MouseEventTransition()


def test_animated_tooltip_eventfilter(qapp):
    from prettyqt import eventfilters

    assert eventfilters.AnimatedToolTipEventFilter()


def test_iconprovider_get_icon_cache(qapp):
    from prettyqt import iconprovider

    assert iconprovider.get_icon("mdi.timer") is iconprovider.get_icon("mdi.timer")


def test_interpolate_text_colors(qapp):
    from prettyqt.utils import colors

    palette = colors.interpolate_text_colors("#1e1e1e", "#ffffff", 10)
    assert len(palette) == 10  # noqa: PLR2004
    assert all(c.isValid() for c in palette)


def test_datatypes_to_string_and_to_date(qapp):
    import datetime as dt

    from prettyqt import core
    from prettyqt.utils import datatypes

    d = dt.date(2025, 5, 1)
    assert datatypes.to_string(d) == "2025-05-01"
    dt_val = dt.datetime(2025, 5, 1, 12, 30, 0)
    assert datatypes.to_string(dt_val) == "2025-05-01 12:30:00"
    assert datatypes.to_string(slice(1, 5, 2)).endswith(")")
    qdate = datatypes.to_date(d)
    assert isinstance(qdate, core.QDate)
    assert qdate == core.QDate(2025, 5, 1)


def test_datatypes_get_editor_for_type_edge_cases(qapp):
    from prettyqt.utils import datatypes

    assert datatypes.get_editor_for_type(dict[str, int]) is None
    np = pytest.importorskip("numpy")
    assert datatypes.get_editor_for_type(np.complex128) is None


def test_node_and_base_resolver():
    from prettyqt.utils import baseresolver, node

    root = node.Node("root")
    child = node.Node("child")
    grandchild = node.Node("grandchild")
    root.append_child(child)
    child.append_child(grandchild)

    resolver = node.NodeResolver()
    assert resolver.get_parent(child) is root
    assert resolver.get_parent(root) is None
    # Verify BaseResolver.get_root directly
    assert baseresolver.BaseResolver.get_root(resolver, grandchild) is root


def test_classhelpers_fixes():
    import abc

    from prettyqt import widgets
    from prettyqt.utils import classhelpers

    class Base:
        pass

    class AbstractSub(Base, abc.ABC):
        @abc.abstractmethod
        def foo(self): ...

    class ConcreteSub(AbstractSub):
        def foo(self):
            return 1

    assert AbstractSub in list(classhelpers.get_subclasses(Base, include_abstract=True))
    assert AbstractSub not in list(
        classhelpers.get_subclasses(Base, include_abstract=False)
    )
    assert ConcreteSub in list(classhelpers.get_subclasses(Base, include_abstract=False))

    qt_parent = classhelpers.get_qt_parent_class(widgets.PushButton, only_direct=True)
    assert qt_parent is widgets.QPushButton
    assert classhelpers.get_qt_parent_class(ConcreteSub, only_direct=True) is None
    assert (
        classhelpers.find_common_ancestor([widgets.PushButton, widgets.CheckBox])
        is widgets.QAbstractButton
    )


def test_helpers_parse_time_ansi_move_in_list():
    assert helpers.parse_time("1s500ms") == 1500  # noqa: PLR2004
    for bad in ("", "abc", "10x", "1s garbage"):
        with pytest.raises(ValueError):  # noqa: PT011
            helpers.parse_time(bad)

    html = helpers.ansi2html("\033[1;3;4mhi\033[0m")
    assert "font-weight: bold" in html
    assert "font-style: italic" in html
    assert "text-decoration: underline" in html

    items = ["a", "b", "a", "c"]
    assert helpers.move_in_list(items, [0], 2) == ["b", "a", "a", "c"]


def test_bidict_merge_flags_empty():
    from prettyqt.utils import bidict

    mapping = bidict(left=constants.ALIGN_LEFT, right=constants.ALIGN_RIGHT)
    merged = mapping.merge_flags([])
    assert merged == constants.AlignmentFlag(0)


def test_texteditselecter_open_slices(qtbot):
    from prettyqt import widgets

    edit = widgets.PlainTextEdit("line0\nline1\nline2\nline3")
    qtbot.addWidget(edit)
    assert len(edit.selecter[:2]) == 3  # noqa: PLR2004
    assert len(edit.selecter[2:]) == 2  # noqa: PLR2004
    assert len(edit.selecter[:]) == 4  # noqa: PLR2004


def test_eventfilters_fixes(qtbot):
    from prettyqt import core, eventfilters, widgets

    table = widgets.TableView()
    qtbot.addWidget(table)
    auto_filter = eventfilters.AutoSizeColumnsEventFilter(table, orientation="horizontal")
    auto_filter._on_scroll()  # model is None, should not crash

    span_filter = eventfilters.SectionAutoSpanEventFilter(table)
    assert span_filter is not None

    lv = widgets.ListView()
    qtbot.addWidget(lv)
    lv.resize(10, 10)
    grid_filter = eventfilters.ListViewGridResizeEventFilter(num_columns=5, parent=lv)
    grid_filter._resize(lv)
    assert lv.gridSize().width() >= 1
    assert lv.iconSize().width() >= 1

    base = eventfilters.BaseEventFilter()

    def _raise_inside():
        with base.applied_to(lv):
            msg = "boom"
            raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="boom"):
        _raise_inside()

    lbl = widgets.Label()
    qtbot.addWidget(lbl)
    time_filter = eventfilters.TimeLabelEventFilter(lbl, interval=10000)
    unrelated_ev = core.QTimerEvent(time_filter._timer_id + 999)
    assert time_filter.eventFilter(lbl, unrelated_ev) is False


def test_iconprovider_fixes(qtbot):
    from prettyqt import core, gui, iconprovider, widgets
    from prettyqt.iconprovider import animation, chariconengine, svgbuffericonengine
    from prettyqt.qt import QtGui

    for prefix in ("fa5b.", "ri.", "msc."):
        assert prefix in iconprovider.PREFIXES

    btn = widgets.PushButton()
    qtbot.addWidget(btn)
    spin = animation.Spin(btn)
    pm = gui.QPixmap(32, 32)
    painter = QtGui.QPainter(pm)
    try:
        rect = core.QRect(0, 0, 32, 32)
        spin.setup(painter, rect)
        spin.setup(painter, rect)  # second call runs translate + rotate
    finally:
        painter.end()

    svg_xml = (
        '<svg width="16" height="16">'
        '<rect width="16" height="16" fill="currentColor"/></svg>'
    )
    engine = svgbuffericonengine.SVGBufferIconEngine(svg_xml, color="red")
    out_pm = engine.pixmap(core.QSize(16, 16), gui.QIcon.Mode.Normal, gui.QIcon.State.On)
    assert not out_pm.isNull()

    iconic = iconprovider._instance()
    char_engine = chariconengine.CharIconEngine(iconic, [])
    cloned = char_engine.clone()
    assert isinstance(cloned, chariconengine.CharIconEngine)
    assert cloned is not char_engine

    # IconicFont.paint must not mutate caller's QRect
    icon = iconic.icon("mdi.timer", offset=(0.25, 0.25))
    orig_rect = core.QRect(0, 0, 32, 32)
    pm2 = gui.QPixmap(32, 32)
    with gui.Painter(pm2) as p:
        icon.paint(p, orig_rect)
    assert orig_rect == core.QRect(0, 0, 32, 32)


def test_custom_network_fixes(qapp, monkeypatch):
    import requests

    from prettyqt.custom_network import downloadworker, update_check

    checker = update_check.UpdateChecker(app_version="1.0.0", packaged=False)
    checker.check_for_update()  # pypi_url is None -> should return cleanly without error

    class FakeResponse:
        content = b"not found"

        def raise_for_status(self):
            raise requests.HTTPError("404")

    monkeypatch.setattr(requests, "get", lambda *a, **kw: FakeResponse())
    worker = downloadworker.DownloadWorker("https://example.invalid/missing")
    failed = []
    worker.signals.download_failed.connect(lambda msg, url: failed.append((msg, url)))
    worker.run()
    assert len(failed) == 1
