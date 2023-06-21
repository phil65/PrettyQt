from __future__ import annotations

import enum
from prettyqt import constants, widgets

SE = widgets.QStyle.SubElement


class CenteredBoxProxyStyle(widgets.QProxyStyle):
    class Roles(enum.IntEnum):
        """Proxy roles."""
        CheckAlignmentRole = constants.USER_ROLE + 3321
        DecorationAlignmentRole = constants.USER_ROLE + 1322

    def subElementRect(self, element, option, widget):
        base_res = super().subElementRect(element, option, widget)
        if element != widgets.QStyle.ControlElement.CE_ItemViewItem:
            return base_res
        item_opt = widgets.QStyleOptionViewItem(option)
        # item_opt = QStyleOptionViewItem()
        # widget.initStyleOption(item_opt)
        match element:
            case SE.SE_ItemViewItemCheckIndicator:
                align_data = (
                    item_opt.index.data(self.Roles.CheckAlignmentRole)
                    if item_opt
                    else None
                )
                if align_data is not None:
                    return widgets.QStyle.alignedRect(
                        item_opt.direction,
                        constants.AlignmentFlag(align_data.value),
                        base_res.size(),
                        item_opt.rect,
                    )
            case SE.SE_ItemViewItemDecoration:
                align_data = (
                    item_opt.index.data(self.Roles.DecorationAlignmentRole)
                    if item_opt
                    else None
                )
                if align_data is not None:
                    return widgets.QStyle.alignedRect(
                        item_opt.direction,
                        constants.AlignmentFlag(align_data.value),
                        base_res.size(),
                        item_opt.rect,
                    )
            case SE.SE_ItemViewItemFocusRect:
                check_align_data = (
                    item_opt.index.data(self.Roles.CheckAlignmentRole)
                    if item_opt
                    else None
                )
                decoration_align_data = (
                    item_opt.index.data(self.Roles.DecorationAlignmentRole)
                    if item_opt
                    else None
                )
                if check_align_data is not None or decoration_align_data is not None:
                    return option.rect
        return base_res


if __name__ == "__main__":
    from prettyqt import gui

    app = widgets.app()
    style = CenteredBoxProxyStyle()
    # app.setStyle(style)
    model = gui.StandardItemModel()
    model.setColumnCount(1)
    model.setRowCount(2)
    pix = gui.QPixmap(20, 20)
    pix.fill(constants.GlobalColor.blue)
    checkable_item = gui.StandardItem()
    checkable_item.setFlags(checkable_item.flags() | constants.IS_CHECKABLE)
    checkable_item.setData(constants.ALIGN_CENTER, style.Roles.CheckAlignmentRole)
    model.setItem(0, 0, checkable_item)
    checkable_item = gui.StandardItem()
    checkable_item.setFlags(checkable_item.flags() | constants.IS_CHECKABLE)
    checkable_item.setData(constants.ALIGN_CENTER, style.Roles.DecorationAlignmentRole)
    checkable_item.setIcon(pix)
    model.setItem(1, 0, checkable_item)
    tv = widgets.TableView()
    tv.set_model(model)
    tv.setStyle(style)
    tv.show()
    app.exec()
