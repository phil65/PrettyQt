from __future__ import annotations

from collections.abc import Iterator
import re
from typing import Any, Callable

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


# IGNORECASE = QtCore.QRegularExpression.CaseInsensitiveOption
# MULTILINE = QtCore.QRegularExpression.MultilineOption
# DOTALL = QtCore.QRegularExpression.DotMatchesEverythingOption
# VERBOSE = QtCore.QRegularExpression.ExtendedPatternSyntaxOption

DONT_ESCAPE = {"!", '"', "%", "'", ",", "/", ":", ";", "<", "=", ">", "@", "`"}

IGNORECASE = re.IGNORECASE
MULTILINE = re.MULTILINE
DOTALL = re.DOTALL
VERBOSE = re.VERBOSE

MAP = bidict(
    {
        re.IGNORECASE: QtCore.QRegularExpression.CaseInsensitiveOption,
        re.MULTILINE: QtCore.QRegularExpression.MultilineOption,
        re.DOTALL: QtCore.QRegularExpression.DotMatchesEverythingOption,
        re.VERBOSE: QtCore.QRegularExpression.ExtendedPatternSyntaxOption,
    }
)


class Match(core.RegularExpressionMatch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.string = None
        self.pos = None
        self.endpos = None

    def __repr__(self):
        return f"<re.Match object; span={self.span()}, match={self.groups()}>"

    def __getitem__(self, item: str | int) -> str:
        return self.captured(item)

    def group(self, *groups: str | int) -> tuple | str:
        if len(groups) > 1:
            return tuple(self.captured(i) for i in groups)
        if len(groups) == 0:
            return self.captured(0)
        return self.captured(groups[0])

    def groups(self, default=None) -> tuple:
        if self.lastindex is None:
            return tuple()
        return tuple(
            self.group(i) if i <= self.lastindex else default
            for i in range(self.re.captureCount())
        )

    def groupdict(self, default=None) -> dict[str, Any]:
        if self.lastindex is None:
            return {}
        groups = [
            self.group(i) if i <= self.lastindex else default
            for i in range(self.re.captureCount())
        ]
        names = self.re.namedCaptureGroups()
        return {names[i]: groups[i] for i in range(self.re.captureCount())}

    def start(self, group: int = 0) -> int:
        return self.capturedStart(group)

    def end(self, group: int = 0) -> int:
        return self.capturedEnd(group)

    def span(self, group: int = 0) -> tuple[int, int]:
        return (self.capturedStart(group), self.capturedEnd(group))

    @property
    def lastindex(self) -> int | None:
        idx = self.lastCapturedIndex()
        return None if idx == -1 else idx

    @property
    def lastgroup(self) -> str | None:
        if self.lastCapturedIndex() == -1:
            return None
        return self.re.namedCaptureGroups()[self.lastCapturedIndex()]

    @property
    def re(self) -> QtCore.QRegularExpression:
        return self.regularExpression()

    @property
    def partial(self) -> bool:
        return self.hasPartialMatch()


class Pattern(core.RegularExpression):
    def __init__(self, pattern: str = "", flags: int = 0):
        flag = QtCore.QRegularExpression.NoPatternOption
        for k, v in MAP.items():
            if k & flags:
                flag |= v
        super().__init__(pattern, flag)

    def match(  # type: ignore[override]
        self, string: str, pos: int = 0, endpos: int | None = None
    ) -> Match | None:
        match = super().match(string[:endpos], pos)
        return Match(match) if match.hasMatch() else None

    def fullmatch(
        self, string: str, pos: int = 0, endpos: int | None = None
    ) -> Match | None:
        if endpos:
            string = string[:endpos]
        match = super().match(string, pos)
        if match.hasMatch() and len(string) == match.end() - match.start():
            return Match(match)
        else:
            return None

    def finditer(
        self, string: str, pos: int = 0, endpos: int | None = None
    ) -> Iterator[Match]:
        for match in self.globalMatch(string[:endpos], offset=pos):
            match.pos = pos
            match.endpos = endpos
            match.string = string
            yield match

    def findall(self, string: str, pos: int = 0, endpos: int | None = None) -> list:
        matches = list(self.globalMatch(string[:endpos], offset=pos))
        return [m.groups() if len(m.groups()) > 1 else m.group(0) for m in matches]

    def subn(self, repl: str | Callable, string: str, count: int = 0):
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
            for k, v in self.groupindex.items():
                to_replace = to_replace.replace(rf"\g<{k}>", m.group(v))
            result = result[: m.start()] + to_replace + result[m.end() :]
        return (result, min(len(matches), count))

    def sub(self, repl: str | Callable, string: str, count: int = 0):
        res = self.subn(repl, string, count)
        return res[0]

    def search(self, string: str, pos: int = 0, endpos: int | None = None):
        match = super().match(string[:endpos], pos)
        return match if match.hasMatch() else None

    def split(self, string: str, maxsplit: int = 0):
        result = list()
        matches = self.global_match(string)
        matches = list(matches)
        prev_match = None
        num_split = min(maxsplit, len(matches)) if maxsplit > 0 else len(matches)
        if matches[0].start() == 0:
            result.append("")
        else:
            result.append(string[0 : matches[0].start()])
        for m in matches[:num_split]:
            if prev_match is not None:
                result.append(string[prev_match.end() : m.start()])
            for g in m.groups():
                result.append(g)
            prev_match = m
        if matches[num_split - 1].end() == len(string):
            result.append("")
        if maxsplit > 0:
            remainder_start = matches[maxsplit].end()
            result.append(string[remainder_start:])
        return result

    @property
    def groups(self) -> int:
        return self.captureCount()

    @property
    def groupindex(self) -> dict[str, int]:
        return {k: i for i, k in enumerate(self.namedCaptureGroups()[1:], start=1)}

    @property
    def flags(self):
        return self.patternOptions()


def compile(pattern: str, flags: int = 0) -> Pattern:
    return Pattern(pattern, flags)


def search(pattern: str, string: str, flags: int = 0) -> core.RegularExpression | None:
    compiled = compile(pattern, flags)
    match = compiled.search(string)
    return match


def match(pattern: str, string: str, flags: int = 0) -> core.RegularExpression | None:
    compiled = compile(pattern, flags)
    return compiled.match(string)


def fullmatch(pattern: str, string: str, flags: int = 0) -> core.RegularExpression | None:
    compiled = compile(pattern, flags)
    return compiled.fullmatch(string)


# def split(pattern: str, string: str, maxsplit=0, flags=0) -> list:
#     compiled = compile(pattern, flags)
#     return compiled.split(string, maxsplit)


def findall(pattern: str, string: str, flags: int = 0) -> list[str]:
    compiled = compile(pattern, flags)
    return compiled.findall(string)


def finditer(pattern, string: str, flags: int = 0):
    compiled = compile(pattern, flags)
    return compiled.finditer(string)


def sub(pattern: str, repl: str, string: str, count: int = 0, flags: int = 0) -> str:
    compiled = compile(pattern, flags)
    return compiled.sub(repl, string, count)


def subn(
    pattern: str, repl: str, string: str, count: int = 0, flags: int = 0
) -> tuple[str, int]:
    compiled = compile(pattern, flags)
    return compiled.subn(repl, string, count)


def escape(pattern: str):
    result = core.RegularExpression.escape(pattern)
    for i in DONT_ESCAPE:
        result.replace(i, r"\i")
    return result


if __name__ == "__main__":
    reg = compile("[0-9]+ [a-z] [0-9]+")
