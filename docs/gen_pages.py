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
nav = docs.create_nav(path="reference")

for path in docs.iter_files("*/__init__.py"):
    mod_path = path.with_suffix("")
    doc_path = path.with_suffix(".md")
    parts = mod_path.parts[:-1]
    complete_mod_path = "prettyqt." + ".".join(mod_path.parts)
    klasses = list(
        classhelpers.iter_classes_for_module(complete_mod_path, module_filter="prettyqt")
    )
    for klass in klasses:
        doc = markdownizer.PrettyQtClassDocument(
            klass=klass, module_path=f'prettyqt.{".".join(parts)}', path=doc_path
        )
        nav[(*parts, klass.__name__)] = doc_path.with_name(f"{klass.__name__}.md")
    if klasses:
        page = markdownizer.ModuleDocument(
            hide_toc=True, module=complete_mod_path, path=doc_path
        )
        nav[parts] = doc_path.with_name("index.md")
nav.write()
