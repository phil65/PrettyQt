"""Generate the code reference pages and navigation."""

from __future__ import annotations

import importlib
from pathlib import Path
import inspect
import mkdocs_gen_files

from prettyqt import core, gui, itemmodels, widgets

BASE_URL = "https://doc.qt.io/qtforpython-6/PySide6/"


def write_file_for_klass(klass, parts, file):
    ident = ".".join(parts)
    file.write(f"::: prettyqt.{ident}.{klass.__name__}\n")
    # print(ident)
    if issubclass(klass, itemmodels.SliceIdentityProxyModel):
        print("here")
        file.write("!!! note\n")
        file.write(
            "This is a [slice proxy](SliceIdentityProxyModel.md) and can be selectively applied to a model.\n\n"
        )
    if issubclass(klass, core.QObject):
        table = get_prop_table_for_klass(klass)
        file.write(table)
        table = get_ancestor_table_for_klass(klass)
        file.write(table)
        if parts[-1] in ["core", "gui", "widgets"]:
            url = f"{BASE_URL}Qt{parts[-1].capitalize()}/Q{klass.__name__}.html"
            file.write(f"Qt Base Class: [Q{klass.__name__}]({url})")
    if hasattr(klass, "ID") and issubclass(klass, gui.Validator):
        file.write(f"\n\nValidator ID: **{klass.ID}**\n\n")
    if hasattr(klass, "ID") and issubclass(klass, widgets.AbstractItemDelegateMixin):
        file.write(f"\n\nDelegate ID: **{klass.ID}**\n\n")


def get_prop_table_for_klass(klass: type[core.QObject]):
    metaobject = core.MetaObject(klass.staticMetaObject)
    user_prop_name = (
        user_prop.get_name()
        if (user_prop := metaobject.get_user_property()) is not None
        else None
    )
    props_without_super = metaobject.get_properties(include_super=False)
    prop_names_without_super = [p.get_name() for p in props_without_super]
    props_with_super = metaobject.get_properties(include_super=True)
    super_props = [
        p for p in props_with_super if p.get_name() not in prop_names_without_super
    ]
    if not props_with_super:
        return ""
    lines = []
    if props_without_super:
        lines.extend(
            (
                f"\n### Class Properties:\n",
                "|Qt Property|Type|User property|\n|-----------|----|-----------|",
            )
        )
        lines.extend(
            f"|`{prop.get_name()}`|{prop.get_meta_type()}|{'x' if prop.get_name() == user_prop_name else ''}|"
            for prop in props_without_super
        )
    if super_props:
        lines.extend(
            (
                f"\n### Inherited Properties:\n",
                "|Qt Property|Type|User property|\n|-----------|----|-----------|",
            )
        )
        lines.extend(
            f"|`{prop.get_name()}`|{prop.get_meta_type()}|{'x' if prop.get_name() == user_prop_name else ''}|"
            for prop in super_props
        )
    return "\n\n" + "\n".join(lines) + "\n\n"


def get_ancestor_table_for_klass(klass: type[core.QObject]):
    subclasses = klass.__subclasses__()
    if not subclasses:
        return ""
    lines = ["|Ancestor|Description|", "|--------|-----------|"]
    lines.extend(
        f"|`{subklass.__name__}`|{subklass.__module__}|" for subklass in subclasses
    )
    return "\n\n" + "\n".join(lines) + "\n\n"


def write_files_for_module(module_path, doc_path, parts):
    full_doc_path = Path("reference", doc_path)
    with mkdocs_gen_files.open(full_doc_path.with_name("index.md"), "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: prettyqt.{ident}")
    try:
        module = importlib.import_module(module_path)
        klass_names = [i[0] for i in inspect.getmembers(module, inspect.isclass)]
        klasses = [
            i[1]
            for i in inspect.getmembers(module, inspect.isclass)
            if issubclass(
                i[1], core.ObjectMixin
            )  # not i[0].endswith("Mixin") and not i[0].startswith("Q")  # f"Q{i[0]}" in klass_names
        ]
    except (AttributeError, ImportError) as e:
        klasses = []
    mkdocs_gen_files.set_edit_path(full_doc_path.with_name("index.md"), module_path)
    for klass in klasses:
        kls_name = klass.__name__
        nav[(*parts, kls_name)] = doc_path.with_name(f"{kls_name}.md").as_posix()
        with mkdocs_gen_files.open(full_doc_path.with_name(f"{kls_name}.md"), "w") as fd:
            write_file_for_klass(klass, parts, fd)
        mkdocs_gen_files.set_edit_path(
            full_doc_path.with_name(f"{kls_name}.md"), module_path
        )


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
    except (AttributeError, ModuleNotFoundError, ImportError) as e:
        klasses = []
    parts = parts[:-1]
    # print(parts, doc_path.with_name("index.md").as_posix())
    nav[parts] = doc_path.with_name("index.md").as_posix()
    write_files_for_module(module_path, doc_path, parts)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
