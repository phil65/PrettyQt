from __future__ import annotations

import logging

from prettyqt import core, custom_models


logger = logging.getLogger(__name__)


class LinkedSelectionModel(core.ItemSelectionModel):
    def __init__(
        self,
        *widgets,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._widgets = widgets
        self._models = [w.model() for w in widgets]
        self._mapper = custom_models.ProxyMapper(*self._models)
        for w in widgets:
            w.selectionModel().currentChanged.connect(self._on_current_change)

    def _on_current_change(self, new: core.ModelIndex, _):
        source = new.model()
        source_index = self._models.index(source)
        targets = list(range(len(self._models)))
        targets.remove(source_index)
        for target in targets:
            target_index = self._mapper.map_index(source_index, target, new)
            self._widgets[target].setCurrentIndex(target_index)


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
