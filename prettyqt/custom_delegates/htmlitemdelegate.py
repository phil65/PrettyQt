from __future__ import annotations

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


class HtmlItemDelegate(widgets.StyledItemDelegate):
    def paint(self, painter, option, index):
        options = widgets.StyleOptionViewItem(option)
        self.initStyleOption(options, index)

        painter.save()

        doc = gui.TextDocument()
        doc.setTextWidth(options.rect.width())

        text_option = gui.TextOption()
        text_option.setWrapMode(gui.TextOption.WrapMode.NoWrap)
        text_option.setAlignment(options.displayAlignment)
        doc.setDefaultTextOption(text_option)

        doc.setHtml(options.text)

        options.text = ""
        options.widget.style().drawControl(
            QtWidgets.QStyle.ControlElement.CE_ItemViewItem, options, painter
        )

        icon_size = options.icon.actualSize(options.rect.size())
        painter.translate(options.rect.left() + icon_size.width(), options.rect.top())
        clip = QtCore.QRectF(
            0, 0, options.rect.width() + icon_size.width(), options.rect.height()
        )

        doc.drawContents(painter, clip)

        painter.restore()

    def sizeHint(self, option, index):
        options = widgets.StyleOptionViewItem(option)
        self.initStyleOption(options, index)

        doc = gui.TextDocument()

        text_option = gui.TextOption()
        text_option.setWrapMode(gui.TextOption.WrapMode.NoWrap)
        doc.setDefaultTextOption(text_option)

        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())

        return QtCore.QSize(doc.idealWidth(), doc.size().height())
