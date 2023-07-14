"""Generate the code reference pages and navigation."""


from __future__ import annotations

import logging
import sys

import prettyqt

from prettyqt.utils import classhelpers, markdownizer

logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

QT_MODULE_ATTR = "QT_MODULE"

prettyqt.import_all()

docs = markdownizer.Docs(module=prettyqt, exclude_modules=["qt"])
qt_nav = docs.create_nav(section="qt_modules")
additional_nav = docs.create_nav(section="additional_modules")
qt_overview = qt_nav.add_overview_page(predicate=lambda x: hasattr(x, QT_MODULE_ATTR))
additional_overview = additional_nav.add_overview_page(
    predicate=lambda x: not hasattr(x, QT_MODULE_ATTR)
)

qt_nav[("overview",)] = "index.md"
additional_nav[("overview",)] = "index.md"

for path in docs.iter_files("*/__init__.py"):
    doc_path = path.with_suffix(".md")
    module_path = ".".join(path.with_suffix("").parts)
    complete_module_path = f"prettyqt.{module_path}"
    module = classhelpers.to_module(complete_module_path)
    klasses = list(
        docs.iter_classes_for_module(complete_module_path, filter_by___all__=True)
    )
    if module and hasattr(module, QT_MODULE_ATTR):
        if klasses:
            qt_nav.add_module_page(module=module_path, path=doc_path)
        for klass in klasses:
            qt_nav.add_class_page(klass=klass, path=doc_path)
    else:
        if klasses:
            additional_nav.add_module_page(module=module_path, path=doc_path)
        for klass in klasses:
            additional_nav.add_class_page(klass=klass, path=doc_path)

additional_nav.pretty_print()

qt_overview.write()
additional_overview.write()
additional_nav.write()
qt_nav.write()
# docs.write_navs()


# from prettyqt import widgets

# app = widgets.app()
# table = markdownizer.MarkdownWidget()
# table.set_markdown(additional_nav)
# table.show()
# app.exec()
