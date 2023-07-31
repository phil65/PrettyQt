from __future__ import annotations

from prettyqt.docs import build_root, build_index


root_nav = build_root.build_root()
page = root_nav.add_index_page("Home", hide_nav=True)
build_index.build_index(page)
root_nav.write()

# from prettyqt import prettyqtmarkdown, widgets
# app = widgets.app()
# print(root_nav)
# table = prettyqtmarkdown.MarkdownWidget()
# table.set_markdown(root_nav)
# table.show()
# app.exec()
