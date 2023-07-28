"""Tests for `prettyqt` package."""

import re

import pytest

from prettyqt import gui, qt, syntaxhighlighters


@pytest.mark.skipif(qt.API == "pyside6", reason="X11 connection break")
def test_jsonhighlighter():
    doc = gui.QTextDocument()
    highlighter = syntaxhighlighters.JsonHighlighter(doc)
    highlighter.highlightBlock('{"a": "b"}')


def test_pythonhighlighter():
    doc = gui.QTextDocument()
    highlighter = syntaxhighlighters.PythonHighlighter(doc)
    highlighter.highlightBlock("def test(): pass")


def test_yamlhighlighter():
    doc = gui.QTextDocument()
    highlighter = syntaxhighlighters.YamlHighlighter(doc)
    highlighter.highlightBlock("---\ntest:\n  - hallo")


def test_markdownhighlighter():
    doc = gui.QTextDocument()
    highlighter = syntaxhighlighters.MarkdownHighlighter(doc)
    highlighter.highlightBlock("### Headline")


def test_regexmatchhighlighter():
    doc = gui.QTextDocument()
    highlighter = syntaxhighlighters.RegexMatchHighlighter(doc)
    text = "a123"
    prog = re.compile("[0-9]")
    spans = [m.span() for m in prog.finditer(text)]
    highlighter.set_spans(spans)
    highlighter.highlightBlock(text)
