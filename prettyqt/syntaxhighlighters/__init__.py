"""syntaxhighlighters module.

contains some custom syntax highlighers
"""

from .highlightrule import HighlightRule
from .jsonhighlighter import JsonHighlighter
from .pythonhighlighter import PythonHighlighter
from .yamlhighlighter import YamlHighlighter
from .xmlhighlighter import XmlHighlighter
from .regexmatchhighlighter import RegexMatchHighlighter
from .markdownhighlighter import MarkdownHighlighter
from .pygmentshighlighter import PygmentsHighlighter


__all__ = [
    "HighlightRule",
    "JsonHighlighter",
    "YamlHighlighter",
    "PythonHighlighter",
    "XmlHighlighter",
    "RegexMatchHighlighter",
    "MarkdownHighlighter",
    "PygmentsHighlighter",
]
