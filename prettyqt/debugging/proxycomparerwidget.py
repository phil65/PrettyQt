from __future__ import annotations

import logging
from typing import Literal

from prettyqt import core, custom_widgets, itemmodels, widgets


logger = logging.getLogger(__name__)


class ProxyComparerWidget(widgets.Splitter):
    """Splitter widget showing a comparison view between a proxy and its sourceModels.

    <figure markdown>
      ![Image title](../../images/proxycomparerwidget.png)
      <figcaption>ProxyComparerWidget</figcaption>
    </figure>
    """

    def __init__(
        self,
        model: core.QAbstractProxyModel,
        itemview: (
            Literal["tree", "table", "list"] | type[widgets.QAbstractItemView]
        ) = "table",
        delegate: (
            widgets.abstractitemview.DelegateStr | widgets.QItemDelegate | None
        ) = "editor",
        link_selections: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.model_itemviews = []
        self.linker = None
        # determine ItemView class for the models
        match itemview:
            case "tree":
                view_cls = widgets.TreeView
            case "table":
                view_cls = widgets.TableView
            case "list":
                view_cls = widgets.ListView
            case type():
                view_cls = itemview
            case _:
                raise TypeError(itemview)

        # collect models
        models = []
        while isinstance(model, core.QAbstractProxyModel):
            models.append(model)
            model = model.sourceModel()
        models.append(model)

        # add column for each model

        for model in reversed(models):
            container = widgets.Widget()
            layout = container.set_layout("vertical")
            table = view_cls()
            table.set_model(model)
            table.set_delegate(delegate)
            self.model_itemviews.append(table)
            prop_table = custom_widgets.QObjectPropertiesTableView()
            prop_table.set_qobject(model)
            header = widgets.Label(type(model).__name__)
            layout.add(header)
            col_splitter = widgets.Splitter("vertical")
            col_splitter.add(table)
            col_splitter.add(prop_table)
            layout.add(col_splitter)
            self.add(container)
        if link_selections:
            self.linker = itemmodels.LinkedSelectionModel(*self.model_itemviews)

    # @classmethod
    # def setup_example(cls):
    #     from prettyqt import gui

    #     dct = dict(
    #         a=["a", "a", "a", "a"],
    #         b=["b", "b", "b", "b"],
    #         c=["c", "c", "c", "c"],
    #     )
    #     model = gui.StandardItemModel.from_dict(dct)
    #     proxy = core.TransposeProxyModel(source_model=model)
    #     return cls(proxy)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    # table = debugging.example_table()
    # table.proxifier.transpose()
    # table.proxifier.to_list()
    splitter = ProxyComparerWidget.setup_example()
    splitter.show()
    app.exec()
