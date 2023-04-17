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
        return 0 if parent.isValid() else len(self.distributions)

    def columnCount(self, parent=core.ModelIndex()):
        return 0 if parent.isValid() else len(self.HEADER)

    def headerData(self, offset: int, orientation, role):  # type: ignore
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self.HEADER[offset]

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        dist = self.distributions[index.row()]
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return dist.metadata["Name"]
            case constants.DISPLAY_ROLE, 1:
                return dist.version
            case constants.DISPLAY_ROLE, 2:
                return dist.metadata["Summary"]
            case constants.DISPLAY_ROLE, 3:
                return dist.metadata["Home-Page"]
            case constants.DISPLAY_ROLE, 4:
                return dist.metadata["Author"]
            case constants.DISPLAY_ROLE, 5:
                return dist.metadata["License"]
            case constants.USER_ROLE, _:
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
