"""Tests for `prettyqt` package."""

import pytest

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError


def test_application(qapp):
    assert qapp.get_mainwindow() is None
    wnd = widgets.MainWindow()
    mw_widget = widgets.Widget()
    mw_widget.setObjectName("test")
    wnd.setCentralWidget(mw_widget)
    assert qapp.get_mainwindow() == wnd
    widget = qapp.get_widget(name="test")
    assert widget == mw_widget
    with pytest.raises(InvalidParamError):
        qapp.get_style_icon("testus")
    icon = qapp.get_style_icon("warning")
    assert isinstance(icon, QtGui.QIcon)
    qapp.set_effect_enabled("animate_toolbox")
    with pytest.raises(InvalidParamError):
        qapp.set_effect_enabled("test")
    # assert qapp.is_effect_enabled("animate_toolbox")
    # qapp.set_navigation_mode("keypad_directional")
    # with pytest.raises(InvalidParamError):
    #     qapp.set_navigation_mode("test")
    # assert qapp.get_navigation_mode("keypad_directional")
    for _widget in qapp:
        pass
    qapp.setApplicationName("testus")
    settings = core.Settings("test", "test2")
    qapp.store_widget_states(settings)
    qapp.restore_widget_states(settings)
    event = QtGui.QKeyEvent(
        QtCore.QEvent.Type.KeyPress, constants.Key.Key_Down, constants.KeyboardModifier(0)
    )
    assert qapp.send_event("test", event) is True
    qapp.post_event("test", event)
    with qapp.edit_stylesheet():
        pass


def test_guiapplication(qapp):
    qapp.set_layout_direction("right_to_left")
    with pytest.raises(InvalidParamError):
        qapp.set_layout_direction("test")
    assert qapp.get_layout_direction() == "right_to_left"
    qapp.get_font()
    qapp.get_icon()
    qapp.get_primary_screen()
    qapp.get_screens()
    qapp.get_screen_at(core.Point(1, 1))
    assert qapp.get_application_state() in [["inactive"], ["active"]]
    qapp.copy_to_clipboard("test")
    qapp.set_icon("mdi.timer")
    qapp.set_icon(None)
    qapp.set_high_dpi_scale_factor_rounding_policy("round_prefer_floor")
    with pytest.raises(InvalidParamError):
        qapp.set_high_dpi_scale_factor_rounding_policy("testus")
    assert qapp.get_high_dpi_scale_factor_rounding_policy() == "round_prefer_floor"


def test_coreapplication(qapp):
    qapp.get_application_file_path()
    expected = core.Dir.toNativeSeparators(qapp.applicationFilePath())
    assert str(qapp.get_application_file_path()) == expected
    qapp.get_application_dir_path()
    qapp.add_library_path("")
    qapp.get_library_paths()
    qapp.set_metadata(
        app_name="test", app_version="1.0.0", org_name="test", org_domain="test"
    )
    qapp.load_language("de")
    qapp.removeTranslator(qapp.translators["de"])


class _Receiver(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.threads: list[QtCore.QThread] = []

    def on_signal(self):
        self.threads.append(QtCore.QThread.currentThread())


class _Emitter(QtCore.QObject):
    fired = core.Signal()


def test_connect_passes_connection_type(qapp):
    """Application's connect wrapper must not drop the connection type."""
    receiver = _Receiver()
    emitter = _Emitter()
    emitter.fired.connect(receiver.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)
    emitter.fired.emit()
    assert receiver.threads == []  # queued: not delivered directly
    qapp.processEvents()
    assert receiver.threads == [qapp.thread()]


def test_queued_connection_from_worker_thread(qapp, qtbot):
    receiver = _Receiver()
    emitter = _Emitter()
    emitter.fired.connect(receiver.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)
    worker = QtCore.QThread()
    emitter.moveToThread(worker)
    worker.started.connect(emitter.fired.emit)
    worker.start()
    qtbot.waitUntil(lambda: len(receiver.threads) == 1, timeout=5000)
    worker.quit()
    worker.wait()
    assert receiver.threads == [qapp.thread()]


def test_coroutine_slot(qapp, qtbot):
    results = []

    async def slot():
        results.append(1)

    emitter = _Emitter()
    emitter.fired.connect(slot)
    emitter.fired.emit()
    qtbot.waitUntil(lambda: results == [1], timeout=5000)


def test_widgets_work_under_plain_qapplication():
    """Prettyqt widgets must not require prettyqt's Application."""
    import os
    import subprocess
    import sys

    code = """
from prettyqt.qt import QtWidgets
app = QtWidgets.QApplication([])
from prettyqt import widgets
assert not isinstance(app, widgets.Application)
w = widgets.Widget()
w.set_icon("mdi.timer")
w.setWindowTitle("title")
widgets.PushButton().setText("text")
import pydantic
from prettyqt.custom_widgets.pydanticform import PydanticDialog
class Model(pydantic.BaseModel):
    name: str = "x"
    count: int = 1
dlg = PydanticDialog(Model, title="Model")
dlg.show()
app.processEvents()
print("ok")
"""
    # pydantic plugins (e.g. logfire) are unrelated and may break on new Pythons
    env = dict(
        os.environ, QT_QPA_PLATFORM="offscreen", PYDANTIC_DISABLE_PLUGINS="__all__"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, env=env, timeout=60
    )
    assert result.returncode == 0, result.stderr
    assert "ok" in result.stdout
