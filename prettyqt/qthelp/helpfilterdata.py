from typing import List, Union

from qtpy import QtHelp, QtCore

from prettyqt import core


class HelpFilterData(QtHelp.QHelpFilterData):
    def set_versions(self, versions: List[Union[QtCore.QVersionNumber, str]]):
        versions = [core.VersionNumber(i) for i in versions]
        self.setVersions(versions)

    def get_versions(self) -> List[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.versions()]
