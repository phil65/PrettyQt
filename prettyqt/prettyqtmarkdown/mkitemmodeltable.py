from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import mknodes

from prettyqt import itemmodels


if TYPE_CHECKING:
    from prettyqt import core


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
