from __future__ import annotations

from prettyqt import core


class SignalMapper(core.ObjectMixin, core.QSignalMapper):
    """Bundles signals from identifiable senders."""

    def __getitem__(self, index: int | str | core.QObject) -> core.QObject:
        return self.mapping(index)

    def __delitem__(self, index: core.QObject):
        return self.removeMappings(index)

    def __setitem__(self, index: core.QObject, value: int | str | core.QObject):
        self.setMapping(index, value)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.Widget()
    mapper = SignalMapper()
    mapper[widget] = 1
    del mapper[widget]
