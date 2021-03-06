"""Tests for `prettyqt` package."""

import re

from prettyqt import syntaxhighlighters


def test_jsonhighlighter():
    highlighter = syntaxhighlighters.JsonHighlighter()
    highlighter.highlightBlock('{"a": "b"}')


def test_pythonhighlighter():
    highlighter = syntaxhighlighters.PythonHighlighter()
    highlighter.highlightBlock("def test(): pass")


def test_yamlhighlighter():
    highlighter = syntaxhighlighters.YamlHighlighter()
    highlighter.highlightBlock("---\ntest:\n  - hallo")


def test_xmlhighlighter():
    highlighter = syntaxhighlighters.XmlHighlighter()
    highlighter.highlightBlock("<xml>test</xml>")


def test_markdownhighlighter():
    highlighter = syntaxhighlighters.MarkdownHighlighter()
    highlighter.highlightBlock("### Headline")


def test_regexmatchhighlighter():
    highlighter = syntaxhighlighters.RegexMatchHighlighter()
    text = "a123"
    prog = re.compile("[0-9]")
    spans = [m.span() for m in prog.finditer(text)]
    highlighter.set_spans(spans)
    highlighter.highlightBlock(text)
