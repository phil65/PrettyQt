from __future__ import annotations

import logging

from prettyqt import core, custom_models


logger = logging.getLogger(__name__)


class LinkedSelectionModel(core.ItemSelectionModel):
    def __init__(
        self,
        *itemviews,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._itemviews = itemviews
        self._models = [w.model() for w in itemviews]
        self._mapper = custom_models.ProxyMapper(*self._models)
        for w in itemviews:
            w.selectionModel().currentChanged.connect(self._on_current_change)

    def _on_current_change(self, new: core.ModelIndex, _):
        source = new.model()
        if source is None:
            logger.warning("No model connected to index")
            return
        source_index = self._models.index(source)
        targets = list(range(len(self._models)))
        targets.remove(source_index)
        for target in targets:
            mapped_idx = self._mapper.map_index(from_=source_index, to=target, index=new)
            self._itemviews[target].setCurrentIndex(mapped_idx)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app(style="Vista")
    table = debugging.example_table()
    table.proxifier.transpose()
    table.proxifier.get_proxy("table_to_list")
    w = debugging.ProxyComparerWidget(table.model())
    tables = w.find_children(widgets.TableView)
    mod = LinkedSelectionModel(*w.proxy_tables)
    with app.debug_mode():
        w.show()
        app.exec()
