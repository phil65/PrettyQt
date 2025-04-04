"""Top-level package for PrettyQt."""

__author__ = """Philipp Temminghoff"""
__email__ = "phil65@kodi.tv"
__version__ = "1.59.1"

# import os

# os.environ["PYTHONBREAKPOINT"] = "prettyqt.debug"


def import_all():
    import importlib
    import logging
    from prettyqt import qt

    logger = logging.getLogger(__name__)
    mods = []
    for mod in __all__:
        try:
            mod = importlib.import_module(f"prettyqt.{mod}")
            mods.append(mod)
        except ImportError:
            logger.warning("%s not available. binding: %s", mod, qt.API)
    return mods


def debug():
    """Print the local variables in the caller's frame."""
    import inspect

    frame = inspect.currentframe()
    stack = inspect.stack()
    if frame is None or frame.f_back is None:
        del frame
        raise RuntimeError
    try:
        from prettyqt import custom_widgets, widgets

        debug.app = widgets.app(organization_name="phil65", application_name="Prettyqt")
        objectbrowser = custom_widgets.ObjectBrowser(frame.f_back.f_globals, stack)
        objectbrowser.show()
        debug.app.exec()
    finally:
        del frame


def show(item):
    from prettyqt import core, debugging, widgets, itemmodels  # noqa
    from prettyqt.utils import classhelpers

    debug.app = widgets.app(organization_name="phil65", application_name="Prettyqt")
    for klass in classhelpers.get_subclasses(core.QAbstractItemModel):
        if "supports" in klass.__dict__ and klass.supports(item):
            if issubclass(klass, core.QAbstractTableModel):
                viewer = widgets.TableView()
            else:
                viewer = widgets.TreeView()
            instance = klass(item)
            viewer.set_model(instance)
            viewer.show()
            debug.app.exec()
            break
    debug.app.exec()


__all__ = [
    "animations",
    "bluetooth",
    "charts",
    "constants",
    "core",
    "custom_network",
    "custom_widgets",
    "debugging",
    "designer",
    "docs",
    "eventfilters",
    "gui",
    "iconprovider",
    "ipython",
    "itemdelegates",
    "itemmodels",
    "location",
    "multimedia",
    "multimediawidgets",
    "network",
    "openglwidgets",
    "pdf",
    "pdfwidgets",
    "positioning",
    "prettyqtmarkdown",
    "printsupport",
    "qml",
    "qthelp",
    "quick",
    "quickwidgets",
    "scintilla",
    "scxml",
    "spatialaudio",
    "statemachine",
    "svg",
    "svgwidgets",
    "syntaxhighlighters",
    "texttospeech",
    "utils",
    "validators",
    "webchannel",
    "webenginecore",
    "webenginewidgets",
    "widgets",
]


if __name__ == "__main__":
    from importlib import metadata

    dist = metadata.distribution("prettyqt")
    show(["abc"])
