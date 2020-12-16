from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWinExtras  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWinExtras

from prettyqt import core, winextras


QtWinExtras.QWinJumpList.__bases__ = (core.Object,)


class WinJumpList(QtWinExtras.QWinJumpList):
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
