from __future__ import annotations

# from collections.abc import Sequence
import contextlib
import enum

from importlib import metadata
import logging
import pkgutil

from packaging.markers import Marker
from packaging.requirements import InvalidRequirement, Requirement
from typing_extensions import Self

from prettyqt import constants, core, itemmodels


logger = logging.getLogger(__name__)


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
    try:
        modules = {Requirement(i).name for i in dist.requires} if dist.requires else set()
    except ValueError as e:
        logger.error(f"{e} for {dist.name}")
        return []
    return [dist for i in modules if (dist := load_dist_info(i)) is not None]


class DistTreeItem(itemmodels.ColumnItemModel.TreeItem):
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


class DistributionColumn(itemmodels.ColumnItem):
    def get_data(self, item: ImportlibTreeModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case ImportlibTreeModel.Roles.DistributionRole:
                return item.obj


class NameColumn(DistributionColumn):
    name = "Name"
    doc = "Package name"

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["Name"]
            case _:
                return super().get_data(item, role)


class VersionColumn(DistributionColumn):
    name = "Version"
    doc = "Version number."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.version
            case _:
                return super().get_data(item, role)


class ConstraintsColumn(DistributionColumn):
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
            case _:
                return super().get_data(item, role)


class MarkerColumn(DistributionColumn):
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
            case _:
                return super().get_data(item, role)


class SummaryColumn(DistributionColumn):
    name = "Summary"
    doc = "Module description."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["Summary"]
            case _:
                return super().get_data(item, role)


class HomepageColumn(DistributionColumn):
    name = "Homepage"
    doc = "URL of the homepage."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["Home-Page"]
            case _:
                return super().get_data(item, role)


class AuthorColumn(DistributionColumn):
    name = "Author"
    doc = "Author name."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["Author"]
            case _:
                return super().get_data(item, role)


class LicenseColumn(DistributionColumn):
    name = "License"
    doc = "License name."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.metadata["License"]
            case _:
                return super().get_data(item, role)


class ImportlibTreeModel(itemmodels.ColumnItemModel):
    """Model showing the dependency tree of a distribution."""

    @core.Enum
    class Roles(enum.IntEnum):
        DistributionRole = constants.USER_ROLE + 43255

    TreeItem = DistTreeItem
    IS_RECURSIVE = True
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
    def setup_example(cls):
        from prettyqt import widgets

        model = cls("prettyqt")
        table = widgets.TreeView(word_wrap=False)
        table.set_model(model)
        table.set_delegate("render_link", column=5)
        table.expand_all(depth=4)
        return table

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

    def _has_children(self, item: ImportlibTreeModel.TreeItem) -> bool:
        return bool(item.requires)

    def _fetch_object_children(self, item: DistTreeItem) -> list[DistTreeItem]:
        return [
            DistTreeItem(obj=dist, parent=item)
            for dist in list_package_requirements(item.metadata["Name"])
        ]


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
