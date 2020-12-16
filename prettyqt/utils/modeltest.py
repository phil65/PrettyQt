# This file is based on the original C++ qabstractitemmodeltester.cpp from:
# http://code.qt.io/cgit/qt/qtbase.git/tree/src/testlib/qabstractitemmodeltester.cpp
# Commit 4af292fe5158c2d19e8ab1351c71c3940c7f1032
#
# Licensed under the following terms:
#
# Copyright (C) 2016 The Qt Company Ltd.
# Copyright (C) 2017 Klarälvdalens Datakonsult AB, a KDAB Group company,
# info@kdab.com, author Giuseppe D'Angelo <giuseppe.dangelo@kdab.com>
# Contact: https://www.qt.io/licensing/
#
# This file is part of the QtTest module of the Qt Toolkit.
#
# $QT_BEGIN_LICENSE:LGPL$
# Commercial License Usage
# Licensees holding valid commercial Qt licenses may use this file in
# accordance with the commercial license agreement provided with the
# Software or, alternatively, in accordance with the terms contained in
# a written agreement between you and The Qt Company. For licensing terms
# and conditions see https://www.qt.io/terms-conditions. For further
# information use the contact form at https://www.qt.io/contact-us.
#
# GNU Lesser General Public License Usage
# Alternatively, this file may be used under the terms of the GNU Lesser
# General Public License version 3 as published by the Free Software
# Foundation and appearing in the file LICENSE.LGPL3 included in the
# packaging of this file. Please review the following information to
# ensure the GNU Lesser General Public License version 3 requirements
# will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
#
# GNU General Public License Usage
# Alternatively, this file may be used under the terms of the GNU
# General Public License version 2.0 or (at your option) the GNU General
# Public license version 3 or any later version approved by the KDE Free
# Qt Foundation. The licenses are as published by the Free Software
# Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
# included in the packaging of this file. Please review the following
# information to ensure the GNU General Public License requirements will
# be met: https://www.gnu.org/licenses/gpl-2.0.html and
# https://www.gnu.org/licenses/gpl-3.0.html.
#
# $QT_END_LICENSE$

from typing import Any, List, NamedTuple

from qtpy import QtCore, QtGui, QtTest


class _Changing(NamedTuple):
    parent: QtCore.QModelIndex
    old_size: int
    last: Any
    next: Any


HAS_QT_TESTER = hasattr(QtTest, "QAbstractItemModelTester")

TYPES = [
    (QtCore.Qt.DisplayRole, (str,)),
    (QtCore.Qt.ToolTipRole, (str,)),
    (QtCore.Qt.StatusTipRole, (str,)),
    (QtCore.Qt.WhatsThisRole, (str,)),
    (QtCore.Qt.SizeHintRole, QtCore.QSize),
    (QtCore.Qt.FontRole, QtGui.QFont),
    (QtCore.Qt.BackgroundColorRole, (QtGui.QColor, QtGui.QBrush)),
    (QtCore.Qt.TextColorRole, (QtGui.QColor, QtGui.QBrush)),
    (
        QtCore.Qt.DecorationRole,
        (QtGui.QPixmap, QtGui.QImage, QtGui.QIcon, QtGui.QColor, QtGui.QBrush),
    ),
]


