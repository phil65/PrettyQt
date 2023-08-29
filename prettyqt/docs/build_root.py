from __future__ import annotations

import logging
import pathlib
import sys

import prettyqt
from prettyqt import prettyqtmarkdown
import mknodes


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

ClassPage = prettyqtmarkdown.MkPrettyQtClassPage


def is_qt_module(module):
    return hasattr(module, "QT_MODULE")


def build_root(project: mknodes.Project):
    project.module = prettyqt
    nav_file = pathlib.Path(__file__).parent / "SUMMARY.md"
    root_nav = mknodes.MkNav.from_file(nav_file, section=None)
    project._root = root_nav
    root_nav._associated_project = project
    qt_docs = root_nav.add_doc(prettyqt, section_name="Qt-based modules")
    # simple/qt
    extra_docs = root_nav.add_doc(prettyqt, section_name="Additional modules")
    # octicons/plus-16
    populate_docs(qt_docs, is_qt_module)
    populate_docs(extra_docs, lambda x: not is_qt_module(x))

    dev_nav = root_nav.add_nav("Development")
    populate_dev_section(dev_nav)
    return root_nav


def populate_docs(doc_nav: mknodes.MkDoc, predicate):
    prettyqt.import_all()
    for submod in doc_nav.iter_modules(predicate=predicate):
        subdoc = doc_nav.add_doc(submod, class_page=ClassPage, flatten_nav=True)
        subdoc.collect_classes()


def populate_dev_section(nav: mknodes.MkNav):
    page = nav.add_page("Changelog")
    page += mknodes.MkChangelog()

    page = nav.add_page("Dependencies", hide_toc=True)
    page += mknodes.MkDependencyTable()

    page = nav.add_page("Code of conduct")
    page += mknodes.MkCodeOfConduct()

    page = nav.add_page("Contributing")
    page += mknodes.MkCommitConventions()
    page += mknodes.MkPullRequestGuidelines()

    page = nav.add_page("Setting up the environment")
    page += mknodes.MkDevEnvSetup()

    node = mknodes.MkLicense()
    page = nav.add_page("License", hide_toc=True)
    page += node


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    nav_file = pathlib.Path(__file__).parent / "SUMMARY.md"
    root_nav = mknodes.MkNav.from_file(nav_file, section=None)
    table = prettyqtmarkdown.MarkdownWidget()
    table.set_markdown(root_nav)
    table.show()
    app.exec()
