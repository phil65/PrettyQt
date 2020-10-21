# -*- coding: utf-8 -*-

# from qtpy import QtWebEngineWidgets

from typing import Iterator, List

try:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
except ImportError:
    from PySide2 import QtWebEngineWidgets

from prettyqt import core, webenginewidgets


class WebEngineHistory(object):
    def __init__(self, history: QtWebEngineWidgets.QWebEngineHistory):
        self.history = history

    def __getattr__(self, val):
        return getattr(self.history, val)

    def __len__(self):
        return len(self.history)

    def __getitem__(self, index: int) -> webenginewidgets.WebEngineHistoryItem:
        item = self.history.itemAt(index)
        return webenginewidgets.WebEngineHistoryItem(item)

    def __iter__(self) -> Iterator[webenginewidgets.WebEngineHistoryItem]:
        items = [webenginewidgets.WebEngineHistoryItem(i) for i in self.history.items()]
        return iter(items)

    def __getstate__(self):
        return core.DataStream.create_bytearray(self.history)

    def __setstate__(self, ba):
        history = None
        core.DataStream.write_bytearray(ba, history)
        self.__init__(history)

    def get_items(self) -> List[webenginewidgets.WebEngineHistoryItem]:
        return [webenginewidgets.WebEngineHistoryItem(i) for i in self.history.items()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    page = webenginewidgets.WebEnginePage()
    page.load_url("http://www.google.de")
    page.load_url("http://www.google.com")
    history = page.history()
    item = WebEngineHistory(history)
    print(len(item))
    app.main_loop()
