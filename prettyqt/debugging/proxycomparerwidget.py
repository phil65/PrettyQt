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
        while isinstance(proxy, core.QAbstractProxyModel):
            container = widgets.Widget()
            layout = container.set_layout("vertical")
            table = View()
            table.set_model(proxy)
            table.set_delegate("editor")
            self.proxy_tables.append(table)
            prop_table = widgets.TableView()
            prop_table.set_delegate("editor")
            model = custom_models.WidgetPropertiesModel(proxy)
            prop_table.set_model(model)
            layout.add(widgets.Label(type(proxy).__name__))
            col_splitter = widgets.Splitter("vertical")
            col_splitter.add(prop_table)
            col_splitter.add(table)
            layout.add(col_splitter)
            self.add(container)
            proxy = proxy.sourceModel()

        container = widgets.Widget()
        layout = container.set_layout("vertical")
        table = View()
        table.set_model(proxy)
        table.set_delegate("editor")
        self.proxy_tables.append(table)
        layout.add(widgets.Label(type(proxy).__name__))
        layout.add(table)
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
