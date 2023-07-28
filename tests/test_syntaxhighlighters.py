"""Tests for `prettyqt` package."""

import re

from prettyqt import gui, syntaxhighlighters


def test_jsonhighlighter():
    doc = gui.TextDocument()
    highlighter = syntaxhighlighters.JsonHighlighter(doc)
    highlighter.highlightBlock('{"a": "b"}')


def test_pythonhighlighter():
    doc = gui.TextDocument()
    highlighter = syntaxhighlighters.PythonHighlighter(doc)
    highlighter.highlightBlock("def test(): pass")


def test_yamlhighlighter():
    doc = gui.TextDocument()
    highlighter = syntaxhighlighters.YamlHighlighter(doc)
    highlighter.highlightBlock("---\ntest:\n  - hallo")


def test_markdownhighlighter():
    doc = gui.TextDocument()
    highlighter = syntaxhighlighters.MarkdownHighlighter(doc)
    highlighter.highlightBlock("### Headline")


def test_regexmatchhighlighter():
    doc = gui.TextDocument()
    highlighter = syntaxhighlighters.RegexMatchHighlighter(doc)
    text = "a123"
    prog = re.compile("[0-9]")
    spans = [m.span() for m in prog.finditer(text)]
    highlighter.set_spans(spans)
    highlighter.highlightBlock(text)
