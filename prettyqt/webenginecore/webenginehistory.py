from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import webenginecore


if TYPE_CHECKING:
    from collections.abc import Iterator


class WebEngineHistory:
    def __init__(self, history: webenginecore.QWebEngineHistory):
        self.history = history

    def __getattr__(self, val):
        return getattr(self.history, val)

    def __len__(self):
        # pyside2 does not support len(self.history)
        return self.history.count()

    def __getitem__(self, index: int) -> webenginecore.WebEngineHistoryItem:
        item = self.history.itemAt(index)
        return webenginecore.WebEngineHistoryItem(item)

    def __iter__(self) -> Iterator[webenginecore.WebEngineHistoryItem]:
        items = [webenginecore.WebEngineHistoryItem(i) for i in self.history.items()]
        return iter(items)

    def get_items(self) -> list[webenginecore.WebEngineHistoryItem]:
        """Get history items."""
        return [webenginecore.WebEngineHistoryItem(i) for i in self.history.items()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    page = webenginecore.WebEnginePage()
    page.load_url("http://www.google.de")
    page.load_url("http://www.google.com")
    history = page.history()
    item = WebEngineHistory(history)
    print(len(item))
    app.exec()
