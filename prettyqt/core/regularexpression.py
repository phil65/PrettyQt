from __future__ import annotations

from typing import Callable, Dict, Iterator, Literal, Optional, Tuple, Union

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


FLAGS = bidict(
    none=QtCore.QRegularExpression.NoPatternOption,
    ignorecase=QtCore.QRegularExpression.CaseInsensitiveOption,
    dotall=QtCore.QRegularExpression.DotMatchesEverythingOption,
    multiline=QtCore.QRegularExpression.MultilineOption,
    verbose=QtCore.QRegularExpression.ExtendedPatternSyntaxOption,
    inverted_greedyness=QtCore.QRegularExpression.InvertedGreedinessOption,
    dont_capture=QtCore.QRegularExpression.DontCaptureOption,
    unicode=QtCore.QRegularExpression.UseUnicodePropertiesOption,
)

MATCH_TYPE = bidict(
    normal=QtCore.QRegularExpression.NormalMatch,
    prefer_complete=QtCore.QRegularExpression.PartialPreferCompleteMatch,
    prefer_first=QtCore.QRegularExpression.PartialPreferFirstMatch,
    no_match=QtCore.QRegularExpression.NoMatch,
)

MatchTypeStr = Literal["normal", "prefer_complete", "prefer_first", "no_match"]

MATCH_OPTIONS = bidict(
    none=QtCore.QRegularExpression.NoMatchOption,
    anchored=QtCore.QRegularExpression.AnchoredMatchOption,
)


class RegularExpression(QtCore.QRegularExpression):
    def __init__(
        self,
        pattern: Union[str, QtCore.QRegularExpression] = "",
        flags: QtCore.QRegularExpression.PatternOption = FLAGS["none"],
    ):
        if isinstance(pattern, QtCore.QRegularExpression):
            super().__init__(pattern)
        else:
            if isinstance(flags, int):
                flags = core.RegularExpression.PatternOptions(flags)  # type: ignore
            super().__init__(pattern, flags)  # type: ignore

    def __repr__(self):
        return f"{type(self).__name__}({self.pattern()!r})"

    def __reduce__(self):
        return type(self), (self.pattern(), int(self.flags))

    def globalMatch(self, *args, **kwargs) -> core.RegularExpressionMatchIterator:
        it = super().globalMatch(*args, **kwargs)
        return core.RegularExpressionMatchIterator(it)

    def global_match(
        self,
        text: str,
        offset: int = 0,
        match_type: MatchTypeStr = "normal",
        anchored: bool = False,
    ):
        options = MATCH_OPTIONS["anchored"] if anchored else MATCH_OPTIONS["none"]
        return self.globalMatch(text, offset, MATCH_TYPE[match_type], options)

    def match(  # type: ignore
        self,
        text: str,
        offset: int = 0,
        match_type: Union[MatchTypeStr, QtCore.QRegularExpression.MatchType] = "normal",
        anchored: bool = False,
    ) -> core.RegularExpressionMatch:
        if isinstance(match_type, str):
            typ = MATCH_TYPE[match_type]
        else:
            typ = match_type
        if isinstance(anchored, bool):
            options = MATCH_OPTIONS["anchored"] if anchored else MATCH_OPTIONS["none"]
        else:
            options = anchored
        match = super().match(text, offset, typ, options)
        return core.RegularExpressionMatch(match)

    def fullmatch(
        self, string: str, pos: int = 0, endpos: Optional[int] = None
    ) -> Optional[core.RegularExpressionMatch]:
        if endpos:
            string = string[:endpos]
        match = super().match(string, pos)
        if match.hasMatch() and len(string) == match.end() - match.start():
            return core.RegularExpressionMatch(match)
        else:
            return None

    def finditer(
        self, string: str, pos: int = 0, endpos: Optional[int] = None
    ) -> Iterator[core.RegularExpressionMatch]:
        for match in self.globalMatch(string[:endpos], offset=pos):
            match.pos = pos
            match.endpos = endpos
            match.string = string
            yield match

    def findall(self, string: str, pos: int = 0, endpos: Optional[int] = None) -> list:
        matches = list(self.globalMatch(string[:endpos], offset=pos))
        return [m.groups() if len(m.groups()) > 1 else m.group(0) for m in matches]

    def subn(
        self, repl: Union[str, Callable], string: str, count: int = 0
    ) -> Tuple[str, int]:
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
            for k in self.groupindex.keys():
                to_replace = to_replace.replace(fr"\g<{k}>", m.group(k))
            result = result[: m.start()] + to_replace + result[m.end() :]
        return (result, min(len(matches), count))

    def sub(self, repl: Union[str, Callable], string: str, count: int = 0) -> str:
        res = self.subn(repl, string, count)
        return res[0]

    def search(self, string: str, pos: int = 0, endpos: Optional[int] = None):
        match = super().match(string[:endpos], pos)
        return match if match.hasMatch() else None

    def split(self, string: str, maxsplit: int = 0):
        raise NotImplementedError()
        # result = list()
        # matches = self.global_match(string)
        # matches = list(matches)
        # if 0 < maxsplit <= len(matches):
        #     remainder = string[matches[maxsplit - 1].end() :]
        #     print(remainder)
        # else:
        #     print(None)
        #     remainder = None
        # if maxsplit > 0:
        #     matches = matches[:maxsplit]
        # prev_match = None
        # m = matches[0]
        # if m.start() == 0:
        #     result.append("")
        # else:
        #     result.append(string[0 : m.start()])
        # for g in m.groups():
        #     result.append(g)
        # prev_match = m
        # for m in matches[1:]:
        #     result.append(string[prev_match.end() : m.start()])
        #     for g in m.groups():
        #         result.append(g)
        #     if m.end() == len(string):
        #         result.append("")
        #     prev_match = m
        # if remainder:
        #     result.append(remainder)
        # return result

    @property
    def groups(self) -> int:
        return self.captureCount()

    @property
    def groupindex(self) -> Dict[str, int]:
        return {k: i for i, k in enumerate(self.namedCaptureGroups()[1:], start=1)}

    @property
    def flags(self):
        return self.patternOptions()


if __name__ == "__main__":
    reg = RegularExpression()
    reg.setPattern("-{1,2}")
