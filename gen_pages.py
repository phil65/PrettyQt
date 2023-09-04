from __future__ import annotations

from prettyqt.docs import build_root, build_index

import mknodes


def build(project: mknodes.Project):
    root_nav = build_root.build_root(project)
    page = root_nav.add_index_page("Home", hide_nav=True)
    build_index.build_index(page)


# from prettyqt import prettyqtmarkdown, widgets
# app = widgets.app()
# print(root_nav)
# table = prettyqtmarkdown.MarkdownWidget()
# table.set_markdown(root_nav)
# table.show()
# app.exec()
