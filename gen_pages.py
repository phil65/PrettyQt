"""Generate the code reference pages and navigation."""

from __future__ import annotations

import logging
import importlib
from pathlib import Path
import inspect
import sys

import prettyqt
from prettyqt import qt, core, gui, itemmodels, widgets

from prettyqt.utils import classhelpers, markdownhelpers, markdownizer

logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

for mod in prettyqt.__all__:
    try:
        importlib.import_module(f"prettyqt.{mod}")
    except ImportError:
        logger.warning(f"{mod} not available. binding: {qt.API}")

app = widgets.app()
# table = widgets.TableView()

SLICE_PROXY_INFO = "This is a [slice proxy](SliceIdentityProxyModel.md) and can be selectively applied to a model."
RECURSIVE_MODEL_INFO = "Model can be recursive, so be careful with iterating whole tree."

HIDE_NAV = """---
hide:
  - toc
---

"""

mapping = {}


def get_widget_screenshot(widget: widgets.QWidget) -> bytes:
    widget.show()
    widget.adjustSize()
    pixmap = widget.grab()
    widget.hide()
    ba = core.ByteArray()
    buffer = core.QBuffer(ba)
    buffer.open(core.QIODeviceBase.OpenModeFlag.WriteOnly)
    ok = pixmap.save(buffer, "PNG")
    return ba.data()


def get_document_for_klass(klass: type, parts: tuple[str, ...], path: str = ""):
    doc = markdownizer.MarkdownDocument(path=path)
    doc += markdownizer.DocStringSection(f'prettyqt.{".".join(parts)}.{klass.__name__}')
    if issubclass(klass, itemmodels.SliceIdentityProxyModel):
        doc += markdownizer.Admonition("info", SLICE_PROXY_INFO)
    if issubclass(klass, core.AbstractItemModelMixin) and klass.IS_RECURSIVE:
        doc += markdownizer.Admonition("warning", RECURSIVE_MODEL_INFO)
    if (
        issubclass(klass, core.AbstractItemModelMixin)
        and klass.DELEGATE_DEFAULT is not None
    ):
        msg = f"Recommended delegate: {klass.DELEGATE_DEFAULT!r}"
        doc += markdownizer.Admonition("info", msg)
    if issubclass(klass, core.QObject):
        # model = itemmodels.QObjectPropertiesModel()
        for table in markdownizer.Table.get_prop_tables_for_klass(klass):
            doc += table
        if table := markdownizer.Table.get_ancestor_table_for_klass(klass):
            doc += table
        if qt_parent := classhelpers.get_qt_parent_class(klass):
            doc += f"Qt Base Class: {markdownhelpers.get_qt_help_link(qt_parent)}"
    if hasattr(klass, "ID") and issubclass(klass, gui.Validator):
        doc += f"\n\nValidator ID: **{klass.ID}**\n\n"
    if hasattr(klass, "ID") and issubclass(klass, widgets.AbstractItemDelegateMixin):
        doc += f"\n\nDelegate ID: **{klass.ID}**\n\n"
    doc += markdownizer.MermaidDiagram.for_classes([klass])
    return doc


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
        doc = get_document_for_klass(klass, parts, path=path)
        # if (
        #     hasattr(klass, "setup_example")
        #     and "Abstract" not in klass.__name__
        #     and not klass.__name__.endswith("Mixin")
        # ):
        #     if widget := klass.setup_example():
        #         doc += markdownizer.BinaryImage(
        #             data=get_widget_screenshot(widget),
        #             path=full_doc_path.parent / f"{kls_name}.png",
        #             header="🖼 Screenshot",
        #         )
        doc.write(path, edit_path=module_path)

    # if klasses:
    page = markdownizer.MarkdownDocument(hide_toc=True)
    page += markdownhelpers.get_class_table(klasses)
    page.write(full_doc_path.with_name("index.md"), edit_path=module_path)


docs = markdownizer.Docs(module_name="prettyqt", exclude_modules=["qt"])

for path in docs.yield_files("*/__init__.py"):
    module_path = path.with_suffix("")
    doc_path = path.with_suffix(".md")
    parts = tuple(module_path.parts)
    complete_module_path = "prettyqt." + ".".join(parts)
    try:
        module = importlib.import_module(complete_module_path)
        klasses = [i[1] for i in inspect.getmembers(module, inspect.isclass)]
    except (AttributeError, ImportError) as e:
        klasses = []
    parts = parts[:-1]
    # print(parts, doc_path.with_name("index.md").as_posix())
    mapping[parts] = doc_path.with_name("index.md").as_posix()
    write_files_for_module(complete_module_path, doc_path, parts)

page = markdownizer.LiterateNav(mapping)
page.write("reference/SUMMARY.md")
