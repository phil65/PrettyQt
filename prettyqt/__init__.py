"""Top-level package for PrettyQt."""

__author__ = """Philipp Temminghoff"""
__email__ = "phil65@kodi.tv"
__version__ = "1.53.2"

# import os

# os.environ["PYTHONBREAKPOINT"] = "prettyqt.debug"


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
    from prettyqt import core, debugging, widgets, itemmodels, qtpandas  # noqa
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
    "bluetooth",
    "charts",
    "constants",
    "core",
    "animations",
    "itemdelegates",
    "itemmodels",
    "custom_network",
    "validators",
    "custom_widgets",
    "debugging",
    "designer",
    "eventfilters",
    "gui",
    "iconprovider",
    "ipython",
    "location",
    "multimedia",
    "multimediawidgets",
    "network",
    "openglwidgets",
    "pdf",
    "pdfwidgets",
    "positioning",
    "printsupport",
    "qml",
    "qthelp",
    "qtpandas",
    "quick",
    "quickwidgets",
    "scintilla",
    "scxml",
    "statemachine",
    "svg",
    "svgwidgets",
    "syntaxhighlighters",
    "texttospeech",
    "spatialaudio",
    "utils",
    "webchannel",
    "webenginecore",
    "webenginewidgets",
    "widgets",
]


if __name__ == "__main__":
    from importlib import metadata

    dist = metadata.distribution("prettyqt")
    show(["abc"])
