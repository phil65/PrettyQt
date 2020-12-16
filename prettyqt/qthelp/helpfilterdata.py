from typing import List, Sequence, Union

from qtpy import QtCore, QtHelp

from prettyqt import core


class HelpFilterData(QtHelp.QHelpFilterData):
    def set_versions(self, versions: Sequence[Union[QtCore.QVersionNumber, str]]):
        versions = [core.VersionNumber(i) for i in versions]
        self.setVersions(versions)

    def get_versions(self) -> List[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.versions()]
