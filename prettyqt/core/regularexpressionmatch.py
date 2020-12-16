from typing import Any, Dict, Optional, Tuple, Union

from qtpy import QtCore


class RegularExpressionMatch(QtCore.QRegularExpressionMatch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.string = None
        self.pos = None
        self.endpos = None

    def __repr__(self):
        return f"{type(self).__name__}()"

    def __getitem__(self, item: Union[int, str]) -> str:
        return self.captured(item)

    def group(self, *groups: Union[int, str]) -> Union[tuple, str]:
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

    def groupdict(self, default=None) -> Dict[str, Any]:
        if self.lastindex is None:
            return dict()
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

    def span(self, group: int = 0) -> Tuple[int, int]:
        return (self.capturedStart(group), self.capturedEnd(group))

    @property
    def lastindex(self) -> Optional[int]:
        idx = self.lastCapturedIndex()
        return None if idx == -1 else idx

    @property
    def lastgroup(self) -> Optional[str]:
        if self.lastCapturedIndex() == -1:
            return None
        return self.re.namedCaptureGroups()[self.lastCapturedIndex()]

    @property
    def re(self) -> QtCore.QRegularExpression:
        return self.regularExpression()

    @property
    def partial(self) -> bool:
        return self.hasPartialMatch()


if __name__ == "__main__":
    reg = RegularExpressionMatch()
