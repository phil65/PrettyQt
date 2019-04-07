# -*- coding: utf-8 -*-

"""syntaxhighlighters module

contains some custom syntax highlighers
"""

from .jsonhighlighter import JsonHighlighter
from .yamlhighlighter import YamlHighlighter
from .pythonhighlighter import PythonHighlighter


__all__ = ["JsonHighlighter", "YamlHighlighter", "PythonHighlighter"]
