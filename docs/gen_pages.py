"""Generate the code reference pages and navigation."""


from __future__ import annotations

import logging
import sys

import prettyqt
from prettyqt import prettyqtmarkdown
import mknodes

# from prettyqt.utils import classhelpers
# from prettyqt import prettyqtmarkdown

logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

QT_MODULE_ATTR = "QT_MODULE"

prettyqt.import_all()
# import os
# os.chdir(".docs/")
# root_nav = mknodes.MkNav.from_file("SUMMARY.md", section=None
root_nav = mknodes.MkNav(filename="somethingelse.md")
qt_docs = root_nav.add_doc(prettyqt, section_name="qt_modules")
# page = qt_docs.add_page("index")
# table = mknodes.MkModuleTable(module=prettyqt, predicate=lambda x: hasattr(x, QT_MODULE_ATTR))
# page += table
extra_docs = root_nav.add_doc(prettyqt, section_name="additional_modules")

for submod in qt_docs.iter_modules(predicate=lambda x: hasattr(x, QT_MODULE_ATTR)):
    subdoc = qt_docs.add_doc(
        submod, class_page=prettyqtmarkdown.MkPrettyQtClassPage, flatten_nav=True
    )
    subdoc.collect_classes()
for submod in extra_docs.iter_modules(predicate=lambda x: not hasattr(x, QT_MODULE_ATTR)):
    subdoc = extra_docs.add_doc(
        submod, class_page=prettyqtmarkdown.MkPrettyQtClassPage, flatten_nav=True
    )
    subdoc.collect_classes()

# extra_docs.pretty_print()

root_nav.write()

# from prettyqt import widgets

# app = widgets.app()
# print(root_nav)
# table = prettyqtmarkdown.MarkdownWidget()
# table.set_markdown(root_nav)
# table.show()
# app.exec()
