"""debugging pachakge."""

from .stalker import Stalker
from .tracebackdialog import TracebackDialog
from .errormessagebox import ErrorMessageBox
from .messagehandler import MessageHandler
from .qobjectdetailsdialog import QObjectDetailsDialog

import contextlib
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


@contextlib.contextmanager
def context_timer():
    now = time.perf_counter()
    yield
    logger.info(time.perf_counter() - now)


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


def proxy_comparer(proxy: QtCore.QAbstractProxyModel):
    from prettyqt import core, custom_models, widgets

    w = widgets.Splitter("horizontal")
    while isinstance(proxy, core.QAbstractProxyModel):
        container = widgets.Widget()
        layout = container.set_layout("vertical")
        table = widgets.TableView()
        table.set_model(proxy)
        table.set_delegate("variant")
        prop_table = widgets.TableView()
        prop_table.set_delegate("variant")
        model = custom_models.WidgetPropertiesModel(proxy)
        prop_table.set_model(model)
        layout.add(widgets.Label(type(proxy).__name__))
        col_splitter = widgets.Splitter("vertical")
        col_splitter.add(prop_table)
        col_splitter.add(table)
        layout.add(col_splitter)
        w.add(container)
        proxy = proxy.sourceModel()

    container = widgets.Widget()
    layout = container.set_layout("vertical")
    table = widgets.TableView()
    table.set_model(proxy)
    table.set_delegate("variant")
    layout.add(widgets.Label(type(proxy).__name__))
    layout.add(table)
    w.add(container)
    return w


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
    table.set_model(model)
    if flatten:
        table.proxifier.flatten()
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
    table.set_delegate("variant")
    table.set_model_for(data)
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

    widget = widgets.Widget()
    layout = widget.set_layout("horizontal", object_name="main")
    with layout.get_sub_layout("splitter", orientation="horizontal") as layout:
        with layout.get_sub_layout("grid") as layout:
            layout[0, 0] = widgets.PushButton("Grid topleft")
            layout[0, 1] = widgets.RadioButton("Grid topright")
            layout[1, 0:1] = widgets.PushButton("Grid bottom")

        with layout.get_sub_layout("flow", object_name="flow") as layout:
            # with layout.get_sub_layout("frame", title="test"):
            layout += widgets.PushButton("Flow 1")
            layout += widgets.RadioButton("Flow 2")
            layout += widgets.PushButton("Flow 3")
            layout += widgets.RadioButton("Flow 4")
        layout += widgets.PlainTextEdit("Splitter middle")
        layout += widgets.PlainTextEdit("Splitter right")
        with layout.get_sub_layout("splitter", orientation="vertical") as layout:
            # with layout.get_sub_layout("frame", title="test"):
            layout += widgets.PlainTextEdit("Splitter top")
            layout += widgets.PlainTextEdit("Splitter middle")
            with layout.get_sub_layout("scroll", orientation="vertical") as layout:
                layout += widgets.PlainTextEdit("ScrollArea top")
                layout += widgets.PlainTextEdit("ScrollArea middle")
                button = layout.add(widgets.PushButton("ScrollArea Bottom"))
    with layout.get_sub_layout("horizontal", object_name="h1") as layout:
        layout += widgets.PlainTextEdit("HorizontalLayout left")
        layout += widgets.PlainTextEdit("HorizontalLayout right")
        with layout.get_sub_layout("grid") as layout2:
            layout2[0, 0] = widgets.PlainTextEdit("VerticalLayout left")
            layout2[0, 1] = widgets.PlainTextEdit("VerticalLayout right")
            layout2[1, 0:1] = example_table()
    button.clicked.connect(lambda: widget.layout().addWidget(widgets.Label("test")))
    return widget


def get_all_qt_classes():
    import importlib
    import inspect
    import PySide6

    return [
        i[1]
        for namespace in PySide6._find_all_qt_modules()
        for i in inspect.getmembers(importlib.import_module(f"PySide6.{namespace}"))
        if isinstance(i[1], type)
    ]


def get_all_qt_enums():
    import inspect
    import enum

    all_qt_enums = [
        i[1]
        for Klass in get_all_qt_classes()
        for i in inspect.getmembers(Klass)
        if isinstance(i[1], enum.EnumType)
    ]

    all_qt_enums.extend(
        [i[1] for i in inspect.getmembers(QtCore.Qt) if isinstance(i[1], enum.EnumType)]
    )
    return all_qt_enums


__all__ = [
    "Stalker",
    "TracebackDialog",
    "ErrorMessageBox",
    "MessageHandler",
    "QObjectDetailsDialog",
]
