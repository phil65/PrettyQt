from __future__ import annotations

import logging

import mknodes

from prettyqt import constants, core, itemmodels
from prettyqt.utils import helpers


logger = logging.getLogger(__name__)


class MarkdownModel(itemmodels.TreeModel):
    """An ItemModel for displaying a mknodes tree."""

    HEADER = ["Repr", "Type", "Files"]

    class Roles:
        MarkdownRole = constants.USER_ROLE + 5325

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.HEADER[section]
        return None

    def columnCount(self, index: core.ModelIndex | None = None) -> int:
        return len(self.HEADER)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        node = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                match node:
                    case mknodes.MkNav():
                        return f"{node.section}/"
                    case mknodes.MkPage():
                        return node.path
                    case _:
                        return repr(node)
            # case constants.DISPLAY_ROLE, 1:
            #     with contextlib.suppress(AttributeError):
            #         return node._to_markdown().count("\n")
            case constants.DISPLAY_ROLE, 1:
                return type(node).__name__
            case constants.DISPLAY_ROLE, 2:
                keys = node.resolved_virtual_files.keys()
                return ", ".join(keys)
            case self.Roles.MarkdownRole, _:
                return node.to_markdown()

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
