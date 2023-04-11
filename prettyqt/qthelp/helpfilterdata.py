from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore, QtHelp


class HelpFilterDataMixin:
    def get_versions(self) -> list[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.versions()]

    def set_versions(self, versions: list[QtCore.QVersionNumber]):
        self.setVersions(versions)


class HelpFilterData(HelpFilterDataMixin):
    def __init__(self, item: QtHelp.QHelpFilterData):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)


if __name__ == "__main__":
    data = HelpFilterData(QtHelp.QHelpFilterData())
    print(data.get_versions())