class ModelTester:
    """A tester for Qt's QAbstractItemModels."""

    def __init__(self, model: QtCore.QAbstractItemModel):
        self._model = model
        self._fetching_more = False
        self._insert: List[_Changing] = []
        self._remove: List[_Changing] = []
        self._changing: List[QtCore.QPersistentModelIndex] = []
        self._qt_tester = None

    def _debug(self, text):
        print("modeltest: " + text)

    def _modelindex_debug(self, index):
        """Get a string for debug output for a QModelIndex."""
        if index is None:
            return "<None>"
        elif not index.isValid():
            return "<invalid> (0x{:x})".format(id(index))
        else:
            data = self._model.data(index, QtCore.Qt.DisplayRole)
            return "{}/{} {!r} (0x{:x})".format(
                index.row(), index.column(), data, id(index)
            )

    def check(self, force_py: bool = False):
        """Run a series of checks in the given model.

        Connect to all of the models signals.

        Whenever anything happens recheck everything.

        :param model: The ``QAbstractItemModel`` to test.
        :param force_py:
          Force using the Python implementation, even if the C++ implementation
          is available.
        """
        assert self._model is not None

        if HAS_QT_TESTER and not force_py:
            reporting_mode = QtTest.QAbstractItemModelTester.FailureReportingMode.Warning
            self._qt_tester = QtTest.QAbstractItemModelTester(self._model, reporting_mode)
            self._debug("Using Qt C++ tester")
            return

        self._debug("Using Python tester")

        self._fetching_more = False
        self._insert = []
        self._remove = []
        self._changing = []

        self._model.columnsAboutToBeInserted.connect(self._run)
        self._model.columnsAboutToBeRemoved.connect(self._run)
        self._model.columnsInserted.connect(self._run)
        self._model.columnsRemoved.connect(self._run)
        self._model.dataChanged.connect(self._run)
        self._model.headerDataChanged.connect(self._run)
        self._model.layoutAboutToBeChanged.connect(self._run)
        self._model.layoutChanged.connect(self._run)
        self._model.modelReset.connect(self._run)
        self._model.rowsAboutToBeInserted.connect(self._run)
        self._model.rowsAboutToBeRemoved.connect(self._run)
        self._model.rowsInserted.connect(self._run)
        self._model.rowsRemoved.connect(self._run)

        # Special checks for changes
        self._model.layoutAboutToBeChanged.connect(self._on_layout_about_to_be_changed)
        self._model.layoutChanged.connect(self._on_layout_changed)
        self._model.rowsAboutToBeInserted.connect(self._on_rows_about_to_be_inserted)
        self._model.rowsAboutToBeRemoved.connect(self._on_rows_about_to_be_removed)
        self._model.rowsInserted.connect(self._on_rows_inserted)
        self._model.rowsRemoved.connect(self._on_rows_removed)
        self._model.dataChanged.connect(self._on_data_changed)
        self._model.headerDataChanged.connect(self._on_header_data_changed)

        self._run()

    def _cleanup(self):
        """Not API intended for users, but called from the fixture function."""
        if self._model is None:
            return

        self._model.columnsAboutToBeInserted.disconnect(self._run)
        self._model.columnsAboutToBeRemoved.disconnect(self._run)
        self._model.columnsInserted.disconnect(self._run)
        self._model.columnsRemoved.disconnect(self._run)
        self._model.dataChanged.disconnect(self._run)
        self._model.headerDataChanged.disconnect(self._run)
        self._model.layoutAboutToBeChanged.disconnect(self._run)
        self._model.layoutChanged.disconnect(self._run)
        self._model.modelReset.disconnect(self._run)
        self._model.rowsAboutToBeInserted.disconnect(self._run)
        self._model.rowsAboutToBeRemoved.disconnect(self._run)
        self._model.rowsInserted.disconnect(self._run)
        self._model.rowsRemoved.disconnect(self._run)

        self._model.layoutAboutToBeChanged.disconnect(self._on_layout_about_to_be_changed)
        self._model.layoutChanged.disconnect(self._on_layout_changed)
        self._model.rowsAboutToBeInserted.disconnect(self._on_rows_about_to_be_inserted)
        self._model.rowsAboutToBeRemoved.disconnect(self._on_rows_about_to_be_removed)
        self._model.rowsInserted.disconnect(self._on_rows_inserted)
        self._model.rowsRemoved.disconnect(self._on_rows_removed)
        self._model.dataChanged.disconnect(self._on_data_changed)
        self._model.headerDataChanged.disconnect(self._on_header_data_changed)

        self._model = None

    def _run(self):
        assert self._model is not None
        assert self._fetching_more is not None
        if self._fetching_more:
            return
        self._test_basic()
        self._test_row_count_and_column_count()
        self._test_has_index()
        self._test_index()
        self._test_parent()
        self._test_data()

    def _test_basic(self):
        """Try to call a number of the basic functions (not all).

        Make sure the model doesn't outright segfault, testing the functions
        which make sense.
        """
        assert not self._model.buddy(QtCore.QModelIndex()).isValid()

        self._model.canFetchMore(QtCore.QModelIndex())
        assert self._column_count(QtCore.QModelIndex()) >= 0
        self._fetch_more(QtCore.QModelIndex())
        flags = self._model.flags(QtCore.QModelIndex())
        assert flags == QtCore.Qt.ItemIsDropEnabled or not flags
        self._has_children(QtCore.QModelIndex())

        has_row = self._model.hasIndex(0, 0)
        if has_row:
            cache = None
            self._model.match(self._model.index(0, 0), -1, cache)

        self._model.mimeTypes()
        assert not self._parent(QtCore.QModelIndex()).isValid()
        assert self._model.rowCount() >= 0
        self._model.span(QtCore.QModelIndex())

        self._model.supportedDropActions()
        self._model.roleNames()

    def _test_row_count_and_column_count(self):
        """Test model's implementation of row/columnCount() and hasChildren().

        Models that are dynamically populated are not as fully tested here.

        The models rowCount() is tested more extensively in _check_children(),
        but this catches the big mistakes.
        """
        # check top row
        top_index = self._model.index(0, 0, QtCore.QModelIndex())

        rows = self._model.rowCount(top_index)
        assert rows >= 0

        columns = self._column_count(top_index)
        assert columns >= 0

        if rows == 0 or columns == 0:
            return

        assert self._has_children(top_index)

        second_level_index = self._model.index(0, 0, top_index)
        assert second_level_index.isValid()

        rows = self._model.rowCount(second_level_index)
        assert rows >= 0

        columns = self._column_count(second_level_index)
        assert columns >= 0

        if rows == 0 or columns == 0:
            return

        assert self._has_children(second_level_index)

    def _test_has_index(self):
        """Test model's implementation of hasIndex().

        hasIndex() is tested more extensively in _check_children(),
        but this catches the big mistakes.
        """
        # Make sure that invalid values return an invalid index
        assert not self._model.hasIndex(-2, -2)
        assert not self._model.hasIndex(-2, 0)
        assert not self._model.hasIndex(0, -2)

        rows = self._model.rowCount()
        columns = self._column_count()

        # check out of bounds
        assert not self._model.hasIndex(rows, columns)
        assert not self._model.hasIndex(rows + 1, columns + 1)

        if rows > 0 and columns > 0:
            assert self._model.hasIndex(0, 0)

    def _test_index(self):
        """Test model's implementation of index().

        index() is tested more extensively in _check_children(),
        but this catches the big mistakes.
        """
        rows = self._model.rowCount()
        columns = self._column_count()

        for row in range(rows):
            for column in range(columns):
                # Make sure that the same index is *always* returned
                a = self._model.index(row, column)
                b = self._model.index(row, column)
                assert a.isValid()
                assert b.isValid()
                assert a == b

    def _test_parent(self):
        """Test model's implementation of QAbstractItemModel::parent()."""
        # Make sure the model won't crash and will return an invalid
        # QModelIndex when asked for the parent of an invalid index.
        assert not self._parent(QtCore.QModelIndex()).isValid()

        if not self._has_children():
            return

        # Column 0                | Column 1      |
        # QModelIndex()           |               |
        #    \- top_index         | top_index_1   |
        #         \- child_index  | child_index_1 |

        # Common error test #1, make sure that a top level index has a parent
        # that is a invalid QModelIndex.
        top_index = self._model.index(0, 0, QtCore.QModelIndex())
        assert not self._parent(top_index).isValid()

        # Common error test #2, make sure that a second level index has a
        # parent that is the first level index.
        if self._has_children(top_index):
            child_index = self._model.index(0, 0, top_index)
            assert self._parent(child_index) == top_index

        # Common error test #3, the second column should NOT have the same
        # children as the first column in a row.
        # Usually the second column shouldn't have children.
        if self._model.hasIndex(0, 1):
            top_index_1 = self._model.index(0, 1, QtCore.QModelIndex())
            if self._has_children(top_index) and self._has_children(top_index_1):
                child_index = self._model.index(0, 0, top_index)
                assert child_index.isValid()
                child_index_1 = self._model.index(0, 0, top_index_1)
                assert child_index_1.isValid()
                assert child_index != child_index_1

        # Full test, walk n levels deep through the model making sure that all
        # parent's children correctly specify their parent.
        self._check_children(QtCore.QModelIndex())

    def _check_children(self, parent, current_depth=0):
        """Check parent/children relationships.

        Called from the parent() test.

        A model that returns an index of parent X should also return X when
        asking for the parent of the index.

        This recursive function does pretty extensive testing on the whole
        model in an effort to catch edge cases.

        This function assumes that rowCount(), columnCount() and index()
        already work.  If they have a bug it will point it out, but the above
        tests should have already found the basic bugs because it is easier to
        figure out the problem in those tests then this one.
        """
        # First just try walking back up the tree.
        p = parent
        while p.isValid():
            p = p.parent()

        # For models that are dynamically populated
        if self._model.canFetchMore(parent):
            self._fetch_more(parent)

        rows = self._model.rowCount(parent)
        columns = self._column_count(parent)

        if rows > 0:
            assert self._has_children(parent)

        # Some further testing against rows(), columns(), and hasChildren()
        assert rows >= 0
        assert columns >= 0
        if rows > 0 and columns > 0:
            assert self._has_children(parent)
        self._debug(
            "Checking children of {} with depth {} "
            "({} rows, {} columns)".format(
                self._modelindex_debug(parent), current_depth, rows, columns
            )
        )

        top_left_child = self._model.index(0, 0, parent)
        assert not self._model.hasIndex(rows, 0, parent)
        assert not self._model.hasIndex(rows + 1, 0, parent)

        for r in range(rows):
            assert not self._model.hasIndex(r, columns, parent)
            assert not self._model.hasIndex(r, columns + 1, parent)

            for c in range(columns):
                assert self._model.hasIndex(r, c, parent)
                index = self._model.index(r, c, parent)
                # rowCount() and columnCount() said that it existed...
                if not index.isValid():
                    self._debug(
                        "Got invalid index at row={} col={} parent={}".format(
                            r, c, self._modelindex_debug(parent)
                        )
                    )
                assert index.isValid()

                # index() should always return the same index when called twice
                # in a row
                modified_index = self._model.index(r, c, parent)
                assert index == modified_index

                sibling = self._model.sibling(r, c, top_left_child)
                assert index == sibling

                sibling2 = top_left_child.sibling(r, c)
                assert index == sibling2

                # Some basic checking on the index that is returned
                assert index.model() == self._model
                assert index.row() == r
                assert index.column() == c

                # If the next test fails here is some somewhat useful debug you
                # play with.
                if self._parent(index) != parent:
                    self._debug(
                        "Inconsistent parent() implementation detected\n"
                        "  index={} exp. parent={} act. parent={}\n"
                        "  row={} col={} depth={}\n"
                        "  data for child: {}\n"
                        "  data for parent: {}\n".format(
                            self._modelindex_debug(index),
                            self._modelindex_debug(parent),
                            self._modelindex_debug(self._parent(index)),
                            r,
                            c,
                            current_depth,
                            self._model.data(index),
                            self._model.data(parent),
                        )
                    )

                # Check that we can get back our real parent.
                assert self._parent(index) == parent

                # recursively go down the children
                if self._has_children(index) and current_depth < 10:
                    self._debug(
                        "{} has {} children".format(
                            self._modelindex_debug(index), self._model.rowCount(index)
                        )
                    )
                    self._check_children(index, current_depth + 1)

                # make sure that after testing the children that the index
                # doesn't change.
                newer_index = self._model.index(r, c, parent)
                assert index == newer_index
        self._debug("Children check for {} done".format(self._modelindex_debug(parent)))

    def _test_data(self):
        """Test model's implementation of data()."""
        if not self._has_children():
            return

        # A valid index should have a valid QVariant data
        assert self._model.index(0, 0).isValid()
        # General purpose roles with a fixed expected type
        for role, typ in TYPES:
            data = self._model.data(self._model.index(0, 0), role)
            if data is not None:
                data = data
            assert data == None or isinstance(data, typ), role  # noqa

        # Check that the alignment is one we know about
        alignment = self._model.data(self._model.index(0, 0), QtCore.Qt.TextAlignmentRole)
        if alignment is not None:
            try:
                alignment = int(alignment)
            except (TypeError, ValueError):
                assert 0, "%r should be a TextAlignmentRole enum" % alignment
            mask = int(QtCore.Qt.AlignHorizontal_Mask | QtCore.Qt.AlignVertical_Mask)
            assert alignment == alignment & mask

        # Check that the "check state" is one we know about.
        state = self._model.data(self._model.index(0, 0), QtCore.Qt.CheckStateRole)
        assert state in [
            None,
            QtCore.Qt.Unchecked,
            QtCore.Qt.PartiallyChecked,
            QtCore.Qt.Checked,
        ]

    def _on_rows_about_to_be_inserted(
        self, parent: QtCore.QModelIndex, start: int, end: int
    ):
        """Store what is about to be inserted.

        This gets stored to make sure it actually happens in rowsInserted.
        """
        last_index = self._model.index(start - 1, 0, parent)
        next_index = self._model.index(start, 0, parent)
        parent_rowcount = self._model.rowCount(parent)

        self._debug(
            "rows about to be inserted: start {}, end {}, parent {}, "
            "parent row count {}, last item {}, next item {}".format(
                start,
                end,
                self._modelindex_debug(parent),
                parent_rowcount,
                self._modelindex_debug(last_index),
                self._modelindex_debug(next_index),
            )
        )

        last_data = self._model.data(last_index) if start > 0 else None
        next_data = self._model.data(next_index) if start < parent_rowcount else None
        c = _Changing(
            parent=parent, old_size=parent_rowcount, last=last_data, next=next_data
        )
        self._insert.append(c)

    def _on_rows_inserted(self, parent: QtCore.QModelIndex, start: int, end: int):
        """Confirm that what was said was going to happen actually did."""
        c = self._insert.pop()
        last_data = (
            self._model.data(self._model.index(start - 1, 0, parent))
            if start >= 1
            else None
        )
        next_data = (
            self._model.data(self._model.index(end + 1, 0, c.parent))
            if end + 1 < self._model.rowCount(c.parent)
            else None
        )
        expected_size = c.old_size + (end - start + 1)
        current_size = self._model.rowCount(parent)

        self._debug(f"rows inserted: start {start}, end {end}")
        self._debug(
            "  from rowsAboutToBeInserted: parent {}, "
            "size {} (-> {} expected), "
            "next data {!r}, last data {!r}".format(
                self._modelindex_debug(c.parent),
                c.old_size,
                expected_size,
                c.next,
                c.last,
            )
        )

        self._debug(
            "  now in rowsInserted:        parent {}, size {}, "
            "next data {!r}, last data {!r}".format(
                self._modelindex_debug(parent), current_size, next_data, last_data
            )
        )
        assert c.parent == parent

        for ii in range(start, end + 1):
            idx = self._model.index(ii, 0, parent)
            self._debug(" item {} inserted: {}".format(ii, self._modelindex_debug(idx)))
        self._debug("")

        assert current_size == expected_size
        if last_data is not None:
            assert c.last == last_data
        if next_data is not None:
            assert c.next == next_data

    def _on_layout_about_to_be_changed(self):
        for i in range(max(self._model.rowCount(), 100)):
            idx = QtCore.QPersistentModelIndex(self._model.index(i, 0))
            self._changing.append(idx)

    def _on_layout_changed(self):
        for p in self._changing:
            assert p == self._model.index(p.row(), p.column(), p.parent())
        self._changing = []

    def _on_rows_about_to_be_removed(
        self, parent: QtCore.QModelIndex, start: int, end: int
    ):
        """Store what is about to be removed to make sure it actually happens.

        This gets stored to make sure it actually happens in rowsRemoved.
        """
        parent_rowcount = self._model.rowCount(parent)
        last_index = self._model.index(start - 1, 0, parent) if start > 0 else None
        next_index = (
            self._model.index(end + 1, 0, parent) if end < parent_rowcount - 1 else None
        )

        self._debug(
            "rows about to be removed: start {}, end {}, parent {}, "
            "parent row count {}, last item {}, next item {}".format(
                start,
                end,
                self._modelindex_debug(parent),
                parent_rowcount,
                self._modelindex_debug(last_index),
                self._modelindex_debug(next_index),
            )
        )

        if last_index is not None:
            assert last_index.isValid()
        if next_index is not None:
            assert next_index.isValid()

        last_data = None if last_index is None else self._model.data(last_index)
        next_data = None if next_index is None else self._model.data(next_index)
        c = _Changing(
            parent=parent, old_size=parent_rowcount, last=last_data, next=next_data
        )
        self._remove.append(c)

    def _on_rows_removed(self, parent: QtCore.QModelIndex, start: int, end: int):
        """Confirm that what was said was going to happen actually did."""
        c = self._remove.pop()
        last_data = (
            self._model.data(self._model.index(start - 1, 0, c.parent))
            if start > 0
            else None
        )
        next_data = (
            self._model.data(self._model.index(start, 0, c.parent))
            if end < c.old_size - 1
            else None
        )
        current_size = self._model.rowCount(parent)
        expected_size = c.old_size - (end - start + 1)

        self._debug(f"rows removed: start {start}, end {end}")
        self._debug(
            "  from rowsAboutToBeRemoved: parent {}, "
            "size {} (-> {} expected), "
            "next data {!r}, last data {!r}".format(
                self._modelindex_debug(c.parent),
                c.old_size,
                expected_size,
                c.next,
                c.last,
            )
        )

        self._debug(
            "  now in rowsRemoved:        parent {}, size {}, "
            "next data {!r}, last data {!r}".format(
                self._modelindex_debug(parent), current_size, next_data, last_data
            )
        )

        assert c.parent == parent
        assert current_size == expected_size
        if last_data is not None:
            assert c.last == last_data
        if next_data is not None:
            assert c.next == next_data

    def _on_data_changed(
        self, top_left: QtCore.QModelIndex, bottom_right: QtCore.QModelIndex
    ):
        assert top_left.isValid()
        assert bottom_right.isValid()
        common_parent = bottom_right.parent()
        assert top_left.parent() == common_parent
        assert top_left.row() <= bottom_right.row()
        assert top_left.column() <= bottom_right.column()
        assert bottom_right.row() < self._model.rowCount(common_parent)
        assert bottom_right.column() < self._column_count(common_parent)

    def _on_header_data_changed(self, orientation, start: int, end: int):
        assert orientation in [QtCore.Qt.Horizontal, QtCore.Qt.Vertical]
        is_vertical = orientation == QtCore.Qt.Vertical
        count = self._model.rowCount() if is_vertical else self._column_count()
        assert 0 <= start <= end < count

    def _column_count(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()):
        """Test columnCount.

        Workaround for the fact that ``columnCount`` is a private method in
        QAbstractListModel/QAbstractTableModel subclasses.
        """
        if isinstance(self._model, QtCore.QAbstractListModel):
            return 1 if parent == QtCore.QModelIndex() else 0
        else:
            return self._model.columnCount(parent)

    def _parent(self, index: QtCore.QModelIndex):
        """Test parent."""
        model_types = (QtCore.QAbstractListModel, QtCore.QAbstractTableModel)
        if isinstance(self._model, model_types):
            return QtCore.QModelIndex()
        else:
            return self._model.parent(index)

    def _has_children(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()):
        """Test hasChildren."""
        model_types = (QtCore.QAbstractListModel, QtCore.QAbstractTableModel)
        if isinstance(self._model, model_types):
            print(parent == QtCore.QModelIndex(), self._model.rowCount())
            return parent == QtCore.QModelIndex() and self._model.rowCount() > 0
        else:
            return self._model.hasChildren(parent)

    def _fetch_more(self, parent: QtCore.QModelIndex):
        """Call ``fetchMore`` on the model and set ``self._fetching_more``."""
        self._fetching_more = True
        self._model.fetchMore(parent)
        self._fetching_more = False
