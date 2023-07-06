from __future__ import annotations

import logging

from prettyqt import core


logger = logging.getLogger(__name__)


class ProxyMapper(core.Object):
    """Class to map indexes / ItemSelections from one proxy to another.

    Also handles cases like:
    ```
                Root model
                    |
               shared proxy
               /          \
            Proxy_1_1     Proxy_2_1
              |            |
            Proxy_1_2     Proxy_2_2
    ```
    When mapping from 1_2 to 2_2, it will find the closest parent ("shared proxy" here),
    use mapToSource / mapSelectionFromSource until it gets there,
    and then mapFromSource / mapSelectionFromSource to get down to 2_2.
    """

    def __init__(
        self,
        *proxies: core.QAbstractItemModel,
        **kwargs,
    ):
        super().__init__(**kwargs)
        chains = [self.get_proxy_chain(proxy) for proxy in proxies]
        common_list = [
            element
            for element in chains[0]
            if all(element in sublist for sublist in chains[1:])
        ]
        if not common_list:
            raise RuntimeError("No common source model")
        common_source = common_list[0]
        logger.debug(f"Common source: {common_source}")
        self._chains = [chain[: chain.index(common_source)] for chain in chains]

    @staticmethod
    def get_proxy_chain(model: core.QAbstractItemModel) -> list[core.QAbstractItemModel]:
        models = [model]
        while isinstance(model, core.QAbstractProxyModel):
            model = model.sourceModel()
            models.append(model)
        return models

    def map_index(self, from_: int, to: int, index: core.ModelIndex) -> core.ModelIndex:
        for model in self._chains[from_]:
            logger.debug(f"mapping from {model!r} to {model.sourceModel()!r}")
            index = model.mapToSource(index)
        for model in reversed(self._chains[to]):
            logger.debug(f"mapping from {model.sourceModel()!r} to {model!r}")
            index = model.mapFromSource(index)
        return index

    def map_selection(
        self, from_: int, to: int, selection: core.QItemSelection
    ) -> core.QItemSelection:
        for model in self._chains[from_]:
            logger.debug(f"mapping from {model!r} to {model.sourceModel()!r}")
            selection = model.mapSelectionToSource(selection)
        for model in reversed(self._chains[to]):
            logger.debug(f"mapping from {model.sourceModel()!r} to {model!r}")
            selection = model.mapSelectionFromSource(selection)
        return selection


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app()
    data = dict(
        a=["abcdedf", "abcdedf", "abcdedf", "abcdedf", "abcdedf", "abcdedfaa"],
        b=[10000000, 2, 3, 4, 5, 6],
        c=[1, 2, 3, 4, 5, 6],
        d=[100000000, 2, 3, 4, 5, 6],
        e=[1000000, 2, 3, 4, 5, 6],
        f=[1000000, 2, 3, 4, 5, 6],
        g=[1, 2, 3, 4, 5, 6],
        h=[1, 2, 3, 4, 5, 6],
        i=[100000000000000, 2, 3, 4, 5, 6],
        j=[1, 2, 3, 4, 5, 6],
        k=[1, 2, 3, 4, 5, 6],
        jkfsj=[10, 20, 30, 40, 50, 60],
    )
    model = gui.StandardItemModel.from_dict(data)
    proxy = core.SortFilterProxyModel(object_name="common")
    proxy.setSourceModel(model)
    proxy_1_1 = core.SortFilterProxyModel(object_name="1_1")
    proxy_1_1.setSourceModel(proxy)
    proxy_1_2 = core.SortFilterProxyModel(object_name="1_2")
    proxy_1_2.setSourceModel(proxy_1_1)
    proxy_2_1 = core.SortFilterProxyModel(object_name="2_1")
    proxy_2_1.setSourceModel(proxy)
    proxy_2_2 = core.SortFilterProxyModel(object_name="2_2")
    proxy_2_2.setSourceModel(proxy_2_1)
    with app.debug_mode():
        mapper = ProxyMapper(proxy_1_2, proxy_2_2)
        index = mapper.map_index(0, 1, proxy_1_2.index(0, 0))
    print(index)
