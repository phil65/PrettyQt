from __future__ import annotations

import contextlib
from collections.abc import Sequence
from importlib import metadata
import pkgutil
from packaging.requirements import Requirement, InvalidRequirement
from packaging.markers import Marker
from typing_extensions import Self

from prettyqt import constants, core, custom_models
from prettyqt.utils import treeitem


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
    modules = {Requirement(i).name for i in dist.requires} if dist.requires else set()
    return [dist for i in modules if (dist := load_dist_info(i)) is not None]


class DistTreeItem(treeitem.TreeItem):
    __slots__ = ("requires", "metadata", "version", "markers")

    def __init__(
        self,
        obj,
        parent: DistTreeItem | None = None,
    ):
        super().__init__(obj, parent=parent)
        self.requires = {}
        self.markers = {}
        if obj is not None and obj.requires is not None:
            for i in obj.requires:
                with contextlib.suppress(InvalidRequirement):
                    req = Requirement(i)
                    self.requires[req.name] = req
                    if ";" in i:
                        extras_str = i.split(";", maxsplit=1)[-1]
                        self.markers[req.name] = Marker(extras_str)
        # Cache the data to avoid excessive IO (obj.metadata reads file)
        self.metadata = None if obj is None else obj.metadata
        self.version = None if obj is None else obj.version


class NameColumn(custom_models.ColumnItem):
    name = "Name"
    doc = "Package name"

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["Name"]


class VersionColumn(custom_models.ColumnItem):
    name = "Version"
    doc = "Version number."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.version


class ConstraintsColumn(custom_models.ColumnItem):
    name = "Constraints"
    doc = "Constraints."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return next(
                    (
                        str(requirement.specifier)
                        for requirement in item.parent_item.requires.values()
                        if item.metadata["name"] == requirement.name
                    ),
                    "",
                )


class MarkerColumn(custom_models.ColumnItem):
    name = "Extra"
    doc = "Extra."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return next(
                    (
                        str(marker)
                        for name, marker in item.parent_item.markers.items()
                        if item.metadata["name"] == name
                    ),
                    "",
                )


class SummaryColumn(custom_models.ColumnItem):
    name = "Summary"
    doc = "Module description."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["Summary"]


class HomepageColumn(custom_models.ColumnItem):
    name = "Homepage"
    doc = "URL of the homepage."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["Home-Page"]


class AuthorColumn(custom_models.ColumnItem):
    name = "Author"
    doc = "Author name."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["Author"]


class LicenseColumn(custom_models.ColumnItem):
    name = "License"
    doc = "License name."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["License"]


class ImportlibTreeModel(custom_models.ColumnItemModel):
    """Model showing the dependency tree of a distribution.

    Attention: Model can be recursive, so be careful with iterating whole tree.
    """

    TreeItem = DistTreeItem

    COLUMNS = [
        NameColumn,
        VersionColumn,
        ConstraintsColumn,
        MarkerColumn,
        SummaryColumn,
        HomepageColumn,
        AuthorColumn,
        LicenseColumn,
    ]

    def __init__(
        self,
        obj: metadata.Distribution | str,
        show_root: bool = False,
        parent: core.QObject | None = None,
    ):
        if isinstance(obj, str):
            obj = metadata.distribution(obj)
        super().__init__(
            obj=obj, columns=self.COLUMNS, parent=parent, show_root=show_root
        )

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, metadata.Distribution)

    @classmethod
    def from_system(cls, parent: core.QObject | None = None) -> Self:
        distributions = list_system_modules()
        return cls(distributions, parent)

    @classmethod
    def from_package(cls, package_name: str, parent: core.QObject | None = None) -> Self:
        distributions = list_package_requirements(package_name)
        return cls(distributions, parent)

    def _has_children(self, item: treeitem.TreeItem) -> bool:
        return bool(item.requires)

    def _fetch_object_children(self, item: DistTreeItem) -> list[DistTreeItem]:
        return [
            DistTreeItem(obj=dist, parent=item)
            for dist in list_package_requirements(item.metadata["Name"])
        ]


class ImportlibDistributionModel(core.AbstractTableModel):
    HEADER = ["Name", "Version", "Summary", "Homepage", "Author", "License"]

    def __init__(
        self,
        distributions: Sequence[metadata.Distribution],
        parent: core.QObject | None = None,
    ):
        super().__init__(parent)
        self.distributions = distributions

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (metadata.Distribution(), *_):
                return True
            case _:
                return False

    def rowCount(self, parent=None):
        parent = parent or core.ModelIndex()
        return 0 if parent.column() > 0 or parent.isValid() else len(self.distributions)

    def columnCount(self, parent=None):
        return 0 if parent is None else len(self.HEADER)

    def headerData(
        self,
        offset: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self.HEADER[offset]

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
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
    def from_system(cls, parent: core.QObject | None = None) -> Self:
        distributions = list_system_modules()
        return cls(distributions, parent)

    @classmethod
    def from_package(cls, package_name: str, parent: core.QObject | None = None) -> Self:
        distributions = list_package_requirements(package_name)
        return cls(distributions, parent)


# if __name__ == "__main__":
#     from prettyqt import widgets

#     app = widgets.app()
#     modules = list_system_modules()
#     tableview = widgets.TableView()
#     model = ImportlibDistributionModel.from_package("prettyqt")
#     tableview.set_model(model)
#     tableview.show()
#     app.exec()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    model = ImportlibTreeModel("prettyqt")
    table = widgets.TreeView(word_wrap=False)
    # table.setSortingEnabled(True)
    table.set_model(model)
    table.set_delegate("render_link", column=5)
    table.expand_all(depth=4)
    table.show()
    app.exec()
