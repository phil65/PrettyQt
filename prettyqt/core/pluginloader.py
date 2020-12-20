from typing import List

from qtpy import QtCore

from prettyqt import core


QtCore.QPluginLoader.__bases__ = (core.Object,)


class PluginLoader(QtCore.QPluginLoader):
    def get_load_hints(self) -> List[str]:
        return [
            k
            for k, v in core.library.LOAD_HINTS.items()  # type: ignore
            if v & self.loadHints()
        ]

    def set_load_hints(self, **kwargs):
        flag = QtCore.QLibrary.LoadHint()  # type: ignore
        for k, v in kwargs.items():
            if v is True:
                flag |= core.library.LOAD_HINTS[k]  # type: ignore
        self.setLoadHints(flag)
