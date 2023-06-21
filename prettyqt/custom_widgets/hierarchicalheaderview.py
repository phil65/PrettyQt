from __future__ import annotations

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


SortIndicator = QtWidgets.QStyleOptionHeader.SortIndicator
StateFlag = QtWidgets.QStyle.StateFlag
CE = QtWidgets.QStyle.ControlElement
SelectedPosition = QtWidgets.QStyleOptionHeader.SelectedPosition
SectionPosition = QtWidgets.QStyleOptionHeader.SectionPosition

HORIZONTAL_HEADER_DATA_ROLE = QtCore.Qt.ItemDataRole.UserRole + 150
VERTICAL_HEADER_DATA_ROLE = QtCore.Qt.ItemDataRole.UserRole + 151


def find_root_index(index: core.ModelIndex) -> core.ModelIndex:
    while index.parent().isValid():
        index = index.parent()
    return index


def get_parent_indexes(index: core.ModelIndex) -> list[core.ModelIndex]:
    indexes = []
    while index.isValid():
        indexes.insert(0, index)
        index = index.parent()
    return indexes


class HierarchicalHeaderView(widgets.HeaderView):
    """Hierarchical header view.

    This class is a Python port of
    http://qt-apps.org/content/show.php/HierarchicalHeaderView?content=103154
    """

    header_model = None

    def __init__(
        self,
        orientation: QtCore.Qt.Orientation | constants.OrientationStr,
        parent: QtWidgets.QWidget,
    ):
        super().__init__(orientation, parent, highlight_sections=True)
        self.setSectionsClickable(True)
        self.sectionResized.connect(self.on_section_resized)
        self.show()  # force to be visible
        if orientation in {constants.HORIZONTAL, "horizontal"}:
            parent.setHorizontalHeader(self)
        else:
            parent.setVerticalHeader(self)
        self.sectionMoved.connect(self._on_section_moved)

    def init_from_new_model(
        self, orientation: QtCore.Qt.Orientation, model: QtCore.QAbstractItemModel
    ):
        is_hor = orientation == constants.HORIZONTAL
        role = HORIZONTAL_HEADER_DATA_ROLE if is_hor else VERTICAL_HEADER_DATA_ROLE
        self.header_model = model.data(core.ModelIndex(), role)

    def find_leaf(
        self, index: core.ModelIndex, section_index: int, current_leaf_index: int
    ) -> tuple[core.ModelIndex, int]:
        if not index.isValid():
            return core.ModelIndex(), current_leaf_index
        model = index.model()
        if child_count := model.columnCount(index):
            for i in range(child_count):
                res, current_leaf_index = self.find_leaf(
                    model.index(0, i, index), section_index, current_leaf_index
                )
                if res.isValid():
                    return res, current_leaf_index
        else:
            current_leaf_index += 1
            if current_leaf_index == section_index:
                return index, current_leaf_index
        return core.ModelIndex(), current_leaf_index

    def leaf_index(self, section_index: int) -> core.ModelIndex:
        if self.header_model:
            current_leaf_index = -1
            for i in range(self.header_model.columnCount()):
                res, current_leaf_index = self.find_leaf(
                    self.header_model.index(0, i), section_index, current_leaf_index
                )
                if res.isValid():
                    return res
        return core.ModelIndex()

    def search_leafs(self, index: core.ModelIndex) -> list[core.ModelIndex]:
        res = []
        if index.isValid():
            model = index.model()
            if child_count := index.model().columnCount(index):
                for i in range(child_count):
                    leaf = model.index(0, i, index)
                    res += self.search_leafs(leaf)
            else:
                res.append(index)
        return res

    def leafs(self, index: core.ModelIndex) -> list[core.ModelIndex]:
        leafs = []
        if index.isValid():
            model = index.model()
            child_count = index.model().columnCount(index)
            for i in range(child_count):
                leaf = model.index(0, i, index)
                leafs += self.search_leafs(leaf)
        return leafs

    def set_foreground_brush(
        self, opt: QtWidgets.QStyleOptionHeader, index: core.ModelIndex
    ):
        if foreground_brush := index.data(constants.FOREGROUND_ROLE):
            brush = QtGui.QBrush(foreground_brush)
            opt.palette.setBrush(QtGui.QPalette.ColorRole.ButtonText, brush)

    def set_background_brush(
        self, opt: QtWidgets.QStyleOptionHeader, index: core.ModelIndex
    ):
        if background_brush := index.data(constants.BACKGROUND_ROLE):
            brush = QtGui.QBrush(background_brush)
            opt.palette.setBrush(QtGui.QPalette.ColorRole.Button, brush)
            opt.palette.setBrush(QtGui.QPalette.ColorRole.Window, brush)

    def get_cell_size(
        self,
        leaf_index: core.ModelIndex,
        hv: QtWidgets.QHeaderView,
        style_options: QtWidgets.QStyleOptionHeader,
    ) -> QtCore.QSize:
        res = QtCore.QSize()
        if variant := leaf_index.data(constants.SIZE_HINT_ROLE):
            res = variant
        fnt = var if (var := leaf_index.data(constants.FONT_ROLE)) else hv.font()
        fnt.setBold(True)
        fm = QtGui.QFontMetrics(fnt)
        text_size = fm.size(0, leaf_index.data(constants.DISPLAY_ROLE))
        size = text_size + QtCore.QSize(4, 0)
        if leaf_index.data(constants.USER_ROLE):
            size.transpose()
        decoration_size = hv.style().sizeFromContents(
            QtWidgets.QStyle.ContentsType.CT_HeaderSection,
            style_options,
            QtCore.QSize(),
            hv,
        )
        empty_text_size = fm.size(0, "")
        return res.expandedTo(size + decoration_size - empty_text_size)

    def get_current_cell_width(
        self,
        searched_index: core.ModelIndex,
        leaf_index: core.ModelIndex,
        section_index: int,
        hv: QtWidgets.QHeaderView,
    ) -> int:
        leafs_list = self.leafs(searched_index)
        if not leafs_list:
            return hv.sectionSize(section_index)
        offset = leafs_list.index(leaf_index) if leaf_index in leafs_list else -1
        first_leaf_section_index = section_index - offset
        return sum(
            hv.sectionSize(first_leaf_section_index + i) for i in range(len(leafs_list))
        )

    def get_current_cell_left(
        self,
        searched_index: core.ModelIndex,
        leaf_index: core.ModelIndex,
        section_index: int,
        left: int,
        hv: QtWidgets.QHeaderView,
    ) -> int:
        if leafs_list := self.leafs(searched_index):
            n = leafs_list.index(leaf_index) if leaf_index in leafs_list else -1
            first_leaf_section_index = section_index - n
            for i in range(n - 1, -1, -1):
                left -= hv.sectionSize(first_leaf_section_index + i)
        return left

    def paint_horizontal_cell(
        self,
        painter: QtGui.QPainter,
        hv: QtWidgets.QHeaderView,
        cell_index: core.ModelIndex,
        leaf_index: core.ModelIndex,
        logical_leaf_index: int,
        style_options: QtWidgets.QStyleOptionHeader,
        section_rect: QtCore.QRect,
        top: int,
    ) -> int:
        uniopt = QtWidgets.QStyleOptionHeader(style_options)
        self.set_foreground_brush(uniopt, cell_index)
        self.set_background_brush(uniopt, cell_index)
        height = (
            section_rect.height() - top
            if cell_index == leaf_index
            else self.get_cell_size(cell_index, hv, uniopt).height()
        )
        left = self.get_current_cell_left(
            cell_index, leaf_index, logical_leaf_index, section_rect.left(), hv
        )
        width = self.get_current_cell_width(
            cell_index, leaf_index, logical_leaf_index, hv
        )
        r = QtCore.QRect(left, top, width, height)
        uniopt.text = cell_index.data(constants.DISPLAY_ROLE)
        painter.save()
        uniopt.rect = r
        style = hv.style()
        if cell_index.data(constants.USER_ROLE):
            style.drawControl(CE.CE_HeaderSection, uniopt, painter, hv)
            m = QtGui.QTransform()
            m.rotate(-90)
            painter.setWorldTransform(m, True)
            new_r = QtCore.QRect(0, 0, r.height(), r.width())
            new_r.moveCenter(QtCore.QPoint(-r.center().y(), r.center().x()))
            uniopt.rect = new_r
            style.drawControl(CE.CE_HeaderLabel, uniopt, painter, hv)
        else:
            style.drawControl(CE.CE_Header, uniopt, painter, hv)
        painter.restore()
        return top + height

    def paint_horizontal_section(
        self,
        painter: QtGui.QPainter,
        section_rect: QtCore.QRect,
        logical_leaf_index: int,
        hv: QtWidgets.QHeaderView,
        style_options: QtWidgets.QStyleOptionHeader,
        leaf_index: core.ModelIndex,
    ):
        old_bo = painter.brushOrigin()
        top = section_rect.y()
        indexes = get_parent_indexes(leaf_index)
        for i, idx in enumerate(indexes):
            real_style_options = QtWidgets.QStyleOptionHeader(style_options)
            if i < len(indexes) - 1 and (
                real_style_options.state & StateFlag.State_Sunken
                or real_style_options.state & StateFlag.State_On
            ):
                t = StateFlag.State_Sunken | StateFlag.State_On
                real_style_options.state = real_style_options.state & ~t
                # FIXME: parent items are not highlighted
            if i < len(indexes) - 1:  # Use sortIndicator for inner level only
                real_style_options.sortIndicator = SortIndicator.None_
            #                if i==0:
            #                    print(self.leafs(indexes[i]), leaf_index)
            top = self.paint_horizontal_cell(
                painter,
                hv,
                idx,
                leaf_index,
                logical_leaf_index,
                real_style_options,
                section_rect,
                top,
            )
        painter.setBrushOrigin(old_bo)

    def paint_vertical_cell(
        self,
        painter: QtGui.QPainter,
        hv: QtWidgets.QHeaderView,
        cell_index: core.ModelIndex,
        leaf_index: core.ModelIndex,
        logical_leaf_index: int,
        style_options: QtWidgets.QStyleOptionHeader,
        section_rect: QtCore.QRect,
        left: int,
    ) -> int:
        uniopt = QtWidgets.QStyleOptionHeader(style_options)
        self.set_foreground_brush(uniopt, cell_index)
        self.set_background_brush(uniopt, cell_index)
        width = (
            section_rect.width() - left
            if cell_index == leaf_index
            else self.get_cell_size(cell_index, hv, uniopt).width()
        )
        top = self.get_current_cell_left(
            cell_index, leaf_index, logical_leaf_index, section_rect.top(), hv
        )
        height = self.get_current_cell_width(
            cell_index, leaf_index, logical_leaf_index, hv
        )
        r = QtCore.QRect(left, top, width, height)
        uniopt.text = cell_index.data(constants.DISPLAY_ROLE)
        painter.save()
        uniopt.rect = r
        style = hv.style()
        if cell_index.data(constants.USER_ROLE):
            style.drawControl(CE.CE_HeaderSection, uniopt, painter, hv)
            m = QtGui.QTransform()
            m.rotate(-90)
            painter.setWorldTransform(m, True)
            new_r = QtCore.QRect(0, 0, r.height(), r.width())
            new_r.moveCenter(QtCore.QPoint(-r.center().y(), r.center().x()))
            uniopt.rect = new_r
            style.drawControl(CE.CE_HeaderLabel, uniopt, painter, hv)
        else:
            style.drawControl(CE.CE_Header, uniopt, painter, hv)
        painter.restore()
        return left + width

    def paint_vertical_section(
        self,
        painter: QtGui.QPainter,
        section_rect: QtCore.QRect,
        logical_leaf_index: int,
        hv: QtWidgets.QHeaderView,
        style_options: QtWidgets.QStyleOptionHeader,
        leaf_index: core.ModelIndex,
    ):
        old_bo = painter.brushOrigin()
        left = section_rect.x()
        indexes = get_parent_indexes(leaf_index)
        for i, idx in enumerate(indexes):
            real_style_options = QtWidgets.QStyleOptionHeader(style_options)
            if i < len(indexes) - 1 and (
                real_style_options.state & StateFlag.State_Sunken
                or real_style_options.state & StateFlag.State_On
            ):
                t = StateFlag.State_Sunken | StateFlag.State_On
                real_style_options.state = real_style_options.state & ~t
                # FIXME: parent items are not highlighted
            left = self.paint_vertical_cell(
                painter,
                hv,
                idx,
                leaf_index,
                logical_leaf_index,
                real_style_options,
                section_rect,
                left,
            )
        painter.setBrushOrigin(old_bo)

    def _on_section_moved(
        self, logical_index: int, old_visual_index: int, new_visual_index: int
    ):
        view = self.parent()
        model = view.model()
        if not hasattr(model, "reorder"):
            return  # reorder underlying data of models with /reorder/ def only
        if getattr(self, "manual_move", False):
            self.manual_move = False
            return
        self.manual_move = True
        self.moveSection(new_visual_index, old_visual_index)  # cancel move
        if not model.reorder(old_visual_index, new_visual_index, self.orientation()):
            return
        rng = sorted((old_visual_index, new_visual_index))

        if self.orientation() == constants.HORIZONTAL:
            options = [(view.columnWidth(i), i) for i in range(rng[0], rng[1] + 1)]
            for i, col in enumerate(range(rng[0], rng[1] + 1)):
                view.setColumnWidth(col, options[i][0])
            view.selectColumn(new_visual_index)
        else:
            options = [(view.rowHeight(i), i) for i in range(rng[0], rng[1] + 1)]
            for i, col in enumerate(range(rng[0], rng[1] + 1)):
                view.setRowHeight(col, options[i][0])
            view.selectRow(new_visual_index)

        # FIXME: don't select if sorting is enable?
        if self.isSortIndicatorShown():
            sort_ind_index = next(
                (i for i, o in enumerate(options) if o[1] == self.sortIndicatorSection()),
                None,
            )
            # sort indicator is among sections being reordered
            if sort_ind_index is not None:
                # FIXME: does unnecessary sorting
                self.setSortIndicator(sort_ind_index + rng[0], self.sortIndicatorOrder())
        model.layoutChanged.emit()  # update view

    def get_style_option_for_cell(
        self, logical_index: int
    ) -> QtWidgets.QStyleOptionHeader:
        opt = QtWidgets.QStyleOptionHeader()
        self.initStyleOption(opt)
        if self.isSortIndicatorShown() and self.sortIndicatorSection() == logical_index:
            asc = self.sortIndicatorOrder() == constants.ASCENDING
            opt.sortIndicator = SortIndicator.SortDown if asc else SortIndicator.SortUp
        if self.window().isActiveWindow():
            opt.state = opt.state | StateFlag.State_Active
        opt.textAlignment = QtCore.Qt.AlignmentFlag.AlignCenter
        opt.iconAlignment = QtCore.Qt.AlignmentFlag.AlignVCenter
        opt.section = logical_index
        visual = self.visualIndex(logical_index)
        if self.count() == 1:
            opt.position = SectionPosition.OnlyOneSection
        elif visual == 0:
            opt.position = SectionPosition.Beginning
        else:
            is_end = visual == self.count() - 1
            opt.position = SectionPosition.End if is_end else SectionPosition.Middle
        sel_model = self.selectionModel()
        if not sel_model:
            return opt
        root_idx = self.rootIndex()
        if self.sectionsClickable() and self.highlightSections():
            if self.orientation() == constants.HORIZONTAL:
                if sel_model.columnIntersectsSelection(logical_index, root_idx):
                    opt.state = opt.state | StateFlag.State_On
                if sel_model.isColumnSelected(logical_index, root_idx):
                    opt.state = opt.state | StateFlag.State_Sunken
            else:
                if sel_model.rowIntersectsSelection(logical_index, root_idx):
                    opt.state = opt.state | StateFlag.State_On
                if sel_model.isRowSelected(logical_index, root_idx):
                    opt.state = opt.state | StateFlag.State_Sunken
        prev_idx = self.logicalIndex(visual - 1)
        next_idx = self.logicalIndex(visual + 1)
        if self.orientation() == constants.HORIZONTAL:
            prev_selected = sel_model.isColumnSelected(prev_idx, root_idx)
            next_selected = sel_model.isColumnSelected(next_idx, root_idx)
        else:
            prev_selected = sel_model.isRowSelected(prev_idx, root_idx)
            next_selected = sel_model.isRowSelected(next_idx, root_idx)

        if prev_selected and next_selected:
            opt.selectedPosition = SelectedPosition.NextAndPreviousAreSelected
        elif prev_selected:
            opt.selectedPosition = SelectedPosition.PreviousIsSelected
        elif next_selected:
            opt.selectedPosition = SelectedPosition.NextIsSelected
        else:
            opt.selectedPosition = SelectedPosition.NotAdjacent
        return opt

    def sectionSizeFromContents(self, logical_index: int) -> QtCore.QSize:
        if not self.header_model:
            return super().sectionSizeFromContents(logical_index)
        cur_leaf_index = self.leaf_index(logical_index)
        if not cur_leaf_index.isValid():
            return super().sectionSizeFromContents(logical_index)
        styleOption = QtWidgets.QStyleOptionHeader(
            self.get_style_option_for_cell(logical_index)
        )
        s = self.get_cell_size(cur_leaf_index, self, styleOption)
        cur_leaf_index = cur_leaf_index.parent()
        while cur_leaf_index.isValid():
            cell_size = self.get_cell_size(cur_leaf_index, self, styleOption)
            if self.orientation() == constants.HORIZONTAL:
                s.setHeight(s.height() + cell_size.height())
            else:
                s.setWidth(s.width() + cell_size.width())
            cur_leaf_index = cur_leaf_index.parent()
        return s

    def paintSection(
        self, painter: QtGui.QPainter, rect: QtCore.QRect, logical_index: int
    ):
        if not rect.isValid():
            super().paintSection(painter, rect, logical_index)
            return
        leaf_index = self.leaf_index(logical_index)
        if not leaf_index.isValid():
            super().paintSection(painter, rect, logical_index)
            return
        style_option = self.get_style_option_for_cell(logical_index)
        if self.orientation() == constants.HORIZONTAL:
            self.paint_horizontal_section(
                painter,
                rect,
                logical_index,
                self,
                style_option,
                leaf_index,
            )
        else:
            self.paint_vertical_section(
                painter,
                rect,
                logical_index,
                self,
                style_option,
                leaf_index,
            )

    def on_section_resized(self, logical_index: int):
        if self.isSectionHidden(logical_index):
            return
        leaf_index = self.leaf_index(logical_index)
        if leaf_index.isValid():
            leafs_list = self.leafs(find_root_index(leaf_index))
            start = leafs_list.index(leaf_index) if leaf_index in leafs_list else -1
            is_horizontal = self.orientation() == constants.HORIZONTAL
            for _ in range(start, 0, -1):
                logical_index -= 1
                w = self.viewport().width()
                h = self.viewport().height()
                pos = self.sectionViewportPosition(logical_index)
                r = QtCore.QRect(pos, 0, w - pos, h)
                if is_horizontal:
                    if self.isRightToLeft():
                        r.setRect(0, 0, pos + self.sectionSize(logical_index), h)
                else:
                    r.setRect(0, pos, w, h - pos)
                self.viewport().update(r.normalized())

    def setModel(self, model: QtCore.QAbstractItemModel):
        super().setModel(model)
        model.layoutChanged.connect(self._on_layout_change)
        self._on_layout_change()

    def _on_layout_change(self):
        if model := self.model():
            self.init_from_new_model(self.orientation(), model)
            is_horizontal = self.orientation() == constants.HORIZONTAL
            count = model.columnCount() if is_horizontal else model.rowCount()
            self.initializeSections(0, count - 1)


