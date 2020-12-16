# from qtpy import QtWebEngineWidgets

from typing import Iterator, List

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets

from prettyqt import webenginewidgets


class WebEngineHistory:
    def __init__(self, history: QtWebEngineWidgets.QWebEngineHistory):
        self.history = history

    def __getattr__(self, val):
        return getattr(self.history, val)

    def __len__(self):
        # pyside2 does not support len(self.history)
        return self.history.count()

    def __getitem__(self, index: int) -> webenginewidgets.WebEngineHistoryItem:
        item = self.history.itemAt(index)
        return webenginewidgets.WebEngineHistoryItem(item)

    def __iter__(self) -> Iterator[webenginewidgets.WebEngineHistoryItem]:
        items = [webenginewidgets.WebEngineHistoryItem(i) for i in self.history.items()]
        return iter(items)

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
