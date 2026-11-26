from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtHelp


if TYPE_CHECKING:
    _HelpFilterDataBase = QtHelp.QHelpFilterData
else:
    _HelpFilterDataBase = object


class HelpFilterDataMixin(_HelpFilterDataBase):
    def get_versions(self) -> list[core.VersionNumber]:
        return [core.VersionNumber(i) for i in self.versions()]

    def set_versions(self, versions: list[core.QVersionNumber]):
        self.setVersions(versions)


class HelpFilterData(HelpFilterDataMixin):
    """Details for the filters used by QHelpFilterEngine."""

    def __init__(self, item: QtHelp.QHelpFilterData):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)


if __name__ == "__main__":
    data = HelpFilterData(QtHelp.QHelpFilterData())
    print(data.get_versions())
