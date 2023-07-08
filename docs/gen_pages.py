"""Generate the code reference pages and navigation."""

from __future__ import annotations

import importlib
from pathlib import Path
import inspect
import mkdocs_gen_files

from prettyqt import (
    core,
    charts,
    custom_network,
    custom_widgets,
    debugging,
    designer,
    eventfilters,
    gui,
    itemdelegates,
    itemmodels,
    ipython,
    # location,
    multimedia,
    multimediawidgets,
    network,
    openglwidgets,
    pdf,
    pdfwidgets,
    positioning,
    printsupport,
    qml,
    qthelp,
    quick,
    quickwidgets,
    # statemachine,
    svg,
    svgwidgets,
    texttospeech,
    validators,
    webenginecore,
    webenginewidgets,
    widgets,
)

from prettyqt.utils import markdownhelpers

# app = widgets.app()
BASE_URL = "https://doc.qt.io/qtforpython-6/PySide6/"
# table = widgets.TableView()


HIDE_NAV = """---
hide:
  - toc
---

"""


def write_file_for_klass(klass: type, parts: tuple[str, ...], file):
    ident = ".".join(parts)
    file.write(f"::: prettyqt.{ident}.{klass.__name__}\n")
    # print(ident)
    if issubclass(klass, itemmodels.SliceIdentityProxyModel):
        text = "This is a [slice proxy](SliceIdentityProxyModel.md) and can be selectively applied to a model."
        message = markdownhelpers.get_admonition("note", text)
        file.write(message)
    if issubclass(klass, core.AbstractItemModelMixin) and klass.IS_RECURSIVE:
        text = "Model can be recursive, so be careful with iterating whole tree."
        message = markdownhelpers.get_admonition("warning", text)
        file.write(message)
    if issubclass(klass, core.QObject):
        # model = itemmodels.QObjectPropertiesModel()
        table = markdownhelpers.get_prop_tables_for_klass(klass)
        file.write(table)
        table = markdownhelpers.get_ancestor_table_for_klass(klass)
        file.write(table)
        if parts[-1] in ["core", "gui", "widgets"]:
            url = f"{BASE_URL}Qt{parts[-1].capitalize()}/Q{klass.__name__}.html"
            file.write(f"Qt Base Class: [Q{klass.__name__}]({url})")
    if hasattr(klass, "ID") and issubclass(klass, gui.Validator):
        file.write(f"\n\nValidator ID: **{klass.ID}**\n\n")
    if hasattr(klass, "ID") and issubclass(klass, widgets.AbstractItemDelegateMixin):
        file.write(f"\n\nDelegate ID: **{klass.ID}**\n\n")
    text = markdownhelpers.get_mermaid_for_klass(klass)
    file.write(text)


def write_files_for_module(module_path, doc_path, parts):
    full_doc_path = Path("reference", doc_path)
    try:
        module = importlib.import_module(module_path)
        # klass_names = [i[0] for i in inspect.getmembers(module, inspect.isclass)]
        klasses = [
            i[1]
            for i in inspect.getmembers(module, inspect.isclass)
            if issubclass(
                i[1], core.ObjectMixin
            )  # not i[0].endswith("Mixin") and not i[0].startswith("Q")  # f"Q{i[0]}" in klass_names
        ]
    except (AttributeError, ImportError) as e:
        klasses = []
    for klass in klasses:
        kls_name = klass.__name__
        nav[(*parts, kls_name)] = doc_path.with_name(f"{kls_name}.md").as_posix()
        with mkdocs_gen_files.open(full_doc_path.with_name(f"{kls_name}.md"), "w") as fd:
            write_file_for_klass(klass, parts, fd)
        # with mkdocs_gen_files.open(full_doc_path.with_name(f"{kls_name}_with_inherited.md"), "w") as fd:
        #     ident = ".".join(parts)
        #     file.write(f"::: prettyqt.{ident}.{klass.__name__}\n")
        #     file.write(f"    options:\n")
        #     file.write(f"      allow_inspection: false\n")
        mkdocs_gen_files.set_edit_path(
            full_doc_path.with_name(f"{kls_name}.md"), module_path
        )
    with mkdocs_gen_files.open(full_doc_path.with_name("index.md"), "w") as fd:
        fd.write(HIDE_NAV)
        text = markdownhelpers.get_class_table(klasses)
        fd.write(text)
    mkdocs_gen_files.set_edit_path(full_doc_path.with_name("index.md"), module_path)


nav = mkdocs_gen_files.Nav()
for path in sorted(Path("./prettyqt").rglob("*/*.py")):
    if "__pyinstaller" in str(path) or path.is_dir():
        continue
    module_path = path.relative_to("./prettyqt").with_suffix("")
    doc_path = path.relative_to("./prettyqt").with_suffix(".md")
    parts = tuple(module_path.parts)
    if parts[-1] != "__init__" or parts[0] == "qt":
        continue
    module_path = "prettyqt." + ".".join(parts)
    try:
        module = importlib.import_module(module_path)
        klasses = [i[1] for i in inspect.getmembers(module, inspect.isclass)]
    except (AttributeError, ImportError) as e:
        klasses = []
    parts = parts[:-1]
    # print(parts, doc_path.with_name("index.md").as_posix())
    nav[parts] = doc_path.with_name("index.md").as_posix()
    write_files_for_module(module_path, doc_path, parts)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
