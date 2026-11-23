from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt.docs import build_index, build_root


if TYPE_CHECKING:
    import mknodes


def build(root: mknodes.MkNav, theme: mknodes.Theme) -> mknodes.MkNav:
    build_root.build_root(root)
    page = root.add_page("Home", is_index=True, hide="nav")
    build_index.build_index(page)
    return root
