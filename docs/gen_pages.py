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

root_nav = mknodes.MkNav(filename="somethingelse.md")
qt_docs = root_nav.add_documentation(prettyqt, section_name="Qt Modules")
# page = qt_docs.add_page("index")
# table = mknodes.MkModuleTable(module=prettyqt, predicate=lambda x: hasattr(x, QT_MODULE_ATTR))
# page += table
extra_docs = root_nav.add_documentation(prettyqt, section_name="Additional Modules")
extra_docs.add_module_overview()

for submod in qt_docs.iter_modules(predicate=lambda x: hasattr(x, QT_MODULE_ATTR)):
    subdoc = qt_docs.add_documentation(
        submod, class_page=prettyqtmarkdown.PrettyQtClassPage
    )
    subdoc.add_module_overview()
    for klass in subdoc.iter_classes():
        subdoc.add_class_page(klass=klass, flatten=True)
for submod in extra_docs.iter_modules(predicate=lambda x: not hasattr(x, QT_MODULE_ATTR)):
    subdoc = extra_docs.add_documentation(
        submod, class_page=prettyqtmarkdown.PrettyQtClassPage
    )
    subdoc.add_module_overview()
    for klass in subdoc.iter_classes():
        subdoc.add_class_page(klass=klass, flatten=True)

# extra_docs.pretty_print()

root_nav.write()

# from prettyqt import widgets

# app = widgets.app()
# table = mknodes.MarkdownWidget()
# table.set_markdown(additional_nav)
# table.show()
# app.exec()
