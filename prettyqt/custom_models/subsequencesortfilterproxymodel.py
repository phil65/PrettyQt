from __future__ import annotations

import re
import sys

from prettyqt import core
from prettyqt.qt import QtCore


MAX_SIZE = sys.maxsize
USER_ROLE = QtCore.Qt.ItemDataRole.UserRole


class SubsequenceSortFilterProxyModel(core.SortFilterProxyModel):
    """Performs subsequence matching/sorting."""

    def __init__(self, case_sensitivity: bool, parent=None):
        super().__init__(parent)
        self.case_sensitivity = case_sensitivity

    def set_prefix(self, prefix: str):
        self.filter_patterns = []
        self.filter_patterns_case_sensitive = []
        self.sort_patterns = []
        flags = re.IGNORECASE if self.case_sensitivity is False else 0
        for i in reversed(range(1, len(prefix) + 1)):
            ptrn = f".*{prefix[0:i]}.*{prefix[i:]}"
            try:
                self.filter_patterns.append(re.compile(ptrn, flags))
                self.filter_patterns_case_sensitive.append(re.compile(ptrn, 0))
                ptrn = f"{prefix[0:i]}.*{prefix[i:]}"
                self.sort_patterns.append(re.compile(ptrn, flags))
            except Exception:
                continue
        self.prefix = prefix

    def filterAcceptsRow(self, row, _):
        completion = self.sourceModel().data(self.sourceModel().index(row, 0))
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
                idx = self.sourceModel().index(row, 0)
                self.sourceModel().setData(idx, rank, USER_ROLE)  # type: ignore
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
            match = re.match(pattern, completion)
            if match:
                # compute rank, the lowest rank the closer it is from the
                # completion
                start = MAX_SIZE
                for m in sort_pattern.finditer(completion):
                    start, end = m.span()
                rank = start + i * 10
                if re.match(pattern_case, completion):
                    # favorise completions where case is matched
                    rank -= 10
                self.sourceModel().setData(idx, rank, USER_ROLE)  # type: ignore
                return True
        return len(self.prefix) == 0
