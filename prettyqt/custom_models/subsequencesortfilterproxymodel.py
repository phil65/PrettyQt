from __future__ import annotations

import re
import sys

from prettyqt import constants, core
from prettyqt.qt import QtCore


MAX_SIZE = sys.maxsize


class SubsequenceSortFilterProxyModel(core.SortFilterProxyModel):
    """Performs subsequence matching/sorting."""

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self.prefix = ""
        self.filter_patterns = []
        self.filter_patterns_case_sensitive = []
        self.sort_patterns = []

    def set_prefix(self, prefix: str):
        self.prefix = prefix
        self.filter_patterns = []
        self.filter_patterns_case_sensitive = []
        self.sort_patterns = []
        flags = 0 if self.is_filter_case_sensitive() else re.IGNORE_CASE
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
        role = self.filterRole()
        idx = self.sourceModel().index(row, column, index)
        completion = self.sourceModel().data(idx, role)
        if (
            completion is None
            or self.prefix is None
            or len(completion) < len(self.prefix)
        ):
            return False
        if len(self.prefix) == 1:
            prefix = self.prefix
            if not self.is_filter_case_sensitive():
                completion = completion.lower()
                prefix = prefix.lower()
            if prefix not in completion:
                return False
            rank = completion.index(prefix)
            self.sourceModel().setData(idx, rank, constants.USER_ROLE)
            return prefix in completion
        for i, (pattern, pattern_case, sort_pattern) in enumerate(
            zip(
                self.filter_patterns,
                self.filter_patterns_case_sensitive,
                self.sort_patterns,
            )
        ):
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
                self.sourceModel().setData(idx, rank, constants.USER_ROLE)
                return True
        return len(self.prefix) == 0


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_models import JsonModel

    app = widgets.app()
    dist = [
        dict(
            a=2,
            b={
                "a": 4,
                "b": [1, 2, 3],
                "jkjkjk": "tekjk",
                "sggg": "tekjk",
                "fdfdf": "tekjk",
                "xxxx": "xxx",
            },
        ),
        6,
        "jkjk",
    ]
    source_model = JsonModel(dist)
    model = SubsequenceSortFilterProxyModel()
    model.setFilterKeyColumn(1)
    model.set_prefix("x")
    model.setSourceModel(source_model)
    table = widgets.TreeView()
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)
    table.show()
    app.main_loop()
