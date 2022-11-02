from __future__ import annotations

from collections.abc import Iterator
import os
from typing import Literal

from prettyqt import iconprovider
from prettyqt.qt import QtWinExtras
from prettyqt.utils import bidict, types


TYPES = bidict(
    custom=QtWinExtras.QWinJumpListCategory.Custom,
    recent=QtWinExtras.QWinJumpListCategory.Recent,
    frequent=QtWinExtras.QWinJumpListCategory.Frequent,
    tasks=QtWinExtras.QWinJumpListCategory.Tasks,
)

TypeStr = Literal["custom", "recent", "frequent", "tasks"]


class WinJumpListCategory(QtWinExtras.QWinJumpListCategory):
    def __contains__(self, item):
        return item in self.items()

    def __len__(self) -> int:
        return self.count()

    def __bool__(self):
        return not self.isEmpty()

    def __iter__(self) -> Iterator[QtWinExtras.QWinJumpListItem]:
        return iter(self.items())

    def get_type(self) -> TypeStr:
        return TYPES.inverse[self.type()]

    def add_destination(self, destination: types.PathType) -> None:
        self.addDestination(os.fspath(destination))

    def set_title(self, title: str) -> None:
        self.setTitle(title)

    def add_link(
        self,
        title: str,
        exe_path: types.PathType,
        arguments: list | None = None,
        icon: types.IconType = None,
    ) -> None:
        icon = iconprovider.get_icon(icon)
        if arguments is None:
            arguments = []
        self.addLink(icon, title, os.fspath(exe_path), arguments)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    cat = WinJumpListCategory()
    len(cat)
    app.main_loop()
