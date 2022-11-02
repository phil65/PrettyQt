from __future__ import annotations

from collections.abc import Iterator

from prettyqt import core, winextras
from prettyqt.qt import QtWinExtras


QtWinExtras.QWinJumpList.__bases__ = (core.Object,)


class WinJumpList(QtWinExtras.QWinJumpList):
    def __setitem__(
        self,
        key: str,
        val: list[QtWinExtras.QWinJumpListItem] | QtWinExtras.QWinJumpListCategory,
    ):
        if isinstance(val, QtWinExtras.QWinJumpListCategory):
            self.addCategory(val)
        else:
            cat = self.add_category(key)
            for item in val:
                cat.addItem(item)

    def __getitem__(self, key: str) -> QtWinExtras.QWinJumpListCategory:
        for i in self.categories():
            if i.title() == key:
                return i
        raise KeyError(key)

    def __iter__(self) -> Iterator[QtWinExtras.QWinJumpListCategory]:
        return iter(self.categories())

    def add_category(self, title: str) -> winextras.WinJumpListCategory:
        cat = winextras.WinJumpListCategory(title)
        self.addCategory(cat)
        return cat

    def get_recent(self) -> QtWinExtras.QWinJumpListCategory:
        return self.recent()

    def get_frequent(self) -> QtWinExtras.QWinJumpListCategory:
        return self.frequent()

    def get_tasks(self) -> QtWinExtras.QWinJumpListCategory:
        return self.tasks()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    pass
    app.main_loop()
