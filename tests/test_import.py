"""Smoke test: the package imports and reports its version."""

import prettyqt


def test_package_imports() -> None:
    """The package can be imported and exposes a version string."""
    assert isinstance(prettyqt.__version__, str)
