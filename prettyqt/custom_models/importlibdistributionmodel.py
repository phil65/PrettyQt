from __future__ import annotations

from collections.abc import Sequence
from importlib import metadata
import pkgutil

from prettyqt import constants, core
from prettyqt.qt import QtCore


def load_dist_info(name: str) -> metadata.Distribution | None:
    try:
        return metadata.distribution(name)
    except metadata.PackageNotFoundError:
        return None


def list_system_modules() -> list[metadata.Distribution]:
    modules = (test.name for test in pkgutil.iter_modules())
    distributions = (load_dist_info(i) for i in modules)
    return [i for i in distributions if i is not None]


def list_package_requirements(package_name: str) -> list[metadata.Distribution]:
    dist = metadata.distribution(package_name)
    modules = (i.split(" ")[0] for i in dist.requires) if dist.requires else []
    distributions = (load_dist_info(i) for i in modules)
    return [i for i in distributions if i is not None]


class ImportlibDistributionModel(core.AbstractTableModel):

    HEADER = ["Name", "Version", "Summary", "Homepage", "Author", "License"]

    def __init__(
        self,
        distributions: Sequence[metadata.Distribution],
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)
        self.distributions = distributions

    def rowCount(self, parent=core.ModelIndex()):
        return len(self.distributions) if not parent.isValid() else 0

    def columnCount(self, parent=core.ModelIndex()):
        return len(self.HEADER) if not parent.isValid() else 0

    def headerData(self, offset: int, orientation, role):  # type: ignore
        if role == constants.DISPLAY_ROLE:
            if orientation == constants.HORIZONTAL:
                return self.HEADER[offset]

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        if role == constants.DISPLAY_ROLE:
            if index.column() == 0:
                dist = self.distributions[index.row()]
                return dist.metadata["Name"]
            elif index.column() == 1:
                dist = self.distributions[index.row()]
                return dist.version
            elif index.column() == 2:
                dist = self.distributions[index.row()]
                return dist.metadata["Summary"]
            elif index.column() == 3:
                dist = self.distributions[index.row()]
                return dist.metadata["Home-Page"]
            elif index.column() == 4:
                dist = self.distributions[index.row()]
                return dist.metadata["Author"]
            elif index.column() == 5:
                dist = self.distributions[index.row()]
                return dist.metadata["License"]
        elif role == constants.USER_ROLE:
            dist = self.distributions[index.row()]
            return dist

    @classmethod
    def from_system(
        cls, parent: QtCore.QObject | None = None
    ) -> ImportlibDistributionModel:
        distributions = list_system_modules()
        return cls(distributions, parent)

    @classmethod
    def from_package(
        cls, package_name: str, parent: QtCore.QObject | None = None
    ) -> ImportlibDistributionModel:
        distributions = list_package_requirements(package_name)
        return cls(distributions, parent)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    modules = list_system_modules()
    tableview = widgets.TableView()
    model = ImportlibDistributionModel.from_package("prettyqt")
    tableview.set_model(model)
    tableview.show()
    app.main_loop()
