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
nav = docs.create_nav(section="reference")

for path in docs.iter_files("*/__init__.py"):
    doc_path = path.with_suffix(".md")
    mod_path = ".".join(path.with_suffix("").parts)
    complete_mod_path = f"prettyqt.{mod_path}"
    klasses = list(
        docs.iter_classes_for_module(complete_mod_path, filter_by___all__=True)
    )
    for klass in klasses:
        nav.add_class_page(klass=klass, path=doc_path)
    if klasses:
        nav.add_module_page(module=mod_path, path=doc_path)
docs.write()
