# -*- coding: utf-8 -*-
"""
"""

from typing import Optional, Tuple, List
import re

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict

# IGNORECASE = QtCore.QRegularExpression.CaseInsensitiveOption
# MULTILINE = QtCore.QRegularExpression.MultilineOption
# DOTALL = QtCore.QRegularExpression.DotMatchesEverythingOption
# VERBOSE = QtCore.QRegularExpression.ExtendedPatternSyntaxOption

IGNORECASE = re.IGNORECASE
MULTILINE = re.MULTILINE
DOTALL = re.DOTALL
VERBOSE = re.VERBOSE

MAP = bidict({re.IGNORECASE: QtCore.QRegularExpression.CaseInsensitiveOption,
              re.MULTILINE: QtCore.QRegularExpression.MultilineOption,
              re.DOTALL: QtCore.QRegularExpression.DotMatchesEverythingOption,
              re.VERBOSE: QtCore.QRegularExpression.ExtendedPatternSyntaxOption})


def compile(pattern, flags=0):
    flag = QtCore.QRegularExpression.NoPatternOption
    for k, v in MAP.items():
        if k & flags:
            flag |= v
    return core.RegularExpression(pattern, flag)


def search(pattern, string, flags=0) -> Optional[core.RegularExpression]:
    compiled = compile(pattern, flags)
    return compiled.search(string)


def match(pattern, string, flags=0) -> Optional[core.RegularExpression]:
    compiled = compile(pattern, flags)
    return compiled.match(string)


def fullmatch(pattern, string, flags=0) -> Optional[core.RegularExpression]:
    compiled = compile(pattern, flags)
    return compiled.fullmatch(string)


# def split(pattern, string, maxsplit=0, flags=0) -> list:
#     compiled = compile(pattern, flags)
#     return compiled.split(string, maxsplit)


def findall(pattern, string, flags=0) -> List[str]:
    compiled = compile(pattern, flags)
    return compiled.findall(string)


def finditer(pattern, string, flags=0):
    compiled = compile(pattern, flags)
    return compiled.finditer(string)


def sub(pattern, repl, string, count=0, flags=0) -> str:
    compiled = compile(pattern, flags)
    return compiled.sub(repl, string, count)


def subn(pattern, repl, string, count=0, flags=0) -> Tuple[str, int]:
    compiled = compile(pattern, flags)
    return compiled.subn(repl, string, count)


def escape(pattern):
    dont_escape = ['!', '"', '%', "'", ',', '/', ':', ';', '<', '=', '>', '@', "`"]
    result = core.RegularExpression.escape(pattern)
    for i in dont_escape:
        result.replace(i, r"\i")
    assert result == re.escape(pattern)


if __name__ == "__main__":
    reg = compile("[0-9]+ [a-z] [0-9]+")
