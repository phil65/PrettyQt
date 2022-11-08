"""Top-level package for PrettyQt."""

__author__ = """Philipp Temminghoff"""
__email__ = "phil65@kodi.tv"
__version__ = "0.190.7"


def debug():
    """Print the local variables in the caller's frame."""
    import inspect

    frame = inspect.currentframe()
    if frame is None or frame.f_back is None:
        del frame
        raise RuntimeError()
    try:
        from prettyqt.objbrowser import objectbrowser

        objectbrowser.ObjectBrowser.browse(frame.f_back.f_globals)
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
