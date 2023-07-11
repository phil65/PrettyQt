from __future__ import annotations

from prettyqt import core


class PluginLoader(core.ObjectMixin, core.QPluginLoader):
    """Load a plugin at runtime."""

    def get_load_hints(self) -> list[core.library.LoadHintStr]:
        return core.library.LOAD_HINTS.get_list(self.loadHints())

    def set_load_hints(self, **kwargs):
        flag = core.QLibrary.LoadHint(0)  # type: ignore
        for k, v in kwargs.items():
            if v is True:
                flag |= core.library.LOAD_HINTS[k]  # type: ignore
        self.setLoadHints(flag)  # type: ignore
