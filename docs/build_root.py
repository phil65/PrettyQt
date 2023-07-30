from __future__ import annotations

import logging
import sys

import prettyqt
from prettyqt import prettyqtmarkdown
import mknodes


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

ClassPage = prettyqtmarkdown.MkPrettyQtClassPage


def is_qt_module(module):
    return hasattr(module, "QT_MODULE")


def build_root(root_nav: mknodes.MkNav):
    qt_docs = root_nav.add_doc(prettyqt, section_name="Qt-based modules")
    extra_docs = root_nav.add_doc(prettyqt, section_name="Additional modules")
    populate_docs(qt_docs, is_qt_module)
    populate_docs(extra_docs, lambda x: not is_qt_module(x))

    dev_nav = root_nav.add_nav("Development")
    populate_dev_section(dev_nav)


def populate_docs(doc_nav: mknodes.MkDoc, predicate):
    prettyqt.import_all()
    for submod in doc_nav.iter_modules(predicate=predicate):
        subdoc = doc_nav.add_doc(submod, class_page=ClassPage, flatten_nav=True)
        subdoc.collect_classes()


def populate_dev_section(dev_nav: mknodes.MkNav):
    changelog_page = dev_nav.add_page("Changelog")
    changelog_page += mknodes.MkChangelog()
    dep_page = dev_nav.add_page("Dependencies", hide_toc=True)
    dep_page += prettyqtmarkdown.MkDependencyTable("prettyqt")


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    root_nav = mknodes.MkNav()
    build_root(root_nav)
    table = prettyqtmarkdown.MarkdownWidget()
    table.set_markdown(root_nav)
    table.show()
    app.exec()
