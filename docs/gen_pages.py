"""Generate the code reference pages and navigation."""


from __future__ import annotations

import logging
import sys

import prettyqt

from prettyqt.utils import classhelpers, markdownizer

logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

prettyqt.import_all()

docs = markdownizer.Docs(module_name="prettyqt", exclude_modules=["qt"])
nav = docs.create_nav(section="qt_modules")
nav2 = docs.create_nav(section="additional_modules")

for path in docs.iter_files("*/__init__.py"):
    doc_path = path.with_suffix(".md")
    module_path = ".".join(path.with_suffix("").parts)
    complete_module_path = f"prettyqt.{module_path}"
    module = classhelpers.to_module(complete_module_path)
    klasses = list(
        docs.iter_classes_for_module(complete_module_path, filter_by___all__=True)
    )
    if module and hasattr(module, "QT_MODULE"):
        for klass in klasses:
            nav.add_class_page(klass=klass, path=doc_path)
        if klasses:
            nav.add_module_page(module=module_path, path=doc_path)
    else:
        for klass in klasses:
            nav2.add_class_page(klass=klass, path=doc_path)
        if klasses:
            nav2.add_module_page(module=module_path, path=doc_path)

docs.write()
