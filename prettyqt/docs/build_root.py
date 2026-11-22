from __future__ import annotations

import logging
import pathlib
import sys

import prettyqt
from prettyqt import prettyqtmarkdown
import mknodes as mk
from mknodes.utils import classhelpers


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def is_qt_module(module):
    return hasattr(module, "QT_MODULE")


def build_root(root_nav: mk.MkNav) -> mk.MkNav:
    old = root_nav.ctx.links
    provider = prettyqtmarkdown.QtLinkProvider(
        old.base_url, old.use_directory_urls, include_stdlib=True
    )
    provider.add_inv_file("docs/qt6.inv", "https://doc.qt.io/qtforpython/")
    root_nav.ctx.links = provider
    root_nav.page_template.announcement_bar = mk.MkMetadataBadges("dependencies")
    nav_file = pathlib.Path(__file__).parent / "SUMMARY.md"
    root_nav.parse.file(nav_file)
    qt_docs = root_nav.add_nav("Qt-based modules")
    extra_docs = root_nav.add_nav("Additional modules")
    populate_docs(qt_docs, is_qt_module)
    populate_docs(extra_docs, lambda x: not is_qt_module(x))

    dev_nav = root_nav.add_nav("Development")
    populate_dev_section(dev_nav)
    return root_nav


def has_valid_docs(klass: type) -> bool:
    """Skip classes with a base whose __doc__ is a descriptor (PySide6 Property).

    jinjarope's get_doc chokes on those.
    """
    return all(isinstance(k.__doc__, str | None) for k in klass.__mro__)


class FlatModuleDoc(mk.MkDoc):
    """MkDoc which documents the classes of a package without recursing.

    mknodes' MkDoc imports and documents every submodule, which breaks for
    binding-specific modules and duplicates the (flat) prettyqt packages.
    """

    def get_children(self):
        if self.module is None:
            return []
        klasses = classhelpers.list_classes(
            module=self.module,
            filter_by___all__=self.filter_by___all__,
            module_filter=self.module.__name__,
            predicate=has_valid_docs,
        )
        pages = [self.add_class_page(klass=k, flatten=self.flatten_nav) for k in klasses]
        self.index_page = mk.MkModulePage(
            module=self.module,
            title=self.module_name,
            is_index=True,
            klasses=klasses,
            parent=self,
        )
        return [*pages, self.index_page]


def populate_docs(doc_nav: mk.MkNav, predicate):
    for submod in prettyqt.import_all():
        if predicate(submod):
            doc = FlatModuleDoc(module=submod, parent=doc_nav, flatten_nav=True)
            doc_nav.nav.register(doc)


def populate_dev_section(nav: mk.MkNav):
    page = nav.add_page("Changelog")
    page += mk.MkChangelog()

    page = nav.add_page("Dependencies", hide="toc")
    page += mk.MkDependencyTable()

    page = nav.add_page("Code of conduct")
    page += mk.MkCodeOfConduct()

    page = nav.add_page("Contributing")
    page += mk.MkCommitConventions()

    page = nav.add_page("Setting up the environment")
    page += mk.MkDevEnvSetup()

    node = mk.MkLicense()
    page = nav.add_page("License", hide="toc")
    page += node


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    nav_file = pathlib.Path(__file__).parent / "SUMMARY.md"
    root_nav = mk.MkNav()
    root_nav.parse.file(nav_file)
    table = prettyqtmarkdown.MarkdownWidget()
    table.set_markdown(root_nav)
    table.show()
    app.exec()
