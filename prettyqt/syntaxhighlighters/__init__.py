"""syntaxhighlighters module.

contains some custom syntax highlighers
"""

from .highlightrule import HighlightRule
from .baserulesyntaxhighlighter import BaseRuleSyntaxHighlighter
from .jsonhighlighter import JsonHighlighter
from .markdownhighlighter import MarkdownHighlighter
from .pygmentshighlighter import PygmentsHighlighter
from .pythonhighlighter import PythonHighlighter
from .regexmatchhighlighter import RegexMatchHighlighter
from .selectedwordhighlighter import SelectedWordHighlighter
from .yamlhighlighter import YamlHighlighter


__all__ = [
    "HighlightRule",
    "BaseRuleSyntaxHighlighter",
    "SelectedWordHighlighter",
    "JsonHighlighter",
    "YamlHighlighter",
    "PythonHighlighter",
    "RegexMatchHighlighter",
    "MarkdownHighlighter",
    "PygmentsHighlighter",
]