if __name__ == "__main__":
    import numpy as np
    import pandas as pd

    from prettyqt.qtpandas import pandasmodels

    class DataFrameModel(pandasmodels.DataTableModel):
        def read_level(
            self, y: int = 0, xs: int = 0, xe: int | None = None, orient=None
        ) -> list[gui.StandardItem]:
            c = (
                self.df.columns
                if orient == HORIZONTAL_HEADER_DATA_ROLE
                else self.df.index
            )
            if not hasattr(c, "levels"):  # not MultiIndex
                return [gui.StandardItem(str(i)) for i in c]
            sibl = []
            section_start, v, xe = xs, None, xe or len(c)
            for i in range(xs, xe):
                label = c.codes[y][i]
                if label != v:
                    if y + 1 < len(c.levels) and i > xs:
                        children = self.read_level(y + 1, section_start, i, orient=orient)
                        sibl[-1].appendRow(children)
                    item = gui.StandardItem(str(c.levels[y][label]))
                    sibl.append(item)
                    section_start = i
                    v = label
            if y + 1 < len(c.levels):
                children = self.read_level(y + 1, section_start, orient=orient)
                sibl[-1].appendRow(children)
            return sibl

        def data(
            self,
            index: core.ModelIndex,
            role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        ):
            if role in (HORIZONTAL_HEADER_DATA_ROLE, VERTICAL_HEADER_DATA_ROLE):
                hm = gui.StandardItemModel()
                hm.appendRow(self.read_level(orient=role))
                return hm
            return super().data(index, role)

        def reorder(self, old_index, new_index, orientation) -> bool:
            """Reorder columns / rows."""
            horizontal = orientation == constants.HORIZONTAL
            cols = list(self.df.columns if horizontal else self.df.index)
            cols.insert(new_index, cols.pop(old_index))
            self.df = self.df[cols] if horizontal else self.df.T[cols].T
            return True

        # def headerData(self, section, orientation, role):
        #     if role != constants.DISPLAY_ROLE:
        #         return
        #     strings = (str(i) for i in idx)
        #     if orientation == constants.HORIZONTAL:
        #         idx = self.df.columns
        #         return "\n".join(strings) if isinstance(idx, tuple) else str(idx)
        #     else:
        #         idx = self.df.index
        #         return " | ".join(strings) if isinstance(idx, tuple) else str(idx)

    app = widgets.app()
    form = widgets.Widget()
    # form.setAttribute(Qt.WA_DeleteOnClose)  # http://stackoverflow.com/a/27178019/1119602
    form.setMinimumSize(700, 260)
    view = widgets.TableView()
    widgets.VBoxLayout(form).addWidget(view)
    form.show()

    # Prepare data
    tuples = [
        ("bar", "one", "q"),
        ("bar", "two", "q"),
        ("baz", "one", "q"),
        ("baz", "two", "q"),
        ("foo", "one", "q"),
        ("foo", "two", "q"),
        ("qux", "one", "q"),
        ("qux", "two", "q"),
    ]
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second", "third"])
    df = pd.DataFrame(np.random.randn(6, 6), index=index[:6], columns=index[:6])

    # Prepare view
    #    oldh, oldv = view.horizontalHeader(), view.verticalHeader()
    #    oldh.setParent(form), oldv.setParent(form) #Save old headers for some reason
    HierarchicalHeaderView(constants.HORIZONTAL, view)
    HierarchicalHeaderView(constants.VERTICAL, view)
    view.h_header.setSectionsMovable(True)  # reorder DataFrame columns manually
    # Set data
    model = DataFrameModel(df)
    view.setModel(model)
    idx = model.index(0, 0)
    view.set_sorting_enabled(True, False)
    view.resizeColumnsToContents()
    view.resizeRowsToContents()
    # Set sorting enabled (after setting model)
    app.main_loop()
