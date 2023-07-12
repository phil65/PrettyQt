from __future__ import annotations

import contextlib
import enum
import functools
import inspect
import logging
import types

from typing import get_args

from prettyqt import constants, core, gui, itemmodels


logger = logging.getLogger(__name__)


@functools.cache
def get_comments(klass: type) -> str | None:
    return inspect.getcomments(klass)


@functools.cache
def get_doc(klass: type) -> str | None:
    return inspect.getdoc(klass)


@functools.cache
def get_file(klass: type) -> str | None:
    with contextlib.suppress(TypeError):
        return inspect.getfile(klass)


@functools.cache
def get_source(klass: type) -> str:
    return inspect.getsource(klass)


@functools.cache
def get_module(klass: type):
    return inspect.getmodule(klass).__name__


SOURCE_FONT = gui.Font.mono(as_qt=True)


class BaseClassTreeModel(itemmodels.TreeModel):
    """Base Tree Model to display class tree structures."""

    HEADER = ["Name", "Docstrings", "Module", "Comments", "File", "Is Abstract"]

    @core.Enum
    class Roles(enum.IntEnum):
        """Item roles."""

        SourceRole = constants.USER_ROLE + 1

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
        klass = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return "Union" if isinstance(klass, types.UnionType) else klass.__name__
            case constants.DISPLAY_ROLE, 1:
                return get_doc(klass)
            case constants.DISPLAY_ROLE, 2:
                return get_module(klass)
            case constants.DISPLAY_ROLE, 3:
                return get_comments(klass)
            case constants.DISPLAY_ROLE, 4:
                return get_file(klass)
            case constants.CHECKSTATE_ROLE, 5:
                return self.to_checkstate(inspect.isabstract(klass))
            case constants.USER_ROLE, _:
                return klass
            case constants.FONT_ROLE, 1 | 3:
                return SOURCE_FONT
            case self.Roles.SourceRole, _:
                return get_source(klass)


class SubClassTreeModel(BaseClassTreeModel):
    """Model to display the subclass tree of a python class.

    Also supports `types.UnionType`.
    """

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, type | types.UnionType)

    def _fetch_object_children(
        self, item: SubClassTreeModel.TreeItem
    ) -> list[SubClassTreeModel.TreeItem]:
        if isinstance(item.obj, types.UnionType):
            return [self.TreeItem(obj=i) for i in get_args(item.obj)]
        return [self.TreeItem(obj=i) for i in item.obj.__subclasses__()]

    def _has_children(self, item: SubClassTreeModel.TreeItem) -> bool:
        if item.obj is None:
            return False
        if isinstance(item.obj, types.UnionType):
            return True
        return len(item.obj.__subclasses__()) > 0


class ParentClassTreeModel(BaseClassTreeModel):
    """Tree model to display the parent class tree of a python class."""

    def __init__(self, *args, **kwargs):
        self._show_mro = False
        super().__init__(*args, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, type)

    def _fetch_object_children(
        self, item: ParentClassTreeModel.TreeItem
    ) -> list[ParentClassTreeModel.TreeItem]:
        if self._show_mro:
            return [self.TreeItem(obj=i) for i in item.obj.mro()[1:]]
        else:
            return [self.TreeItem(obj=i) for i in item.obj.__bases__]

    def _has_children(self, item: ParentClassTreeModel.TreeItem) -> bool:
        if item.obj is None:
            return False
        return len(item.obj.__bases__) > 0

    def set_show_mro(self, show: bool):
        """Toggles mro mode on or off.

        Arguments:
            show: toggle mro mode on/off
        """
        self._show_mro = show

    def get_show_mro(self) -> bool:
        """Returns True if mro mode is turned on."""
        return self._show_mro

    show_mro = core.Property(bool, get_show_mro, set_show_mro)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    model = SubClassTreeModel(core.ObjectMixin | core.Object, show_root=True, parent=view)
    view.set_model(model)
    # view.proxifier[0].modify(
    #     lambda x: gui.QColor("blue"),
    #     role=constants.BACKGROUND_ROLE,
    #     selector=lambda x: issubclass(x, core.QObject),
    #     selector_role=constants.USER_ROLE,
    # )
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("editor")
    view.resize(1000, 1000)
    view.show()
    with app.debug_mode():
        app.exec()
