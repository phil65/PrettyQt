from __future__ import annotations

from collections.abc import Callable, Iterator
import re

from typing import Literal

import bidict as bd

from prettyqt import core
from prettyqt.utils import bidict, get_repr


RE_MAP = bd.bidict(
    {
        re.IGNORECASE: core.QRegularExpression.PatternOption.CaseInsensitiveOption,
        re.MULTILINE: core.QRegularExpression.PatternOption.MultilineOption,
        re.DOTALL: core.QRegularExpression.PatternOption.DotMatchesEverythingOption,
        re.VERBOSE: core.QRegularExpression.PatternOption.ExtendedPatternSyntaxOption,
    }
)

mod = core.QRegularExpression

PatternOptionStr = Literal[
    "none",
    "ignorecase",
    "dotall",
    "multiline",
    "verbose",
    "inverted_greedyness",
    "dont_capture",
    "unicode",
]

PATTERN_OPTIONS: bidict[PatternOptionStr, mod.PatternOption] = bidict(
    none=mod.PatternOption.NoPatternOption,
    ignorecase=mod.PatternOption.CaseInsensitiveOption,
    dotall=mod.PatternOption.DotMatchesEverythingOption,
    multiline=mod.PatternOption.MultilineOption,
    verbose=mod.PatternOption.ExtendedPatternSyntaxOption,
    inverted_greedyness=mod.PatternOption.InvertedGreedinessOption,
    dont_capture=mod.PatternOption.DontCaptureOption,
    unicode=mod.PatternOption.UseUnicodePropertiesOption,
)

MatchTypeStr = Literal["normal", "prefer_complete", "prefer_first", "no_match"]

MATCH_TYPE: bidict[MatchTypeStr, mod.MatchType] = bidict(
    normal=mod.MatchType.NormalMatch,
    prefer_complete=mod.MatchType.PartialPreferCompleteMatch,
    prefer_first=mod.MatchType.PartialPreferFirstMatch,
    no_match=mod.MatchType.NoMatch,
)

MatchOptionStr = Literal["none", "anchored"]

MATCH_OPTIONS: bidict[MatchOptionStr, mod.MatchOption] = bidict(
    none=mod.MatchOption.NoMatchOption,
    anchored=mod.MatchOption.AnchorAtOffsetMatchOption,  # type: ignore
)


class RegularExpression(core.QRegularExpression):
    def __init__(
        self,
        pattern: str | core.QRegularExpression | re.Pattern = "",
        flags: core.QRegularExpression.PatternOption = PATTERN_OPTIONS["none"],
    ):
        match pattern:
            case core.QRegularExpression():
                super().__init__(pattern)
            case re.Pattern():
                qflag = self.PatternOption(0)
                for flag in re.RegexFlag(pattern.flags):
                    if flag in RE_MAP:
                        qflag |= RE_MAP[flag]
                super().__init__(pattern.pattern, qflag)
            case _:
                if isinstance(flags, int):
                    flags = core.RegularExpression.PatternOption(flags)  # type: ignore
                super().__init__(pattern, flags)  # type: ignore

    def __repr__(self):
        return get_repr(self, self.pattern())

    @property
    def _pattern(self):
        return self.pattern()

    __match_args__ = ("_pattern",)

    def __reduce__(self):
        return type(self), (self.pattern(), self.flags)

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
        match_type: MatchTypeStr | core.QRegularExpression.MatchType = "normal",
        anchored: bool = False,
    ) -> core.RegularExpressionMatch:
        typ = MATCH_TYPE[match_type] if isinstance(match_type, str) else match_type
        if isinstance(anchored, bool):
            options = MATCH_OPTIONS["anchored"] if anchored else MATCH_OPTIONS["none"]
        else:
            options = anchored
        match = super().match(text, offset, typ, options)
        return core.RegularExpressionMatch(match)

    def fullmatch(
        self, string: str, pos: int = 0, endpos: int | None = None
    ) -> core.RegularExpressionMatch | None:
        if endpos:
            string = string[:endpos]
        match = super().match(string, pos)
        if match.hasMatch() and len(string) == match.end() - match.start():
            return core.RegularExpressionMatch(match)
        else:
            return None

    def finditer(
        self, string: str, pos: int = 0, endpos: int | None = None
    ) -> Iterator[core.RegularExpressionMatch]:
        for match in self.globalMatch(string[:endpos], offset=pos):
            match.pos = pos
            match.endpos = endpos
            match.string = string
            yield match

    def findall(self, string: str, pos: int = 0, endpos: int | None = None) -> list:
        matches = list(self.globalMatch(string[:endpos], offset=pos))
        return [m.groups() if len(m.groups()) > 1 else m.group(0) for m in matches]

    def subn(self, repl: str | Callable, string: str, count: int = 0) -> tuple[str, int]:
        result = string
        matches = self.global_match(string)
        matches = list(matches)
        if count > 0:
            matches = matches[:count]
        matches = list(reversed(matches))
        for m in matches:
            to_replace = repl if isinstance(repl, str) else repl(m)
            for j in range(self.groups):
                to_replace = to_replace.replace(rf"\g<{j}>", m.group(j))
            for k in self.groupindex:
                to_replace = to_replace.replace(rf"\g<{k}>", m.group(k))
            result = result[: m.start()] + to_replace + result[m.end() :]
        return (result, min(len(matches), count))

    def sub(self, repl: str | Callable, string: str, count: int = 0) -> str:
        res = self.subn(repl, string, count)
        return res[0]

    def search(self, string: str, pos: int = 0, endpos: int | None = None):
        match = super().match(string[:endpos], pos)
        return match if match.hasMatch() else None

    def split(self, string: str, maxsplit: int = 0):
        raise NotImplementedError
        # result = []
        # matches = self.global_match(string)
        # matches = list(matches)
        # if 0 < maxsplit <= len(matches):
        #     remainder = string[matches[maxsplit - 1].end() :]
        # else:
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
    def groupindex(self) -> dict[str, int]:
        return {k: i for i, k in enumerate(self.namedCaptureGroups()[1:], start=1)}

    @property
    def flags(self) -> core.QRegularExpression.PatternOption:
        return self.patternOptions()

    def to_py_pattern(self) -> re.Pattern:
        flag = re.RegexFlag(0)
        for qflag in self.patternOptions():
            if qflag in RE_MAP.inverse:
                flag |= RE_MAP.inverse[qflag]
        return re.compile(self.pattern(), flag)


if __name__ == "__main__":
    pattern = re.compile("test", flags=re.MULTILINE)
    reg = RegularExpression(pattern)
