from typing import List

from qtpy import QtHelp

from prettyqt import core


QtHelp.QHelpFilterEngine.__bases__ = (core.Object,)


class HelpFilterEngine(QtHelp.QHelpFilterEngine):
    def get_available_versions(self) -> List[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.availableVersions()]
