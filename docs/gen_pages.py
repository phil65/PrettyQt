"""Generate the code reference pages and navigation."""

from __future__ import annotations

import logging
from pathlib import Path
import sys

import prettyqt

from prettyqt.utils import classhelpers, markdownizer

logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

prettyqt.import_all()

docs = markdownizer.Docs(module_name="prettyqt", exclude_modules=["qt"])
ref_page = docs.create_nav(path="reference")

for path in docs.iter_files("*/__init__.py"):
    mod_path = path.with_suffix("")
    doc_path = path.with_suffix(".md")
    complete_mod_path = "prettyqt." + ".".join(mod_path.parts)
    parts = mod_path.parts[:-1]
    full_doc_path = Path("reference", doc_path)
    klasses = list(
        classhelpers.iter_classes_for_module(complete_mod_path, module_filter="prettyqt")
    )
    for klass in klasses:
        kls_name = klass.__name__
        ref_page[(*parts, kls_name)] = doc_path.with_name(f"{kls_name}.md")
        path = full_doc_path.with_name(f"{kls_name}.md")
        doc = markdownizer.PrettyQtClassDocument(
            klass=klass, module_path=f'prettyqt.{".".join(parts)}', path=path
        )
    if klasses:
        ref_page[parts] = doc_path.with_name("index.md")
        ref_doc_path = full_doc_path.with_name("index.md")
        page = markdownizer.ModuleDocument(
            hide_toc=True, module=complete_mod_path, path=ref_doc_path
        )
ref_page.write()
