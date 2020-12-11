from typing import List

from qtpy import QtCore

from prettyqt import core


QtCore.QPluginLoader.__bases__ = (core.Object,)


class PluginLoader(QtCore.QPluginLoader):
    def get_load_hints(self) -> List[str]:
        return [k for k, v in core.library.LOAD_HINTS.items() if v & self.loadHints()]

    def set_load_hints(self, **kwargs):
        flag = QtCore.QLibrary.LoadHint(0)
        for k, v in kwargs.items():
            if v is True:
                flag |= core.library.LOAD_HINTS[k]
        self.setLoadHints(flag)
