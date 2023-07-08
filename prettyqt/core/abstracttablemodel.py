from __future__ import annotations

from prettyqt import constants, core


class AbstractTableModelMixin(core.AbstractItemModelMixin):
    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED
        | constants.IS_ENABLED
        | constants.IS_SELECTABLE
        | constants.NO_CHILDREN
    )


class AbstractTableModel(AbstractTableModelMixin, core.QAbstractTableModel):
    pass


if __name__ == "__main__":
    from prettyqt import itemmodels, widgets

    app = widgets.app()
    model = itemmodels.QObjectPropertiesModel(app)
    table = widgets.TableView()
    table.set_model(model)
    print(model.to_markdown())
