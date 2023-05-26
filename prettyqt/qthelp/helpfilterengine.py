from __future__ import annotations

from prettyqt import core, qthelp
from prettyqt.qt import QtHelp


class HelpFilterEngine(core.ObjectMixin, QtHelp.QHelpFilterEngine):
    def get_available_versions(self) -> list[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.availableVersions()]

    def get_filter_data(self, filter_name: str) -> qthelp.HelpFilterData:
        return qthelp.HelpFilterData(self.filterData(filter_name))


if __name__ == "__main__":
    core_engine = qthelp.HelpEngineCore("test")
    engine = HelpFilterEngine(core_engine)
    print(engine.get_filter_data("a"))
