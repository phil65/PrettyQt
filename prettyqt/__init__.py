"""Top-level package for PrettyQt."""

__author__ = """Philipp Temminghoff"""
__email__ = "phil65@kodi.tv"
__version__ = "1.42.0"

# import os

# os.environ["PYTHONBREAKPOINT"] = "prettyqt.debug"


def debug():
    """Print the local variables in the caller's frame."""
    import inspect

    frame = inspect.currentframe()
    stack = inspect.stack()
    if frame is None or frame.f_back is None:
        del frame
        raise RuntimeError()
    try:
        from prettyqt.objbrowser import objectbrowser

        objectbrowser.ObjectBrowser.browse(frame.f_back.f_globals, stack)
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


if __name__ == "__main__":
    debug()
