# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Union, Callable, Optional, Iterator
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

MATCH_TYPES = bidict(normal=QtCore.QRegularExpression.NormalMatch,
                     prefer_complete=QtCore.QRegularExpression.PartialPreferCompleteMatch,
                     prefer_first=QtCore.QRegularExpression.PartialPreferFirstMatch,
                     no_match=QtCore.QRegularExpression.NoMatch)

MATCH_OPTIONS = bidict(none=QtCore.QRegularExpression.NoMatchOption,
                       anchored=QtCore.QRegularExpression.AnchoredMatchOption)


class RegularExpression(QtCore.QRegularExpression):

    def __init__(self, pattern="", flags=FLAGS["none"]):
        if isinstance(flags, int):
            flags = core.RegularExpression.PatternOptions(flags)
        super().__init__(pattern, flags)

    def __repr__(self):
        return f"RegularExpression({self.pattern()!r})"

    def __reduce__(self):
        return (self.__class__, (self.pattern(),))

    def globalMatch(self, *args, **kwargs) -> core.RegularExpressionMatchIterator:
        it = super().globalMatch(*args, **kwargs)
        return core.RegularExpressionMatchIterator(it)

    def global_match(self,
                     text: str,
                     offset: int = 0,
                     match_type: str = "normal",
                     anchored: bool = False):
        options = MATCH_OPTIONS["anchored"] if anchored else MATCH_OPTIONS["none"]
        return self.globalMatch(text, offset, MATCH_TYPES[match_type], options)

    def match(self, text, offset=0, match_type="normal", anchored=False):
        if isinstance(match_type, str):
            match_type = MATCH_TYPES[match_type]
        if isinstance(anchored, bool):
            options = MATCH_OPTIONS["anchored"] if anchored else MATCH_OPTIONS["none"]
        else:
            options = anchored
        match = super().match(text, offset, match_type, options)
        return core.RegularExpressionMatch(match)

    def finditer(self,
                 string: str,
                 pos: int = 0,
                 endpos: Optional[int] = None) -> Iterator[core.RegularExpressionMatch]:
        for match in self.globalMatch(string[:endpos], offset=pos):
            match.pos = pos
            match.endpos = endpos
            match.string = string
            yield match

    def findall(self,
                string: str,
                pos: int = 0,
                endpos: Optional[int] = None) -> list:
        matches = [m for m in self.globalMatch(string[:endpos], offset=pos)]
        return [m.groups() if len(m.groups()) > 1 else m.group(0) for m in matches]

    def subn(self, repl: Union[str, Callable], string: str, count: int = 0):
        result = string
        matches = self.global_match(string)
        matches = list(matches)
        if count > 0:
            matches = matches[:count]
        matches = list(reversed(matches))
        for m in matches:
            to_replace = repl if isinstance(repl, str) else repl(m)
            for j in range(self.groups):
                to_replace = to_replace.replace(fr"\g<{j}>", m.group(j))
            for j in self.groupindex.keys():
                to_replace = to_replace.replace(fr"\g<{j}>", m.group(j))
            result = result[:m.start()] + to_replace + result[m.end():]
        return (result, min(len(matches), count))

    def sub(self, repl: Union[str, Callable], string: str, count: int = 0):
        res = self.subn(repl, string, count)
        return res[0]

    def split(self, string: str, maxsplit: int = 0):
        pass

    @property
    def groups(self):
        return self.captureCount()

    @property
    def groupindex(self):
        return {k: i for i, k in enumerate(self.namedCaptureGroups()[1:], start=1)}


if __name__ == "__main__":
    reg = RegularExpression()
    reg.setPattern('-{1,2}')
