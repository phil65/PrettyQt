from __future__ import annotations

from importlib import resources
import pathlib


ROOT_PATH = pathlib.Path(resources.files("prettyqt"))  # type: ignore

LOCALIZATION_PATH = ROOT_PATH / "localization"
THEMES_PATH = ROOT_PATH / "resources" / "themes"
RE_LEXER_PATH = (
    ROOT_PATH / "syntaxhighlighters" / "custom_highlighters" / "regularexpressionlexer.py"
)
ICON_FONT_PATH = ROOT_PATH / "iconprovider" / "fonts"

DOCS_PATH = ROOT_PATH.parent / "docs"
INV_FILE = DOCS_PATH / "qt6.inv"
