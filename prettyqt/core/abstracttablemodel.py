from typing import TYPE_CHECKING

from prettyqt import constants, core


if TYPE_CHECKING:
    from prettyqt.qt import QtCore

    _AbstractTableModelBase = QtCore.QAbstractTableModel
else:
    _AbstractTableModelBase = object


class AbstractTableModelMixin(core.AbstractItemModelMixin, _AbstractTableModelBase):
    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED
        | constants.IS_ENABLED
        | constants.IS_SELECTABLE
        | constants.NO_CHILDREN
    )


class AbstractTableModel(AbstractTableModelMixin, core.QAbstractTableModel):
    """Abstract model that can be subclassed to create table models."""


if __name__ == "__main__":
    from prettyqt import itemmodels, widgets

    app = widgets.app()
    model = itemmodels.QObjectPropertiesModel(app)
    table = widgets.TableView()
    table.set_model(model)
    print(model.to_markdown())
