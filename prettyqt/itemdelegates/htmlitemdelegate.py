from __future__ import annotations

from prettyqt import core, gui, widgets


class BaseMarkupDelegate(widgets.StyledItemDelegate):
    # An alternative approach would be go grab a pixmap from a QLabel for painting.
    # (see ButtonDelegate)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doc = gui.TextDocument()
        self.text_option = gui.TextOption()
        self.text_option.setWrapMode(gui.TextOption.WrapMode.NoWrap)
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
        self.set_text(option.text)
        # self.doc.setTextWidth(option.rect.width())
        self.doc.setPageSize(core.QSizeF(option.rect.width(), option.rect.height()))


class HtmlItemDelegate(BaseMarkupDelegate):
    """Delegate do display HTML text."""

    ID = "html"

    def set_text(self, text: str):
        self.doc.setHtml(text)


class MarkdownItemDelegate(BaseMarkupDelegate):
    """Delegate do display Markdown text."""

    ID = "markdown"

    def __init__(self, *args, mode: str = "github", **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = mode

    def set_text(self, text: str):
        Feat = self.doc.MarkdownFeature  # noqa: N806
        match self._mode:
            case "no_html":
                self.doc.setMarkdown(text, Feat.MarkdownNoHTML)
            case "commonmark":
                self.doc.setMarkdown(text, Feat.MarkdownDialectCommonMark)
            case "github" | "":
                self.doc.setMarkdown(text, Feat.MarkdownDialectGitHub)
            case _:
                raise ValueError(self._mode)

    def get_markup_mode(self) -> str:
        return self._mode

    def set_markup_mode(self, mode: str):
        self._mode = mode

    markup_mode = core.Property(
        str,
        get_markup_mode,
        set_markup_mode,
        doc="Which markdown dialect to use.",
    )


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
