"""Tests for `prettyqt.debugging.inspector`."""

import json
import os
import pathlib

import pytest

from prettyqt import debugging, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


def test_ensure_offscreen(monkeypatch):
    monkeypatch.delenv("QT_QPA_PLATFORM", raising=False)
    debugging.ensure_offscreen()
    assert os.environ["QT_QPA_PLATFORM"] == "offscreen"

    monkeypatch.setenv("QT_QPA_PLATFORM", "xcb")
    debugging.ensure_offscreen()
    assert os.environ["QT_QPA_PLATFORM"] == "xcb"


def test_pump_and_wait_until(qapp):
    assert debugging.wait_until(lambda: True, timeout_ms=100, app=qapp) is True
    assert debugging.wait_until(lambda: False, timeout_ms=30, interval_ms=5) is False

    flag = [False]
    QtCore.QTimer.singleShot(25, lambda: flag.__setitem__(0, True))
    assert debugging.wait_until(lambda: flag[0], timeout_ms=1000, interval_ms=5) is True
    debugging.pump(qapp, ms=15)


def test_find_widget(qtbot):
    win = QtWidgets.QMainWindow()
    win.setObjectName("main-win")
    qtbot.addWidget(win)
    dock = QtWidgets.QDockWidget("Tools", win)
    dock.setObjectName("tools-dock")
    btn = QtWidgets.QPushButton("Go")
    btn.setObjectName("go-btn")
    dock.setWidget(btn)
    win.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)

    assert debugging.find_widget(win, "window") is win
    assert debugging.find_widget(win, "root") is win
    assert debugging.find_widget(win, "main-win") is win
    assert debugging.find_widget(win, "tools-dock") is dock
    assert debugging.find_widget(win, "go-btn") is btn
    assert debugging.find_widget(win, "does-not-exist") is None


def test_capture_writes_png(qtbot, tmp_path):
    widget = QtWidgets.QPushButton("Snapshot")
    qtbot.addWidget(widget)
    widget.resize(160, 48)
    widget.show()
    debugging.pump(ms=20)

    out_path = tmp_path / "nested" / "shot.png"
    info = debugging.capture(widget, out_path, scenario="basic", target="btn")
    dpr = widget.devicePixelRatioF()
    expected_w = round(160 * dpr)
    expected_h = round(48 * dpr)
    assert info == debugging.CaptureInfo(
        scenario="basic",
        target="btn",
        path=str(out_path),
        width=expected_w,
        height=expected_h,
    )
    assert out_path.is_file()
    img = QtGui.QImage(str(out_path))
    assert not img.isNull()
    assert (img.width(), img.height()) == (info.width, info.height)


def test_inspect_tree_clipped_label_plain_and_rich_text(qtbot):
    root = QtWidgets.QWidget()
    root.setObjectName("root")
    qtbot.addWidget(root)
    root.resize(400, 300)

    # Plain clipped label (no wordWrap)
    clipped = QtWidgets.QLabel(
        "This is an intentionally very long label that will be clipped", root
    )
    clipped.setObjectName("clipped")
    clipped.setGeometry(10, 10, 40, 24)

    # Wrapped label should NOT warn even when narrow
    wrapped = QtWidgets.QLabel(
        "This is a long label with word wrap enabled so it should not warn", root
    )
    wrapped.setObjectName("wrapped")
    wrapped.setWordWrap(True)
    wrapped.setGeometry(10, 40, 40, 60)

    # Rich text label whose HTML markup is long, but visible text ("OK") fits easily
    rich_ok = QtWidgets.QLabel(
        '<span style="font-weight: 600; color: #123456; padding: 2px;">OK</span>',
        root,
    )
    rich_ok.setObjectName("rich-ok")
    rich_ok.setGeometry(10, 110, 120, 24)

    # Rich text label whose rendered text actually overflows
    rich_clipped = QtWidgets.QLabel(
        "<b>Very long rich text heading that overflows a tiny box</b>",
        root,
    )
    rich_clipped.setObjectName("rich-clipped")
    rich_clipped.setGeometry(10, 140, 30, 24)

    root.show()
    debugging.pump(ms=20)

    lines, warnings = debugging.inspect_tree(root)
    assert any("QLabel#rich-ok" in line and 'text="OK"' in line for line in lines)
    clipped_widgets = {w.widget for w in warnings if w.kind == "clipped-label"}
    assert "QLabel#clipped" in clipped_widgets
    assert "QLabel#rich-clipped" in clipped_widgets
    assert "QLabel#wrapped" not in clipped_widgets
    assert "QLabel#rich-ok" not in clipped_widgets


