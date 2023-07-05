from __future__ import annotations

import logging

from typing import Literal

from prettyqt import core, custom_models, widgets


logger = logging.getLogger(__name__)


class ProxyComparerWidget(widgets.Splitter):
    def __init__(
        self,
        proxy: core.QAbstractProxyModel,
        itemview: Literal["tree", "table", "list"]
        | type[widgets.QAbstractItemView] = "table",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.proxy_tables = []

        # determine ItemView class for the models
        match itemview:
            case "tree":
                View = widgets.TreeView
            case "table":
                View = widgets.TableView
            case "list":
                View = widgets.ListView
            case type():
                View = itemview
            case _:
                raise TypeError(itemview)

        # collect models
        models = []
        while isinstance(proxy, core.QAbstractProxyModel):
            models.append(proxy)
            proxy = proxy.sourceModel()
        models.append(proxy)

        # add column for each model

        for model in reversed(models):
            container = widgets.Widget()
            layout = container.set_layout("vertical")
            table = View()
            table.set_model(model)
            table.set_delegate("editor")
            self.proxy_tables.append(table)
            prop_table = widgets.TableView()
            prop_table.set_delegate("editor")
            prop_model = custom_models.WidgetPropertiesModel(model)
            prop_table.set_model(prop_model)
            layout.add(widgets.Label(type(model).__name__))
            col_splitter = widgets.Splitter("vertical")
            col_splitter.add(table)
            col_splitter.add(prop_table)
            layout.add(col_splitter)
            self.add(container)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    table = debugging.example_table()
    table.proxifier.transpose()
    table.proxifier.to_list()
    splitter = ProxyComparerWidget(table.model())
    splitter.show()
    app.exec()
