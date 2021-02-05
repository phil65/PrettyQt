from __future__ import annotations

from typing import Sequence

from prettyqt import core
from prettyqt.qt import QtCore, QtHelp


class HelpFilterData(QtHelp.QHelpFilterData):
    def set_versions(self, versions: Sequence[QtCore.QVersionNumber | str]):
        versions = [core.VersionNumber(i) for i in versions]
        self.setVersions(versions)

    def get_versions(self) -> list[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.versions()]
