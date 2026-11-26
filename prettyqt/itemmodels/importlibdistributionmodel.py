# from collections.abc import Sequence
import contextlib
import enum
from importlib import metadata
import logging
from typing import TYPE_CHECKING, ClassVar, Self

from packaging.requirements import InvalidRequirement, Requirement
from packaging.utils import canonicalize_name

from prettyqt import constants, core, itemmodels


if TYPE_CHECKING:
    from packaging.markers import Marker


logger = logging.getLogger(__name__)


def load_dist_info(name: str) -> metadata.Distribution | None:
    try:
        return metadata.distribution(name)
    except metadata.PackageNotFoundError:
        return None


def list_system_modules() -> list[metadata.Distribution]:
    """Return all installed distributions (deduplicated by normalized name)."""
    dists: dict[str, metadata.Distribution] = {}
    for dist in metadata.distributions():
        if name := dist.metadata.get("Name"):
            dists.setdefault(canonicalize_name(name), dist)
    return sorted(dists.values(), key=lambda d: canonicalize_name(d.metadata["Name"]))


def list_package_requirements(package_name: str) -> list[metadata.Distribution]:
    dist = metadata.distribution(package_name)
    names = set()
    for req in dist.requires or []:
        with contextlib.suppress(InvalidRequirement):
            names.add(Requirement(req).name)
    return [dist for i in sorted(names) if (dist := load_dist_info(i)) is not None]


class DistTreeItem(itemmodels.ColumnItemModel.TreeItem):
    """TreeItem for a Distribution. Can also hold a list of distributions (as root)."""

    def __init__(
        self,
        obj: metadata.Distribution | list[metadata.Distribution] | None,
        parent: DistTreeItem | None = None,
    ):
        super().__init__(obj, parent=parent)
        self.requires: dict[str, Requirement] = {}
        self.markers: dict[str, Marker] = {}
        is_dist = isinstance(obj, metadata.Distribution)
        for i in (obj.requires or []) if is_dist else []:
            with contextlib.suppress(InvalidRequirement):
                req = Requirement(i)
                name = canonicalize_name(req.name)
                self.requires[name] = req
                if req.marker is not None:
                    self.markers[name] = req.marker
        # Cache the data to avoid excessive IO (obj.metadata reads file)
        self.metadata = obj.metadata if is_dist else {}
        self.version = obj.version if is_dist else None

    def get_meta(self, key: str) -> str:
        return (self.metadata.get(key) if self.metadata else None) or ""

    @property
    def canonical_name(self) -> str:
        return canonicalize_name(self.get_meta("Name"))


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
                return item.get_meta("Name")
            case _:
                return super().get_data(item, role)


class VersionColumn(DistributionColumn):
    name = "Version"
    doc = "Version number."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.version or ""
            case _:
                return super().get_data(item, role)


class ConstraintsColumn(DistributionColumn):
    name = "Constraints"
    doc = "Constraints."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                parent = item.parent_item
                if (
                    parent is None
                    or (req := parent.requires.get(item.canonical_name)) is None
                ):
                    return ""
                return str(req.specifier)
            case _:
                return super().get_data(item, role)


class MarkerColumn(DistributionColumn):
    name = "Extra"
    doc = "Extra."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                parent = item.parent_item
                if (
                    parent is None
                    or (marker := parent.markers.get(item.canonical_name)) is None
                ):
                    return ""
                return str(marker)
            case _:
                return super().get_data(item, role)


class SummaryColumn(DistributionColumn):
    name = "Summary"
    doc = "Module description."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.get_meta("Summary")
            case _:
                return super().get_data(item, role)


class HomepageColumn(DistributionColumn):
    name = "Homepage"
    doc = "URL of the homepage."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.get_meta("Home-Page")
            case _:
                return super().get_data(item, role)


class AuthorColumn(DistributionColumn):
    name = "Author"
    doc = "Author name."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.get_meta("Author")
            case _:
                return super().get_data(item, role)


class LicenseColumn(DistributionColumn):
    name = "License"
    doc = "License name."

    def get_data(self, item, role):
        match role:
            case constants.DISPLAY_ROLE:
                return item.get_meta("License")
            case _:
                return super().get_data(item, role)


class ImportlibTreeModel(itemmodels.ColumnItemModel):
    """Model showing the dependency tree of a distribution."""

    @core.Enum
    class Roles(enum.IntEnum):
        DistributionRole = constants.USER_ROLE + 43255

    SUPPORTS = metadata.Distribution | str | list[metadata.Distribution]
    TreeItem = DistTreeItem
    IS_RECURSIVE = True
    COLUMNS: ClassVar = [
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
        obj: metadata.Distribution | str | list[metadata.Distribution],
        show_root: bool = False,
        parent: core.QObject | None = None,
    ):
        """Show the requirements tree of a distribution.

        Arguments:
            obj: Distribution (or name of it). If a list of distributions is given,
                 they will be shown as top level items.
            show_root: whether to show the distribution itself as the root item.
            parent: parent QObject
        """
        if isinstance(obj, str):
            obj = metadata.distribution(obj)
        if isinstance(obj, list):
            show_root = False
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
        return cls(list_system_modules(), parent=parent)

    @classmethod
    def from_package(cls, package_name: str, parent: core.QObject | None = None) -> Self:
        return cls(list_package_requirements(package_name), parent=parent)

    def _has_children(self, item: DistTreeItem) -> bool:
        return bool(item.obj) if isinstance(item.obj, list) else bool(item.requires)

    def _fetch_object_children(self, item: DistTreeItem) -> list[DistTreeItem]:
        if isinstance(item.obj, list):
            return [DistTreeItem(obj=dist) for dist in item.obj]
        if not item.requires:
            return []
        dists = (load_dist_info(req.name) for req in item.requires.values())
        return [DistTreeItem(obj=dist) for dist in dists if dist is not None]


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
