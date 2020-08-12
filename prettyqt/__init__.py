# -*- coding: utf-8 -*-

"""Top-level package for PrettyQt."""

__author__ = """Philipp Temminghoff"""
__email__ = "phil65@kodi.tv"
__version__ = "0.115.0"


def debug():
    """Print the local variables in the caller's frame."""
    import inspect

    frame = inspect.currentframe()
    try:
        from prettyqt.objbrowser import objectbrowser

        print(frame.f_back.f_locals)
        objectbrowser.ObjectBrowser.browse(frame.f_back.f_locals)
    finally:
        del frame


__all__ = [
    "core",
    "gui",
    "widgets",
    "custom_widgets",
    "custom_models",
    "syntaxhighlighters",
    "charts",
    "webenginewidgets",
    "debug",
]
