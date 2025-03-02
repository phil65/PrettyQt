from __future__ import annotations

import logging

from prettyqt import core
from prettyqt.utils import modelhelpers


logger = logging.getLogger(__name__)


MERMAID = """
    ``` mermaid
    classDiagram
      Shared_proxy <|-- Proxy_1_1
      Shared_proxy <|-- Proxy_2_1
      Proxy_1_1 <|-- Proxy_1_2
      Proxy_2_1 <|-- Proxy_2_2
      Root_model <-- Shared_proxy
      class Proxy_1_1{
      }
      class Proxy_2_1{
      }
      class Root_model{
      }
    ```
"""


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
    ``` py
    mapper = ProxyMapper(proxy_1_2, proxy_2_1)
    index = proxy_1_2.index(0, 0)
    mapped_index = mapper.map_index(source=0, target=1, index)
    ```

    """

    def __init__(
        self,
        *proxies: core.QAbstractItemModel,
        **kwargs,
    ):
        super().__init__(**kwargs)
        chains = [modelhelpers.get_proxy_chain(proxy) for proxy in proxies]
        common_list = [
            element
            for element in chains[0]
            if all(element in sublist for sublist in chains[1:])
        ]
        if not common_list:
            msg = "No common source model"
            raise RuntimeError(msg)
        common_source = common_list[0]
        logger.debug("Common source: %s", common_source)
        self._chains = [chain[: chain.index(common_source)] for chain in chains]

    def map_index(
        self, source: int, target: int, index: core.ModelIndex
    ) -> core.ModelIndex:
        """Map index from source to target."""
        for model in self._chains[source]:
            logger.debug("mapping from %r to %r", model, model.sourceModel())
            index = model.mapToSource(index)
        for model in reversed(self._chains[target]):
            logger.debug("mapping from %r to %r", model.sourceModel(), model)
            index = model.mapFromSource(index)
        return index

    def map_selection(
        self, source: int, target: int, selection: core.QItemSelection
    ) -> core.QItemSelection:
        """Map selection from source to target."""
        for model in self._chains[source]:
            logger.debug("mapping from %r to %r", model, model.sourceModel())
            selection = model.mapSelectionToSource(selection)
        for model in reversed(self._chains[target]):
            logger.debug("mapping from %r to %r", model.sourceModel(), model)
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
