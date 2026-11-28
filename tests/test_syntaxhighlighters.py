"""Tests for `prettyqt` package."""

import re

import pytest

from prettyqt import gui, syntaxhighlighters


def test_jsonhighlighter():
    doc = gui.QTextDocument()
    highlighter = syntaxhighlighters.JsonHighlighter(doc)
    highlighter.highlightBlock('{"a": "b\\"c"}')


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


def test_regexmatchhighlighter_multiline():
    doc = gui.QTextDocument("abc\ndef\nghi")
    highlighter = syntaxhighlighters.RegexMatchHighlighter(doc)
    # Span covering "bc\ndef\ngh" -> positions 1..10
    highlighter.set_spans([(1, 10)])
    block1 = doc.findBlockByNumber(1)
    block2 = doc.findBlockByNumber(2)
    assert block1.layout().formats()
    end_formats = block2.layout().formats()
    assert end_formats
    assert end_formats[0].start == 0
    assert end_formats[0].length == 2  # noqa: PLR2004


def test_pygmentshighlighter_stylesheet_preserves_document(qapp):
    pytest.importorskip("pygments")
    doc = gui.QTextDocument("def foo():\n    return 42\n")
    highlighter = syntaxhighlighters.PygmentsHighlighter(doc, lexer="python")
    highlighter.set_style_sheet(".k { color: #ff0000; }")
    highlighter.rehighlight()
    assert doc.toPlainText() == "def foo():\n    return 42\n"


def test_selectedwordhighlighter_standalone_and_escape(qapp):
    doc = gui.QTextDocument("foo.bar(1) and fooXbar(1)")
    highlighter = syntaxhighlighters.SelectedWordHighlighter(doc)
    highlighter.set_selection_mode("all")
    highlighter.set_selection_term("foo.bar(1)")
    formats = doc.findBlockByNumber(0).layout().formats()
    assert len(formats) == 1
    assert formats[0].start == 0
    assert formats[0].length == len("foo.bar(1)")
