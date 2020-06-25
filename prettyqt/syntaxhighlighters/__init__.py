# -*- coding: utf-8 -*-

"""syntaxhighlighters module

contains some custom syntax highlighers
"""

from .jsonhighlighter import JsonHighlighter
from .pythonhighlighter import PythonHighlighter
from .yamlhighlighter import YamlHighlighter
from .xmlhighlighter import XmlHighlighter
from .regexmatchhighlighter import RegexMatchHighlighter

__all__ = ["JsonHighlighter",
           "YamlHighlighter",
           "PythonHighlighter",
           "XmlHighlighter",
           "RegexMatchHighlighter"]
