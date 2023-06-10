"""debugging pachakge."""

from .stalker import Stalker
from .tracebackdialog import TracebackDialog
from .errormessagebox import ErrorMessageBox
from .messagehandler import MessageHandler
from .qobjectdetailsdialog import QObjectDetailsDialog

from collections.abc import Callable
import time
import functools
import logging
from prettyqt import qt
from prettyqt.qt import QtCore


logger = logging.getLogger(__name__)


def timeit(func: Callable) -> Callable:
    @functools.wraps(func)
    def timeit_wrapper(*args, **kwargs):
        # logger.info(f'Function {func.__name__}{args} {kwargs}')
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.info(
            f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds"
        )
        return result

    return timeit_wrapper


def for_all_methods(decorator: Callable) -> Callable:
    def decorate(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                logger.info(f"decorated {attr}")
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


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


def example_table(flatten: bool = False):
    from prettyqt import widgets
    import pandas as pd

    data = dict(
        a=["abcdedf", "abcdedf", "abcdedf", "abcdedf", "abcdedf", "abcdedfaa"],
        b=[10000000, 2, 3, 4, 5, 6],
        c=[1, 2, 3, 4, 5, 6],
        d=[100000000, 2, 3, 4, 5, 6],
        e=[1000000, 2, 3, 4, 5, 6],
        f=[1000000, 2, 3, 4, 5, 6],
        g=[1, 2, 3, 4, 5, 6],
        h=[1, 2, 3, 4, 5, 6],
        i=[100000000000000, 2, 3, 4, 5, 6],
        j=[1, 2, 3, 4, 5, 6],
        k=[1, 2, 3, 4, 5, 6],
        jkfsj=[10, 20, 30, 40, 50, 60],
    )
    data = pd.DataFrame(data)
    table = widgets.TableView()
    table.set_model(data)
    return table


def example_multiindex_df():
    import pandas as pd
    import numpy as np

    tuples = [
        ("bar", "one", "q"),
        ("bar", "two", "q"),
        ("baz", "one", "q"),
        ("baz", "two", "q"),
        ("foo", "one", "q"),
        ("foo", "two", "q"),
        ("qux", "one", "q"),
        ("qux", "two", "q"),
    ] * 10
    dim = len(tuples)
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second", "third"])
    return pd.DataFrame(np.random.randn(dim, dim), index=index, columns=index)


def example_widget():
    from prettyqt import widgets

    widget = widgets.ScrollArea()
    layout = widget.set_layout("horizontal")
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


__all__ = [
    "Stalker",
    "TracebackDialog",
    "ErrorMessageBox",
    "MessageHandler",
    "QObjectDetailsDialog",
]
