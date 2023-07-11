"""Generate the code reference pages and navigation."""

from __future__ import annotations

import logging
import importlib
from pathlib import Path
import inspect
import sys

import prettyqt
from prettyqt import qt, core, gui, itemmodels, widgets

from prettyqt.utils import classhelpers, markdownizer

logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

for mod in prettyqt.__all__:
    try:
        importlib.import_module(f"prettyqt.{mod}")
    except ImportError:
        logger.warning(f"{mod} not available. binding: {qt.API}")

# app = widgets.app()
# table = widgets.TableView()

SLICE_PROXY_INFO = "This is a [slice proxy](SliceIdentityProxyModel.md) and can be selectively applied to a model."
RECURSIVE_MODEL_INFO = "Model can be recursive, so be careful with iterating whole tree."

HIDE_NAV = """---
hide:
  - toc
---

"""

mapping = {}


def write_files_for_module(module_path, doc_path, parts):
    full_doc_path = Path("reference", doc_path)
    try:
        module = importlib.import_module(module_path)
        # klass_names = [i[0] for i in inspect.getmembers(module, inspect.isclass)]
        klasses = [
            i[1]
            for i in inspect.getmembers(module, inspect.isclass)
            if i[1].__module__.startswith("prettyqt")
        ]
    except (AttributeError, ImportError) as e:
        klasses = []
    for klass in klasses:
        kls_name = klass.__name__
        mapping[(*parts, kls_name)] = doc_path.with_name(f"{kls_name}.md").as_posix()
        path = full_doc_path.with_name(f"{kls_name}.md")
        doc = markdownizer.PrettyQtClassDocument(
            klass=klass, module_path=f'prettyqt.{".".join(parts)}', path=path
        )
        doc.write(path, edit_path=module_path)

    # if klasses:
    page = markdownizer.Document(hide_toc=True)
    page += markdownizer.Table.get_classes_table(klasses)
    page.write(full_doc_path.with_name("index.md"), edit_path=module_path)


docs = markdownizer.Docs(module_name="prettyqt", exclude_modules=["qt"])

for path in docs.yield_files("*/__init__.py"):
    module_path = path.with_suffix("")
    doc_path = path.with_suffix(".md")
    parts = tuple(module_path.parts)
    complete_module_path = "prettyqt." + ".".join(parts)
    try:
        module = importlib.import_module(complete_module_path)
        klasses = [klass for _name, klass in inspect.getmembers(module, inspect.isclass)]
    except (AttributeError, ImportError) as e:
        klasses = []
    parts = parts[:-1]
    # print(parts, doc_path.with_name("index.md").as_posix())
    mapping[parts] = doc_path.with_name("index.md").as_posix()
    write_files_for_module(complete_module_path, doc_path, parts)

page = markdownizer.LiterateNav(mapping)
page.write("reference/SUMMARY.md")
