from typing import List, Union

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets


class WebEngineScriptCollection:
    def __init__(self, item: QtWebEngineWidgets.QWebEngineScriptCollection):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __getitem__(self, index: str) -> QtWebEngineWidgets.QWebEngineScript:
        return self.item.findScript(index)

    def __len__(self):
        return self.item.count()

    def __iter__(self):
        return iter(self.item.toList())

    def __contains__(self, other: QtWebEngineWidgets.QWebEngineScript):
        return self.item.contains(other)

    def __add__(
        self,
        other: Union[
            QtWebEngineWidgets.QWebEngineScript, List[QtWebEngineWidgets.QWebEngineScript]
        ],
    ):
        self.item.insert(other)
        return self


if __name__ == "__main__":
    from prettyqt import webenginewidgets, widgets

    app = widgets.app()
    page = webenginewidgets.WebEnginePage()
    scripts = page.scripts()
    script = webenginewidgets.WebEngineScript()
    script.setName("test")
    item = WebEngineScriptCollection(scripts)
    assert bool(item) is False
    item += script
    assert script in item
    assert len(item) == 1
    assert bool(item) is True
    app.main_loop()
