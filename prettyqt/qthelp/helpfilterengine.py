from __future__ import annotations

from typing import List

from prettyqt import core
from prettyqt.qt import QtHelp


QtHelp.QHelpFilterEngine.__bases__ = (core.Object,)


class HelpFilterEngine(QtHelp.QHelpFilterEngine):
    def get_available_versions(self) -> List[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.availableVersions()]
