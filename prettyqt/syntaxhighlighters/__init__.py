# -*- coding: utf-8 -*-

"""syntaxhighlighters module

contains some custom syntax highlighers
"""

from .jsonhighlighter import JsonHighlighter
from .pythonhighlighter import PythonHighlighter
from .yamlhighlighter import YamlHighlighter
from .xmlhighlighter import XmlHighlighter

__all__ = ["JsonHighlighter", "YamlHighlighter", "PythonHighlighter", "XmlHighlighter"]
