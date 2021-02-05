from __future__ import annotations

from typing import Iterator

import pytest

from prettyqt import gui, qt, widgets
from prettyqt.prettyqtest import exceptions, modeltest, qt_bot, qtlogging
from prettyqt.qt import QtCore, QtWidgets


@pytest.fixture(scope="session")
def qapp_args() -> list[str]:
    """Fixture that provides QApplication arguments to use.

    You can override this fixture to pass different arguments to
    ``QApplication``:

    .. code-block:: python

       @pytest.fixture(scope="session")
       def qapp_args():
           return ["--arg"]
    """
    return []


@pytest.fixture(scope="session")
def qapp(qapp_args: list[str], pytestconfig) -> Iterator[widgets.Application]:
    app = widgets.Application(qapp_args)
    name = pytestconfig.getini("qt_qapp_name")
    app.set_metadata(
        app_name=name, app_version="1.0.0", org_name="test", org_domain="test"
    )
    yield app


@pytest.fixture
def qtbot(qapp: widgets.Application, request):
    """Fixture used to create a QtBot instance for using during testing.

    Make sure to call add_widget for each top-level widget you create to ensure
    that they are properly closed after the test ends.
    """
    result = qt_bot.QtBot(request)
    return result


@pytest.fixture
def qtlog(request):
    """Fixture that can access messages captured during testing."""
    if hasattr(request._pyfuncitem, "qt_log_capture"):
        return request._pyfuncitem.qt_log_capture
    else:
        return qtlogging._QtMessageCapture([])  # pragma: no cover


class QtTester:
    @staticmethod
    def send_keypress(widget: QtWidgets.QWidget, key):
        event = gui.KeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.KeyboardModifiers())
        widgets.Application.sendEvent(widget, event)

    @staticmethod
    def send_mousepress(widget: QtWidgets.QWidget, key):
        event = gui.MouseEvent(
            QtCore.QEvent.MouseButtonRelease,
            QtCore.QPointF(0, 0),
            QtCore.QPointF(0, 0),
            key,
            QtCore.Qt.NoButton,
            QtCore.Qt.KeyboardModifiers(),
        )
        widgets.Application.sendEvent(widget, event)

    @staticmethod
    def send_mousemove(
        widget: QtWidgets.QWidget, target: QtCore.QPointF | None = None, delay: int = 0
    ):
        if target is None:
            target = QtCore.QPointF(0, 0)
        event = gui.MouseEvent(
            QtCore.QEvent.MouseButtonRelease,
            target,
            QtCore.QPointF(0, 0),
            QtCore.Qt.NoButton,
            QtCore.Qt.NoButton,
            QtCore.Qt.KeyboardModifiers(),
        )
        widgets.Application.sendEvent(widget, event)

    @staticmethod
    def test_model(model: QtCore.QAbstractItemModel, force_py: bool = False):
        tester = modeltest.ModelTester(model)
        tester.check(force_py=force_py)
        tester._cleanup()


@pytest.fixture
def qttester() -> type[QtTester]:
    return QtTester


def pytest_addoption(parser):
    parser.addini(
        "qt_api", 'Qt api version to use: "pyside2", "pyqt5", "pyside6", "pyqt6"'
    )
    parser.addini("qt_no_exception_capture", "disable automatic exception capture")
    parser.addini(
        "qt_default_raising",
        "Default value for the raising parameter of qt_bot.wait_signal/wait_callback",
    )
    parser.addini(
        "qt_qapp_name", "The Qt application name to use", default="prettyqtest-app"
    )

    default_log_fail = qtlogging.QtLoggingPlugin.LOG_FAIL_OPTIONS[0]
    opt = qtlogging.QtLoggingPlugin.LOG_FAIL_OPTIONS
    parser.addini(
        "qt_log_level_fail",
        f'log level in which tests can fail: {opt} (default: "{default_log_fail}")',
        default=default_log_fail,
    )
    parser.addini(
        "qt_log_ignore",
        "list of regexes for messages that should not cause a tests " "to fails",
        type="linelist",
    )

    group = parser.getgroup("qt", "qt testing")
    group.addoption(
        "--no-qt-log",
        dest="qt_log",
        action="store_false",
        default=True,
        help="disable pytest-qt logging capture",
    )
    group.addoption(
        "--qt-log-format",
        dest="qt_log_format",
        default=None,
        help="defines how qt log messages are displayed.",
    )


@pytest.mark.hookwrapper
@pytest.mark.tryfirst
def pytest_runtest_setup(item):
    """Hook called after before test setup starts, to start capturing exceptions asap."""
    capture_enabled = exceptions._is_exception_capture_enabled(item)
    if capture_enabled:
        item.qt_exception_capture_manager = exceptions._QtExceptionCaptureManager()
        item.qt_exception_capture_manager.start()
    yield
    _process_events()
    if capture_enabled:
        item.qt_exception_capture_manager.fail_if_exceptions_occurred("SETUP")


@pytest.mark.hookwrapper
@pytest.mark.tryfirst
def pytest_runtest_call(item):
    yield
    _process_events()
    capture_enabled = exceptions._is_exception_capture_enabled(item)
    if capture_enabled:
        item.qt_exception_capture_manager.fail_if_exceptions_occurred("CALL")


@pytest.mark.hookwrapper
@pytest.mark.trylast
def pytest_runtest_teardown(item):
    """Hook called after each test tear down.

    Process any pending events and avoid leaking events to the next test.
    Also, if exceptions have been captured during fixtures teardown, fail the test.
    """
    _process_events()
    qt_bot._close_widgets(item)
    _process_events()
    yield
    _process_events()
    capture_enabled = exceptions._is_exception_capture_enabled(item)
    if capture_enabled:
        item.qt_exception_capture_manager.fail_if_exceptions_occurred("TEARDOWN")
        item.qt_exception_capture_manager.finish()


def _process_events():
    """Call app.processEvents() while taking care of capturing exceptions."""
    app = widgets.Application.instance()
    if app is not None:
        widgets.Application.processEvents()


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "qt_no_exception_capture: Disables pytest-qt's automatic exception "
        "capture for just one test item.",
    )

    config.addinivalue_line(
        "markers", "qt_log_level_fail: overrides qt_log_level_fail ini option."
    )
    config.addinivalue_line(
        "markers", "qt_log_ignore: overrides qt_log_ignore ini option."
    )
    config.addinivalue_line("markers", "no_qt_log: Turn off Qt logging capture.")

    if config.getoption("qt_log") and config.getoption("capture") != "no":
        config.pluginmanager.register(qtlogging.QtLoggingPlugin(config), "_qt_logging")

    # qt_api.set_qt_api(config.getini("qt_api"))

    qt_bot.QtBot._inject_qtest_methods()


def pytest_report_header() -> list[str]:
    fields = [
        f"{qt.API} {QtCore.BINDING_VERSION}",
        f"Qt runtime {str(QtCore.qVersion())}",
        f"Qt compiled {QtCore.__version__}",
    ]
    version_line = " -- ".join(fields)
    return [version_line]
