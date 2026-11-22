from __future__ import annotations

from prettyqt.docs import build_root, build_index

import mknodes


def build(root: mknodes.MkNav, theme: mknodes.Theme) -> mknodes.MkNav:
    build_root.build_root(root)
    page = root.add_page("Home", is_index=True, hide="nav")
    build_index.build_index(page)
    return root
