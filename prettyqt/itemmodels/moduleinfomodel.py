import enum
from importlib import machinery
import logging
import os
import pathlib
import pkgutil
import types
from typing import ClassVar

from prettyqt import constants, core, itemmodels


logger = logging.getLogger(__name__)


class ModuleInfoModel(itemmodels.TreeModel):
    """Tree Model to display a module hierarchy (using pkgutil)."""

    HEADER: ClassVar = ["Name", "Path", "Is Package"]
    SUPPORTS = str | os.PathLike[str] | types.ModuleType | pkgutil.ModuleInfo

    def __init__(self, obj, **kwargs):
        match obj:
            case types.ModuleType():
                # packages have __path__, plain modules only __file__
                paths = getattr(obj, "__path__", None)
                file = paths[0] if paths else obj.__file__
                if file is None:
                    raise TypeError(obj)
                obj = _module_info_for_path(pathlib.Path(file))
            case str() | os.PathLike():
                obj = _module_info_for_path(pathlib.Path(obj))
            case pkgutil.ModuleInfo():
                pass
            case _:
                raise TypeError(obj)
        super().__init__(obj, **kwargs)

    @core.Enum
    class Roles(enum.IntEnum):
        ModuleInfoRole = constants.USER_ROLE + 2

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.HEADER[section]
        return None

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        info = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return info.name
            case constants.DISPLAY_ROLE, 1:
                return str(info.module_finder.path)
            case constants.CHECKSTATE_ROLE, 2:
                return self.to_checkstate(info.ispkg)
            case self.Roles.ModuleInfoRole, _:
                return info
        return None

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, pkgutil.ModuleInfo | types.ModuleType)

    @staticmethod
    def _get_package_path(info: pkgutil.ModuleInfo) -> str | None:
        if not info.ispkg:
            return None
        return os.path.join(info.module_finder.path, info.name)  # noqa: PTH118

    def _fetch_object_children(
        self, item: ModuleInfoModel.TreeItem
    ) -> list[ModuleInfoModel.TreeItem]:
        if (path := self._get_package_path(item.obj)) is None:
            return []
        return [self.TreeItem(obj=i) for i in pkgutil.iter_modules([path])]

    def _has_children(self, item: ModuleInfoModel.TreeItem) -> bool:
        if (path := self._get_package_path(item.obj)) is None:
            return False
        return any(True for _ in pkgutil.iter_modules([path]))


def _module_info_for_path(path: pathlib.Path) -> pkgutil.ModuleInfo:
    if path.name == "__init__.py":
        path = path.parent
    is_pkg = path.is_dir()
    name = path.name if is_pkg else path.stem
    finder = machinery.FileFinder(str(path.parent))
    return pkgutil.ModuleInfo(module_finder=finder, name=name, ispkg=is_pkg)


if __name__ == "__main__":
    import prettyqt
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    model = ModuleInfoModel(prettyqt.__path__[0], show_root=True, parent=view)
    view.set_model(model)
    view.expand_all(depth=2)
    view.resize(1000, 1000)
    view.show()
    with app.debug_mode():
        app.exec()
