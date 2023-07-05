from __future__ import annotations

import logging

from prettyqt import core, custom_models, widgets


logger = logging.getLogger(__name__)


class ProxyComparerWidget(widgets.Splitter):
    def __init__(self, proxy: core.QAbstractProxyModel, is_tree: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.proxy_tables = []
        while isinstance(proxy, core.QAbstractProxyModel):
            container = widgets.Widget()
            layout = container.set_layout("vertical")
            table = widgets.TreeView() if is_tree else widgets.TableView()
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
        table = widgets.TreeView() if is_tree else widgets.TableView()
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
