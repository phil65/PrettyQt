from __future__ import annotations

from prettyqt import core, qthelp


class HelpFilterEngine(core.ObjectMixin):
    """Filtered view of the help contents."""

    def __init__(self, item: qthelp.QHelpFilterEngine):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_available_versions(self) -> list[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.availableVersions()]

    def get_filter_data(self, filter_name: str) -> qthelp.HelpFilterData:
        return qthelp.HelpFilterData(self.filterData(filter_name))


if __name__ == "__main__":
    core_engine = qthelp.HelpEngineCore("test")
    engine = HelpFilterEngine(core_engine)
    print(engine.get_filter_data("a"))
