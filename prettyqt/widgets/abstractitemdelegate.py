from __future__ import annotations

import logging

from prettyqt import constants, core
from prettyqt.qt import QtWidgets


logger = logging.getLogger(__name__)


class AbstractItemDelegateMixin(core.ObjectMixin):
    pass
    # this pattern doesnt work for PySide6 yet (cant pass kwargs for class definition)
    # _registry = {}

    # def __init_subclass__(cls, identifier=None, **kwargs):
    #     super().__init_subclass__(**kwargs)
    #     if identifier is not None:
    #         logger.debug(f"registering delegate {cls} {identifier!r}")
    #         if (
    #             identifier in cls._registry
    #             and cls._registry[identifier].__name__ != cls.__name__
    #         ):
    #             raise NameError(f"Delegate with id {identifier!r} already registered.")
    #         cls._registry[identifier] = cls

    @staticmethod
    def _data_for_index(
        index: core.ModelIndex, role: constants.ItemDataRole = constants.USER_ROLE
    ):
        # using index.data() sometimes casts stuff in PyQt6
        model = index.model()
        data = model.data(index, role)
        return data


class AbstractItemDelegate(AbstractItemDelegateMixin, QtWidgets.QAbstractItemDelegate):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
