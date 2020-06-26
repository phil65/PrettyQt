# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Union, Callable, Optional
import re

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict

FLAGS = bidict(none=QtCore.QRegularExpression.NoPatternOption,
               ignorecase=QtCore.QRegularExpression.CaseInsensitiveOption,
               dotall=QtCore.QRegularExpression.DotMatchesEverythingOption,
               multiline=QtCore.QRegularExpression.MultilineOption,
               verbose=QtCore.QRegularExpression.ExtendedPatternSyntaxOption,
               inverted_greedyness=QtCore.QRegularExpression.InvertedGreedinessOption,
               dont_capture=QtCore.QRegularExpression.DontCaptureOption,
               unicode=QtCore.QRegularExpression.UseUnicodePropertiesOption)

MAP = bidict({re.IGNORECASE: QtCore.QRegularExpression.CaseInsensitiveOption,
              re.MULTILINE: QtCore.QRegularExpression.MultilineOption,
              re.DOTALL: QtCore.QRegularExpression.DotMatchesEverythingOption,
              re.VERBOSE: QtCore.QRegularExpression.ExtendedPatternSyntaxOption})


class RegularExpression(QtCore.QRegularExpression):

    def __repr__(self):
        return f"RegularExpression({self.pattern()!r})"

    def __reduce__(self):
        return (self.__class__, (self.pattern(),))

    def matches_in_text(self, text):
        result = self.match(text)
        while result.hasMatch():
            length = result.capturedLength(0)
            index = result.capturedStart(0)
            yield index, length
            result = self.match(text, index + length)

    def match(self, *args, **kwargs):
        match = super().match(*args, **kwargs)
        return core.RegularExpressionMatch(match)

    def globalMatch(self, *args, **kwargs):
        it = super().globalMatch(*args, **kwargs)
        return core.RegularExpressionMatchIterator(it)

    def finditer(self, string: str, pos: int = 0, endpos: Optional[int] = None):
        for match in self.globalMatch(string[:endpos], offset=pos):
            match.pos = pos
            match.endpos = endpos
            match.string = string
            yield match

    def findall(self, string: str, pos: int = 0, endpos: Optional[int] = None):
        matches = [m for m in self.globalMatch(string[:endpos], offset=pos)]
        return [m.groups() if len(m.groups()) > 1 else m.group(0) for m in matches]

    def sub(self, repl: Union[str, Callable], string: str, count: int = 0):
        pass

    def split(self, string: str, maxsplit: int = 0):
        pass


if __name__ == "__main__":
    reg = RegularExpression()
    reg.setPattern("[0-9]+ [a-z] [0-9]+")
    for i in reg.matches_in_text("033 a 03444"):
        print(i)
