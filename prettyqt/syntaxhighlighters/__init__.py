"""syntaxhighlighters module.

contains some custom syntax highlighers
"""

from .highlightrule import HighlightRule
from .selectedwordhighlighter import SelectedWordHighlighter
from .jsonhighlighter import JsonHighlighter
from .pythonhighlighter import PythonHighlighter
from .yamlhighlighter import YamlHighlighter
from .regexmatchhighlighter import RegexMatchHighlighter
from .markdownhighlighter import MarkdownHighlighter
from .pygmentshighlighter import PygmentsHighlighter


__all__ = [
    "HighlightRule",
    "SelectedWordHighlighter",
    "JsonHighlighter",
    "YamlHighlighter",
    "PythonHighlighter",
    "RegexMatchHighlighter",
    "MarkdownHighlighter",
    "PygmentsHighlighter",
]
