from __future__ import annotations

import logging

from prettyqt import core

logger = logging.getLogger(__name__)


class ProxyMapper(core.Object):
    """Class to map indexes / ItemSelections from one proxy to another.

    Also handles cases like:

                Root model
                    |
               shared proxy
               /          \
            Proxy_1_1     Proxy_2_1
              |            |
            Proxy_1_2     Proxy_2_2

    When mapping from 1_2 to 2_2, it will find the closest parent ("shared proxy" here),
    use mapToSource / mapSelectionFromSource until it gets there,
    and then mapFromSource / mapSelectionFromSource to get down to 2_2.
    """

    def __init__(
        self,
        proxy_1: core.QAbstractItemModel,
        proxy_2: core.QAbstractItemModel,
        **kwargs,
    ):
        super().__init__(**kwargs)
        proxychain_1 = self.get_proxy_chain(proxy_1)
        proxychain_2 = self.get_proxy_chain(proxy_2)
        common_list = [c for c in proxychain_1 if c in proxychain_2]
        if not common_list:
            raise RuntimeError("No common source model")
        common_source = common_list[0]
        logger.debug(f"Common source: {common_source}")
        self._proxychain_1 = proxychain_1[: proxychain_1.index(common_source)]
        self._proxychain_2 = proxychain_2[: proxychain_2.index(common_source)]
        logger.debug(f"Chain 1:{self._proxychain_1}")
        logger.debug(f"Chain 2:{self._proxychain_2}")

    @staticmethod
    def get_proxy_chain(model) -> list[core.QAbstractItemModel]:
        models = [model]
        while isinstance(model, core.QAbstractProxyModel):
            model = model.sourceModel()
            models.append(model)
        return models

    def map_index_from_one_to_two(self, index: core.ModelIndex) -> core.ModelIndex:
        for model in self._proxychain_1:
            logger.debug(f"mapping from {model!r} to {model.sourceModel()!r}")
            index = model.mapToSource(index)
        for model in reversed(self._proxychain_2):
            logger.debug(f"mapping from {model.sourceModel()!r} to {model!r}")
            index = model.mapFromSource(index)
        return index

    def map_index_from_two_to_one(self, index: core.ModelIndex) -> core.ModelIndex:
        for model in self._proxychain_2:
            logger.debug(f"mapping from {model!r} to {model.sourceModel()!r}")
            index = model.mapToSource(index)
        for model in reversed(self._proxychain_1):
            logger.debug(f"mapping from {model.sourceModel()!r} to {model!r}")
            index = model.mapFromSource(index)
        return index

    def map_selection_from_one_to_two(
        self, selection: core.QItemSelection
    ) -> core.QItemSelection:
        for model in self._proxychain_1:
            logger.debug(f"mapping from {model!r} to {model.sourceModel()!r}")
            selection = model.mapSelectionToSource(selection)
        for model in reversed(self._proxychain_2):
            logger.debug(f"mapping from {model.sourceModel()!r} to {model!r}")
            selection = model.mapSelectionFromSource(selection)
        return selection

    def map_selection_from_two_to_one(
        self, selection: core.QItemSelection
    ) -> core.QItemSelection:
        for model in self._proxychain_2:
            logger.debug(f"mapping from {model!r} to {model.sourceModel()!r}")
            selection = model.mapSelectionToSource(selection)
        for model in reversed(self._proxychain_1):
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
        index = mapper.map_index_from_one_to_two(proxy_1_2.index(0, 0))
