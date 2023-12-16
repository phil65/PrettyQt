from __future__ import annotations

import logging
import pathlib
import sys

import prettyqt
from prettyqt import prettyqtmarkdown
import mknodes as mk


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def is_qt_module(module):
    return hasattr(module, "QT_MODULE")


def build_root(project: mk.Project):
    old = project.linkprovider
    provider = prettyqtmarkdown.QtLinkProvider(
        old.base_url, old.use_directory_urls, include_stdlib=True
    )
    provider.add_inv_file("docs/qt6.inv", "https://doc.qt.io/qtforpython/")
    project.linkprovider = provider
    project.theme.announcement_bar = mk.MkMetadataBadges("dependencies")
    nav_file = pathlib.Path(__file__).parent / "SUMMARY.md"
    root_nav = mk.MkNav()
    root_nav.parse.file(nav_file)
    project._root = root_nav
    root_nav.associated_project = project
    qt_docs = root_nav.add_doc(prettyqt, section_name="Qt-based modules")
    # simple/qt
    extra_docs = root_nav.add_doc(prettyqt, section_name="Additional modules")
    # octicons/plus-16
    populate_docs(qt_docs, is_qt_module)
    populate_docs(extra_docs, lambda x: not is_qt_module(x))

    dev_nav = root_nav.add_nav("Development")
    populate_dev_section(dev_nav)
    return root_nav


def populate_docs(doc_nav: mk.MkDoc, predicate):
    prettyqt.import_all()
    for submod in doc_nav.iter_modules(predicate=predicate):
        doc_nav.add_doc(submod, class_template="classpage_custom.jinja", flatten_nav=True)


def populate_dev_section(nav: mk.MkNav):
    page = nav.add_page("Changelog")
    page += mk.MkChangelog()

    page = nav.add_page("Dependencies", hide="toc")
    page += mk.MkDependencyTable()

    page = nav.add_page("Code of conduct")
    page += mk.MkCodeOfConduct()

    page = nav.add_page("Contributing")
    page += mk.MkCommitConventions()
    page += mk.MkPullRequestGuidelines()

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
