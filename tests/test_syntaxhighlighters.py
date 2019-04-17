#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import syntaxhighlighters


def test_jsonhighlighter():
    highlighter = syntaxhighlighters.JsonHighlighter()
    highlighter.highlightBlock('{"a": "b"}')


def test_pythonhighlighter():
    highlighter = syntaxhighlighters.PythonHighlighter()
    highlighter.highlightBlock("def test(): pass")


def test_yamlhighlighter():
    syntaxhighlighters.YamlHighlighter()
