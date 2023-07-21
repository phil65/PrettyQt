from __future__ import annotations

import logging

from mknodes import connectionbuilder

from prettyqt import constants, core


logger = logging.getLogger(__name__)


class IndexConnectionBuilder(connectionbuilder.ConnectionBuilder):
    def __init__(
        self, index: core.ModelIndex, fetch_more: bool = True, attribute_roles=None
    ):
        self.fetch_more = fetch_more
        self.attribute_roles = attribute_roles or []
        super().__init__([index])

    def get_id(self, item: core.ModelIndex) -> int:
        return id(item)

    def get_title(self, item: core.ModelIndex) -> str:
        return item.data(constants.DISPLAY_ROLE)

    def get_attributes(self, item: core.ModelIndex) -> list[str]:
        return [item.data(role) for role in self.attribute_roles]

    def get_children(self, item: core.ModelIndex) -> list[core.ModelIndex]:
        model = item.model()
        if self.fetch_more:
            while model.canFetchMore(item):
                model.fetchMore(item)
        return [model.index(i, 0, item) for i in range(model.rowCount(item))]


class PrettyQtDiagram:
    pass


if __name__ == "__main__":
    import mknodes

    from prettyqt import prettyqtmarkdown

    page = mknodes.MkPage([])
    page += mknodes.MkAdmonition("test")
    page += mknodes.MkTable(data=dict(a=[1, 2], b=["c", "D"]), header="From mapping")
    page += mknodes.MkDocStrings(core, header="DocStrings")
    model = prettyqtmarkdown.MarkdownModel(page)
    builder = IndexConnectionBuilder(model.index(0, 0, core.ModelIndex()))
    print(builder.connections)
