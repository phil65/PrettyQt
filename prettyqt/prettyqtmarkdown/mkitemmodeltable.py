from __future__ import annotations

from importlib import metadata
import logging

from typing import Any

import mknodes

from prettyqt import core, itemmodels


logger = logging.getLogger(__name__)


class MkItemModelTable(mknodes.MkTable):
    """Table which can display Qt ItemModels.

    The given ItemModel will get proxied with a ProxyModel which translates
    data from some of the ItemRoles to Markup styling, and afterwords converted
    to a Markup table.
    """

    def __init__(
        self,
        model: core.AbstractItemModelMixin,
        use_checkstate_role: bool = True,
        **kwargs: Any,
    ):
        """Constructor.

        Arguments:
            model: The ItemModel to display.
            use_checkstate_role: whether to display the CheckStateRole value if available.
            kwargs: Keyword arguments passed to get_table_data.
        """
        proxy = itemmodels.SliceToMarkdownProxyModel(None, source_model=model)
        data, h_header, _ = proxy.get_table_data(
            use_checkstate_role=use_checkstate_role, **kwargs
        )
        data = list(zip(*data))
        super().__init__(data, columns=h_header)


class MkDependencyTable(MkItemModelTable):
    """MkTable subclass to display a dependency table."""

    def __init__(
        self,
        distribution: str | metadata.Distribution = "prettyqt",
    ):
        """Constructor.

        Arguments:
            distribution: distribution to show dependency table for.
        """
        model = itemmodels.ImportlibTreeModel(distribution)
        proxy = itemmodels.ColumnOrderProxyModel(
            order=["Name", "Constraints", "Extra", "Summary", "Homepage"],
            source_model=model,
        )
        super().__init__(proxy)


if __name__ == "__main__":
    table = MkDependencyTable("prettyqt")
    print(table)
