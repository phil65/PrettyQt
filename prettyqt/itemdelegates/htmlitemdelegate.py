from __future__ import annotations

from prettyqt import core, gui, widgets


class HtmlItemDelegate(widgets.StyledItemDelegate):
    ID = "html"
    """Delegate do display HTML text.

    An alternative approach would be go grab a pixmal from a QLabel for painting.
    (see ButtonDelegate)
    """

    def __init__(self, mode: str = "html", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doc = gui.TextDocument()
        self.text_option = gui.TextOption()
        self.text_option.setWrapMode(gui.TextOption.WrapMode.NoWrap)
        self._mode = mode
        self.doc.setDefaultTextOption(self.text_option)
        self.doc.setDocumentMargin(0)

    def paint(
        self,
        painter: gui.QPainter,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        painter.save()
        option = widgets.StyleOptionViewItem(option)
        self.initStyleOption(option, index)
        self.prepare_doc(option)
        # draw everything without text
        option.text = ""
        option.widget.style().drawControl(
            widgets.QStyle.ControlElement.CE_ItemViewItem, option, painter
        )

        # now we find position of our label and display our TextDocument there.
        icon_size = option.icon.actualSize(option.decorationSize)
        margin = icon_size.width()
        painter.translate(option.rect.left() + margin, option.rect.top())
        clip = core.QRectF(0, 0, option.rect.width() + margin, option.rect.height())
        self.doc.drawContents(painter, clip)

        painter.restore()

    def sizeHint(self, option: widgets.QStyleOptionViewItem, index: core.ModelIndex):
        option = widgets.StyleOptionViewItem(option)
        self.initStyleOption(option, index)
        self.prepare_doc(option)
        return core.QSize(int(self.doc.idealWidth()), int(self.doc.size().height()))

    def prepare_doc(self, option: widgets.QStyleOptionViewItem):
        self.text_option.setAlignment(option.displayAlignment)
        self.doc.setDefaultFont(option.font)
        Feat = self.doc.MarkdownFeature
        match self._mode:
            case "html":
                self.doc.setHtml(option.text)
            case "markdown_no_html":
                self.doc.setMarkdown(option.text, Feat.MarkdownNoHTML)
            case "markdown_commonmark":
                self.doc.setMarkdown(option.text, Feat.MarkdownDialectCommonMark)
            case "markdown_github":
                self.doc.setMarkdown(option.text, Feat.MarkdownDialectGitHub)
        # self.doc.setTextWidth(option.rect.width())
        self.doc.setPageSize(core.QSizeF(option.rect.width(), option.rect.height()))

    def get_markup_mode(self, str):
        return self._mode

    def set_markup_mode(self, mode: str):
        self._mode = mode

    markup_mode = core.Property(str, get_markup_mode, set_markup_mode)


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
    item.setFont(gui.Font.mono())
    item.set_data(iconprovider.get_icon("mdi.folder"), "user")
    model += item
    w.show()
    app.exec()
