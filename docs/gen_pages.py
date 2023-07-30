from __future__ import annotations

import pathlib

import mknodes
from docs import build_root, build_index

# load our existing SUMMARY.md and static content...
nav_file = pathlib.Path(__file__).parent / "SUMMARY.md"
root_nav = mknodes.MkNav.from_file(nav_file)
page = root_nav.add_index_page("Home", hide_nav=True)
build_index.build_index(page)
# and extend it with generated documentation.
build_root.build_root(root_nav)
root_nav.write()

# from prettyqt import widgets
# app = widgets.app()
# print(root_nav)
# table = prettyqtmarkdown.MarkdownWidget()
# table.set_markdown(root_nav)
# table.show()
# app.exec()
