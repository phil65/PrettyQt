"""Tests for `prettyqt.iconprovider`."""

import pytest

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.iconprovider import animation, chariconengine, svgbuffericonengine
from prettyqt.qt import QtGui


SAMPLE_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<rect width="24" height="24" fill="currentColor"/>'
    "</svg>"
)


@pytest.mark.parametrize(
    "icon_name",
    [
        "mdi.folder",
        "fa5s.adjust",
        "fa5b.500px",
        "ri.4k-fill",
        "msc.account",
        "ei.address-book",
        "ph.activity",
    ],
)
def test_get_icon_prefixes(qapp, icon_name):
    icon = iconprovider.get_icon(icon_name)
    assert isinstance(icon, gui.Icon)
    assert not icon.isNull()
    pm = icon.pixmap(16, 16)
    assert not pm.isNull()


def test_get_icon_options(qapp):
    raw_icon = iconprovider.get_icon("mdi.folder", color="red", as_qicon=True)
    assert isinstance(raw_icon, QtGui.QIcon)
    assert not raw_icon.isNull()

    wrapped = iconprovider.get_icon(raw_icon)
    assert isinstance(wrapped, gui.Icon)
    assert not wrapped.isNull()


def test_char_icon_engine_clone_and_paint(qapp):
    iconic = iconprovider._instance()
    opts = [iconic._parse_options({}, {}, "mdi.folder")]
    engine = chariconengine.CharIconEngine(iconic, opts)

    cloned = engine.clone()
    assert isinstance(cloned, chariconengine.CharIconEngine)
    assert cloned is not engine
    assert cloned.iconic is engine.iconic
    assert cloned.options == engine.options

    pm = engine.pixmap(core.QSize(24, 24), gui.QIcon.Mode.Normal, gui.QIcon.State.Off)
    assert not pm.isNull()
    assert pm.size() == core.QSize(24, 24)

    target = gui.QPixmap(24, 24)
    target.fill(gui.QColor("transparent"))
    with gui.Painter(target) as painter:
        cloned.paint(
            painter,
            core.QRect(0, 0, 24, 24),
            gui.QIcon.Mode.Normal,
            gui.QIcon.State.Off,
        )
    assert not target.isNull()


def test_svg_buffer_icon_engine(qapp):
    engine = svgbuffericonengine.SVGBufferIconEngine(SAMPLE_SVG, color="blue")
    cloned = engine.clone()
    assert isinstance(cloned, svgbuffericonengine.SVGBufferIconEngine)
    assert cloned is not engine

    engine.change_color("green")
    pm = engine.pixmap(core.QSize(24, 24), gui.QIcon.Mode.Normal, gui.QIcon.State.Off)
    assert not pm.isNull()
    assert pm.size() == core.QSize(24, 24)

    target = gui.QPixmap(24, 24)
    target.fill(gui.QColor("transparent"))
    with gui.Painter(target) as painter:
        engine.paint(
            painter,
            core.QRect(0, 0, 24, 24),
            gui.QIcon.Mode.Disabled,
            gui.QIcon.State.Off,
        )
    assert not target.isNull()


def test_spin_animation_paint_with_raw_qpainter(qtbot):
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    spin = animation.Spin(widget, interval=50, step=15)
    icon = iconprovider._icon("mdi.folder", animation=spin)

    pm = QtGui.QPixmap(32, 32)
    pm.fill(QtGui.QColor("transparent"))
    rect = core.QRect(0, 0, 32, 32)
    painter = QtGui.QPainter(pm)
    try:
        # First paint initializes the timer in spin.info
        icon.paint(painter, rect)
        assert widget in spin.info
        # Advance angle and paint again to exercise translate/rotate on raw QPainter
        spin._update()
        icon.paint(painter, rect)
    finally:
        painter.end()
        if widget in spin.info:
            spin.info[widget][0].stop()

    assert not pm.isNull()
