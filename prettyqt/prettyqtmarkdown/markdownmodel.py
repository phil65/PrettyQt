from __future__ import annotations

import contextlib
import logging

import mknodes

from prettyqt import constants, core, itemmodels
from prettyqt.utils import helpers


logger = logging.getLogger(__name__)


class MarkdownModel(itemmodels.TreeModel):
    """An ItemModel for displaying a mknodes tree."""

    class Roles:
        MarkdownRole = constants.USER_ROLE + 5325

    def columnCount(self, index: core.ModelIndex | None = None) -> int:
        return 2

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        data = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return repr(data)
            case constants.DISPLAY_ROLE, 1:
                with contextlib.suppress(AttributeError):
                    return data._to_markdown().count("\n")
            # case constants.DISPLAY_ROLE, 2:
            #     return data.to_markdown()
            case self.Roles.MarkdownRole, _:
                return data.to_markdown()

    def _fetch_object_children(self, item) -> list[MarkdownModel.TreeItem]:
        return [self.TreeItem(i) for i in item.obj.children]

    def _has_children(self, item) -> bool:
        return len(item.obj.children) > 0


if __name__ == "__main__":
    page = mknodes.MkPage()
    page += mknodes.MkAdmonition("test")
    page += mknodes.MkTable(data=dict(a=[1, 2], b=["c", "D"]), header="From mapping")
    page += mknodes.MkDocStrings(helpers, header="DocStrings")
    model = MarkdownModel(page)
    print(page.to_markdown())
