"""debugging pachakge."""

from .stalker import Stalker
from .tracebackdialog import TracebackDialog
from .errormessagebox import ErrorMessageBox
from .messagehandler import MessageHandler


import logging
from prettyqt import qt
from prettyqt.qt import QtCore


class QtLogger(logging.Handler):
    def emit(self, record: logging.LogRecord):
        match record.level:
            case logging.DEBUG:
                QtCore.qDebug(self.format(record))
            case logging.INFO:
                QtCore.qInfo(self.format(record))
            case logging.WARNING:
                QtCore.qWarning(self.format(record))
            case logging.CRITICAL:
                QtCore.qCritical(self.format(record))
            case logging.CRITICAL:
                QtCore.qFatal(self.format(record))


def is_deleted(obj) -> bool:
    match qt.API:
        case "pyside6":
            import shiboken6

            return not shiboken6.isValid(obj)
        case "pyqt6":
            from PyQt6 import sip

            return sip.isdeleted(obj)


def example_tree(flatten: bool = False):
    from prettyqt import widgets
    from prettyqt.custom_models import JsonModel

    dist = [
        dict(
            a=2,
            b={
                "a": 4,
                "b": [1, 2, 3],
                "jkjkjk": "tekjk",
                "sggg": "tekjk",
                "fdfdf": "tekjk",
                "xxxx": "xxx",
            },
        ),
        6,
        "jkjk",
    ]
    table = widgets.TreeView()
    model = JsonModel(dist, parent=table)
    table.setRootIsDecorated(True)
    model = model.proxifier.get_proxy("flatten_tree") if flatten else model
    table.set_model(model)
    return table


def example_widget():
    from prettyqt import widgets

    widget = widgets.Widget()
    with widgets.VBoxLayout.create(widget) as layout:
        with layout.get_sub_layout("splitter", orientation="horizontal") as layout:
            layout += widgets.PlainTextEdit("upper left")
            layout += widgets.PlainTextEdit("upper middle")
            with layout.get_sub_layout("splitter", orientation="vertical") as layout:
                layout += widgets.PlainTextEdit("upper right")
                layout += widgets.PlainTextEdit("middle right")
                with layout.get_sub_layout("horizontal") as layout:
                    layout += widgets.PlainTextEdit("upper right")
                    layout += widgets.PlainTextEdit("middle right")
                    button = layout.add(widgets.PushButton("test"))
        with layout.get_sub_layout("horizontal") as layout:
            layout += widgets.PlainTextEdit("lower left")
            layout += widgets.PlainTextEdit("lower right")

    button.clicked.connect(lambda: widget.layout().addWidget(widgets.Label("test")))
    return widget


__all__ = ["Stalker", "TracebackDialog", "ErrorMessageBox", "MessageHandler"]
