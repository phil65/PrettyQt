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

# app = widgets.app()
BASE_URL = "https://doc.qt.io/qtforpython-6/PySide6/"
# table = widgets.TableView()


def class_name(cls):
    """Return a string representing the class"""
    # NOTE: can be changed to str(class) for more complete class info
    return cls.__name__


def classes_tree(klasses):
    module_classes = set()
    inheritances = []

    def inspect_class(klass):
        if class_name(klass) not in module_classes:
            # if klass.__module__.startswith(base_module):
            module_classes.add(class_name(klass))
            for base in klass.__bases__:
                inheritances.append((class_name(base), class_name(klass)))
                inspect_class(base)

    for klass in klasses:
        inspect_class(klass)
    return module_classes, inheritances


def classes_tree_to_mermaid(klasses, inheritances):
    return "graph TD;\n" + "\n".join(
        list(klasses) + ["%s --> %s" % (a, b) for a, b in inheritances]
    )


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
        file.write("!!! note\n")
        file.write(
            "    This is a [slice proxy](SliceIdentityProxyModel.md) and can be selectively applied to a model.\n\n"
        )
    if issubclass(klass, core.AbstractItemModelMixin) and klass.IS_RECURSIVE:
        file.write("!!! Warning\n")
        file.write(
            "    Model can be recursive, so be careful with iterating whole tree.\n\n"
        )
    if issubclass(klass, core.QObject):
        # model = itemmodels.QObjectPropertiesModel()
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
    text = get_mermaid_for_klass(klass, file)


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
                f"\n## Class Properties\n",
                "|Qt Property|Type|User property|\n|-----------|----|-----------|",
            )
        )
        lines.extend(
            f"|`{prop.get_name()}`|**{(prop.get_meta_type().get_name() or '').rstrip('*')}**|{'x' if prop.get_name() == user_prop_name else ''}|"
            for prop in props_without_super
        )
    if super_props:
        lines.extend(
            (
                f"\n## Inherited Properties\n",
                "|Qt Property|Type|User property|\n|-----------|----|-----------|",
            )
        )
        lines.extend(
            f"|`{prop.get_name()}`|**{(prop.get_meta_type().get_name() or '').rstrip('*')}**|{'x' if prop.get_name() == user_prop_name else ' '}|"
            for prop in super_props
        )
    return "\n\n" + "\n".join(lines) + "\n\n"


def get_mermaid_for_klass(klass, fd):
    classes, inheritances = classes_tree([klass])
    text = classes_tree_to_mermaid(classes, inheritances)
    fd.write("\n\n## ₼ Class diagram\n\n``` mermaid\n")
    fd.write(text)
    fd.write("\n```\n")


def link_for_class(klass):
    if klass is set:
        return "set"
    return f"[{klass.__qualname__}]({klass.__qualname__}.md)"


def get_ancestor_table_for_klass(klass: type[core.QObject]):
    subclasses = klass.__subclasses__()
    if not subclasses:
        return ""
    lines = ["|Ancestor|Module|", "|--------|-----------|"]
    lines.extend(
        f"|{link_for_class(subklass)}|{subklass.__module__}|" for subklass in subclasses
    )
    return "\n\n## Child classes\n\n" + "\n".join(lines) + "\n\n"


def get_class_table(klasses: type[core.QObject]):
    lines = ["|Name|Module|Ancestors|Inherits|", "|--|--|--|--|"]
    for kls in klasses:
        subclasses = kls.__subclasses__()
        parents = kls.__bases__
        subclass_str = ", ".join(link_for_class(subclass) for subclass in subclasses)
        parent_str = ", ".join(link_for_class(parent) for parent in parents)
        line = f"|{link_for_class(kls)}|{kls.__module__}|{subclass_str}|{parent_str}|"
        lines.append(line)
    return "\n\n" + "\n".join(lines) + "\n\n"


def write_files_for_module(module_path, doc_path, parts):
    full_doc_path = Path("reference", doc_path)
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
        text = get_class_table(klasses)
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
    except (AttributeError, ModuleNotFoundError, ImportError) as e:
        klasses = []
    parts = parts[:-1]
    # print(parts, doc_path.with_name("index.md").as_posix())
    nav[parts] = doc_path.with_name("index.md").as_posix()
    write_files_for_module(module_path, doc_path, parts)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