def test_inspect_tree_cramped_button_and_zero_size(qtbot):
    root = QtWidgets.QWidget()
    qtbot.addWidget(root)
    root.resize(400, 200)

    cramped = QtWidgets.QPushButton("&Apply Changes Now", root)
    cramped.setObjectName("cramped-btn")
    cramped.setGeometry(10, 10, 20, 28)

    ok_btn = QtWidgets.QPushButton("&OK", root)
    ok_btn.setObjectName("ok-btn")
    ok_btn.setGeometry(10, 50, 120, 28)

    zero = QtWidgets.QWidget(root)
    zero.setObjectName("empty-box")
    zero.setGeometry(10, 90, 0, 20)

    root.show()
    debugging.pump(ms=20)

    lines, warnings = debugging.inspect_tree(root)
    assert any('text="Apply Changes Now"' in line for line in lines)
    kinds = {(w.widget, w.kind) for w in warnings}
    assert ("QPushButton#cramped-btn", "cramped-button") in kinds
    assert ("QPushButton#ok-btn", "cramped-button") not in kinds
    assert ("QWidget#empty-box", "zero-size") in kinds

    # Custom ignore_zero_size suppresses the warning
    _, filtered = debugging.inspect_tree(
        root,
        ignore_zero_size=lambda w: w.objectName() == "empty-box",
    )
    filtered_kinds = {(w.widget, w.kind) for w in filtered}
    assert ("QWidget#empty-box", "zero-size") not in filtered_kinds


def test_inspect_tree_out_of_bounds_and_false_positive_guards(qtbot):
    win = QtWidgets.QMainWindow()
    win.setObjectName("win")
    qtbot.addWidget(win)
    win.resize(500, 400)

    # ScrollArea with huge content inside viewport must NOT trigger out-of-bounds
    scroll = QtWidgets.QScrollArea(win)
    scroll.setObjectName("scroll")
    big_content = QtWidgets.QWidget()
    big_content.setObjectName("big-content")
    big_content.resize(2000, 2000)
    scroll.setWidget(big_content)
    win.setCentralWidget(scroll)

    # Tabified docks: inactive dock is parked offscreen by Qt, must NOT warn
    dock1 = QtWidgets.QDockWidget("First", win)
    dock1.setObjectName("dock-1")
    dock1.setWidget(QtWidgets.QLabel("Label inside first dock"))
    dock2 = QtWidgets.QDockWidget("Second", win)
    dock2.setObjectName("dock-2")
    dock2.setWidget(QtWidgets.QLabel("Label inside second dock"))
    win.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock1)
    win.tabifyDockWidget(dock1, dock2)
    dock2.raise_()

    # Real out-of-bounds SubWindow child (like an uncentered popup overlay)
    overlay = QtWidgets.QWidget()
    overlay.setObjectName("bad-overlay")
    overlay.setParent(win, QtCore.Qt.WindowType.SubWindow)
    overlay.setGeometry(350, 50, 300, 120)  # 350 + 300 = 650 > 500
    overlay.show()

    # Negative-offset child widget
    neg = QtWidgets.QWidget(win)
    neg.setObjectName("neg-child")
    neg.setGeometry(-20, 10, 80, 40)

    # Independent QDialog child uses screen coords, must NOT trigger out-of-bounds
    dlg = QtWidgets.QDialog(win)
    dlg.setObjectName("child-dialog")
    dlg.setGeometry(900, 900, 200, 150)

    win.show()
    dlg.show()
    debugging.pump(ms=30)

    _, warnings = debugging.inspect_tree(win)
    oob = {w.widget for w in warnings if w.kind == "out-of-bounds"}
    assert "QWidget#bad-overlay" in oob
    assert "QWidget#neg-child" in oob
    assert "QWidget#big-content" not in oob
    assert "QDockWidget#dock-1" not in oob
    assert "QDockWidget#dock-2" not in oob
    assert "QDialog#child-dialog" not in oob
    dlg.close()


def test_ui_inspector_workflow(qtbot, tmp_path):
    win = widgets.MainWindow()
    win.setObjectName("demo-win")
    qtbot.addWidget(win)
    dock = widgets.DockWidget("Info", win)
    dock.setObjectName("info-dock")
    dock.setWidget(widgets.Label("Ready"))
    win.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
    win.setCentralWidget(widgets.Label("Central"))
    win.show()

    inspector = debugging.UIInspector(win, out_dir=tmp_path)
    inspector.resize(640, 480, settle_ms=20)
    assert (win.width(), win.height()) == (640, 480)
    assert inspector.wait_until(lambda: win.isVisible(), timeout_ms=500)

    cap = inspector.capture(scenario="initial", target="window")
    assert pathlib.Path(cap.path).is_file()

    caps = inspector.capture_targets(
        ["window", "info-dock", "window", "missing"],
        scenario="multi",
    )
    assert [c.target for c in caps] == ["window", "info-dock"]
    assert all(pathlib.Path(c.path).is_file() for c in caps)

    with pytest.raises(LookupError, match="missing"):
        inspector.capture_targets(["missing"], strict=True)

    lines, warns = inspector.tree()
    assert lines[0].startswith("MainWindow#demo-win")
    assert inspector.warnings(record=True) == warns

    manifest_path = inspector.write_manifest(extra={"language": "en"})
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert data["size"] == "640x480"
    assert data["language"] == "en"
    assert len(data["captures"]) == 3  # noqa: PLR2004
    assert data["warnings"] == []
