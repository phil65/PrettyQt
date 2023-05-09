from __future__ import annotations

import re
import sys

from prettyqt import constants, core
from prettyqt.qt import QtCore


MAX_SIZE = sys.maxsize


class SubsequenceSortFilterProxyModel(core.SortFilterProxyModel):
    """Performs subsequence matching/sorting."""

    def __init__(
        self, case_sensitivity: bool = False, parent: QtCore.QObject | None = None
    ):
        super().__init__(parent)
        self.case_sensitivity = case_sensitivity
        self.prefix = ""
        self.filter_patterns = []
        self.filter_patterns_case_sensitive = []
        self.sort_patterns = []

    def set_prefix(self, prefix: str):
        self.prefix = prefix
        self.filter_patterns = []
        self.filter_patterns_case_sensitive = []
        self.sort_patterns = []
        flags = re.IGNORECASE if self.case_sensitivity is False else 0
        for i in reversed(range(1, len(prefix) + 1)):
            ptrn = f".*{prefix[:i]}.*{prefix[i:]}"
            try:
                self.filter_patterns.append(re.compile(ptrn, flags))
                self.filter_patterns_case_sensitive.append(re.compile(ptrn, 0))
                ptrn = f"{prefix[:i]}.*{prefix[i:]}"
                self.sort_patterns.append(re.compile(ptrn, flags))
            except Exception:
                continue

    def filterAcceptsRow(self, row, index):
        column = self.filterKeyColumn()
        idx = self.sourceModel().index(row, column, index)
        completion = self.sourceModel().data(idx)
        if completion is None or self.prefix is None:
            return False
        if len(completion) < len(self.prefix):
            return False
        if len(self.prefix) == 1:
            try:
                prefix = self.prefix
                if self.case_sensitivity is False:
                    completion = completion.lower()
                    prefix = self.prefix.lower()
                rank = completion.index(prefix)
                self.sourceModel().setData(idx, rank, constants.USER_ROLE)
                return prefix in completion
            except ValueError:
                return False
        for i, patterns in enumerate(
            zip(
                self.filter_patterns,
                self.filter_patterns_case_sensitive,
                self.sort_patterns,
            )
        ):
            pattern, pattern_case, sort_pattern = patterns
            if re.match(pattern, completion):
                # compute rank, the lowest rank the closer it is from the
                # completion
                start = MAX_SIZE
                for m in sort_pattern.finditer(completion):
                    start, end = m.span()
                rank = start + i * 10
                if re.match(pattern_case, completion):
                    # favorise completions where case is matched
                    rank -= 10
                self.sourceModel().setData(idx, rank, constants.USER_ROLE)  # type: ignore
                return True
        return len(self.prefix) == 0
