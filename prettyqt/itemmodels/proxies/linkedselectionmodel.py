from __future__ import annotations

import logging

from prettyqt import core, itemmodels


logger = logging.getLogger(__name__)


class LinkedSelectionModel(core.ItemSelectionModel):
    # TODO: atm this doesnt need to inherit from ItemSelectionModel.
    # Not sure if there is any advantage in doing so...
    # Otherwise we could rename to SelectionLinker and just inherit from
    # object / core.Object
    def __init__(
        self,
        *itemviews,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._itemviews = itemviews
        self._models = [w.model() for w in itemviews]
        self._mapper = itemmodels.ProxyMapper(*self._models)
        for w in itemviews:
            w.selectionModel().currentChanged.connect(self._on_current_change)
            w.selectionModel().selectionChanged.connect(self._on_selection_change)

    def _on_current_change(self, new: core.ModelIndex, _):
        source = self.sender().model()
        source_index = self._models.index(source)
        target_indexes = list(range(len(self._models)))
        target_indexes.remove(source_index)
        for target_index in target_indexes:
            mapped = self._mapper.map_index(
                source=source_index, target=target_index, index=new
            )
            self._itemviews[target_index].setCurrentIndex(mapped)

    def _on_selection_change(self, new: core.QItemSelection, _):
        source_model = self.sender().model()
        source_index = self._models.index(source_model)
        target_indexes = list(range(len(self._models)))
        target_indexes.remove(source_index)
        for target_index in target_indexes:
            selected = self._mapper.map_selection(
                source=source_index, target=target_index, selection=new
            )
            sel_model = self._itemviews[target_index].selectionModel()
            sel_model.select(selected, sel_model.SelectionFlag.Select)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app(style="Vista")
    table = debugging.example_table()
    table.proxifier.transpose()
    table.proxifier.get_proxy("table_to_list")
    w = debugging.ProxyComparerWidget(table.model())
    tables = w.find_children(widgets.TableView)
    with app.debug_mode():
        w.show()
        app.exec()
