from __future__ import annotations

from typing import Sequence

from prettyqt import core
from prettyqt.qt import QtHelp
from prettyqt.utils import types


class HelpFilterData(QtHelp.QHelpFilterData):
    def set_versions(self, versions: Sequence[types.SemanticVersionType]):
        versions = [core.VersionNumber(i) for i in versions]
        self.setVersions(versions)

    def get_versions(self) -> list[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.versions()]
