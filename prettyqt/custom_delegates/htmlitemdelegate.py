from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtCore, QtWidgets


class HtmlItemDelegate(widgets.StyledItemDelegate):
    """Delegate do display HTML text.

    An alternative approach would be go grab a pixmal from a QLabel for painting.
    (see ButtonDelegate)
    """

    def paint(self, painter, option, index):
        options = widgets.StyleOptionViewItem(option)
        self.initStyleOption(options, index)
        painter.save()

        # we prepare a TextDocument with all available data
        doc = gui.TextDocument()
        doc.setTextWidth(options.rect.width())
        text_option = gui.TextOption()
        text_option.setWrapMode(gui.TextOption.WrapMode.NoWrap)
        text_option.setAlignment(options.displayAlignment)
        doc.setDefaultTextOption(text_option)
        doc.setDefaultFont(options.font)
        doc.setHtml(options.text)

        # draw everything without text
        options.text = ""
        options.widget.style().drawControl(
            QtWidgets.QStyle.ControlElement.CE_ItemViewItem, options, painter
        )

        # now we find position of our label and display our TextDocument there.
        icon_size = options.icon.actualSize(options.decorationSize)
        margin = icon_size.width()
        painter.translate(options.rect.left() + margin, options.rect.top())
        clip = QtCore.QRectF(0, 0, options.rect.width() + margin, options.rect.height())
        doc.drawContents(painter, clip)

        painter.restore()

    def sizeHint(self, option, index):
        options = widgets.StyleOptionViewItem(option)
        self.initStyleOption(options, index)

        doc = gui.TextDocument()

        text_option = gui.TextOption()
        text_option.setWrapMode(gui.TextOption.WrapMode.NoWrap)
        doc.setDefaultTextOption(text_option)
        doc.setDefaultFont(options.font)
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
    item.setBackground(gui.Color("green"))
    item.setIcon(iconprovider.get_icon("mdi.folder", as_qicon=True))
    item.setFont(gui.Font("Consolas"))
    item.set_data("user", iconprovider.get_icon("mdi.folder"))
    model += item
    w.show()
    app.main_loop()
