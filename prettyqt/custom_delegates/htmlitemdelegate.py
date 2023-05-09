from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtCore, QtWidgets


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

        return QtCore.QSize(int(doc.idealWidth()), int(doc.size().height()))


if __name__ == "__main__":
    from prettyqt import iconprovider

    app = widgets.app()
    model = gui.StandardItemModel()
    model.add("test")
    app = widgets.app()
    w = widgets.ListView()
    w.set_delegate(HtmlItemDelegate())
    w.set_model(model)
    item = gui.StandardItem("<b>test</b>")
    item.set_data("user", iconprovider.get_icon("mdi.folder"))
    model += item
    w.show()
    app.main_loop()
