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
ref_page = markdownizer.LiterateNav(path="reference")

for path in docs.yield_files("*/__init__.py"):
    mod_path = path.with_suffix("")
    doc_path = path.with_suffix(".md")
    parts = tuple(mod_path.parts)
    complete_mod_path = "prettyqt." + ".".join(parts)
    parts = parts[:-1]
    full_doc_path = Path("reference", doc_path)
    klasses = classhelpers.get_module_classes(complete_mod_path, module_filter="prettyqt")
    for klass in klasses:
        kls_name = klass.__name__
        ref_page[(*parts, kls_name)] = doc_path.with_name(f"{kls_name}.md").as_posix()
        path = full_doc_path.with_name(f"{kls_name}.md")
        doc = markdownizer.PrettyQtClassDocument(
            klass=klass, module_path=f'prettyqt.{".".join(parts)}', path=path
        )
        doc.write(path, edit_path=complete_mod_path)
    if klasses:
        ref_page[parts] = doc_path.with_name("index.md").as_posix()
        ref_doc_path = full_doc_path.with_name("index.md")
        page = markdownizer.Document(hide_toc=True, path=ref_doc_path)
        page += markdownizer.Table.get_classes_table(klasses)
        page.write(full_doc_path.with_name("index.md"), edit_path=complete_mod_path)

ref_page.write()
