# -*- coding: utf-8 -*-
"""
"""

from typing import Union, Optional
import pathlib

try:
    from PyQt5 import QtWinExtras  # type: ignore
except ImportError:
    from PySide2 import QtWinExtras

from prettyqt import gui
from prettyqt.utils import bidict

TYPES = bidict(
    custom=QtWinExtras.QWinJumpListCategory.Custom,
    recent=QtWinExtras.QWinJumpListCategory.Recent,
    frequent=QtWinExtras.QWinJumpListCategory.Frequent,
    tasks=QtWinExtras.QWinJumpListCategory.Tasks,
)


class WinJumpListCategory(QtWinExtras.QWinJumpListCategory):
    def __contains__(self, item):
        return item in self.items()

    def __len__(self):
        return self.count()

    def __bool__(self):
        return not self.isEmpty()

    def get_type(self) -> str:
        return TYPES.inv[self.type()]

    def add_destination(self, destination: Union[str, pathlib.Path]):
        self.addDestination(str(destination))

    def set_title(self, title: str):
        self.setTitle(title)

    def add_link(
        self,
        title: str,
        exe_path: Union[str, pathlib.Path],
        arguments: Optional[list] = None,
        icon: gui.icon.IconType = None,
    ):
        icon = gui.icon.get_icon(icon)
        if arguments is None:
            arguments = []
        self.addLink(icon, title, str(exe_path), arguments)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    cat = WinJumpListCategory()
    len(cat)
    app.exec_()
