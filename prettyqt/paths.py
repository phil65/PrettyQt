from importlib import resources
import pathlib


ROOT_PATH = pathlib.Path(resources.files("prettyqt"))  # type: ignore

LOCALIZATION_PATH = ROOT_PATH / "localization"
THEMES_PATH = ROOT_PATH / "themes"
RE_LEXER_PATH = (
    ROOT_PATH / "syntaxhighlighters" / "pygments" / "regularexpressionlexer.py"
)
ICON_FONT_PATH = ROOT_PATH / "iconprovider" / "fonts"
