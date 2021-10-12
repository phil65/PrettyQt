from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWebEngineCore


class WebEngineScriptCollection:
    def __init__(self, item: QtWebEngineCore.QWebEngineScriptCollection):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __getitem__(self, index: str) -> QtWebEngineCore.QWebEngineScript:
        if core.VersionNumber.get_qt_version() < (6, 0, 0):
            return self.item.findScript(index)
        else:
            return self.item.find(index)[0]

    def __len__(self):
        return self.item.count()

    def __iter__(self):
        return iter(self.item.toList())

    def __contains__(self, other: QtWebEngineCore.QWebEngineScript):
        return self.item.contains(other)

    def __add__(
        self,
        other: (
            QtWebEngineCore.QWebEngineScript | list[QtWebEngineCore.QWebEngineScript]
        ),
    ):
        self.item.insert(other)
        return self


if __name__ == "__main__":
    from prettyqt import webenginecore, widgets

    app = widgets.app()
    page = webenginecore.WebEnginePage()
    scripts = page.scripts()
    script = webenginecore.WebEngineScript()
    script.setName("test")
    item = WebEngineScriptCollection(scripts)
    assert bool(item) is False
    item += script
    assert script in item
    assert len(item) == 1
    assert bool(item) is True
    app.main_loop()
