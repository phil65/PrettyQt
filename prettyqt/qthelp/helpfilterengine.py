from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


class HelpFilterEngine(core.ObjectMixin, QtHelp.QHelpFilterEngine):
    def get_available_versions(self) -> list[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.availableVersions()]
