from __future__ import annotations

import logging

from prettyqt import constants, core, gui, itemmodels
from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class SliceToMarkdownProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model which adds a role containing markdown-formatted text.

    Text is formatted based on FontRole, Checkstate role, etc.
    """

    class Roles:
        MarkdownRole = constants.USER_ROLE + 24453

    ID = "to_markdown"
    ICON = "mdi.palette-outline"

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not self.indexer_contains(index) or role != self.Roles.MarkdownRole:
            return super().data(index, role)
        # self.strip_styling = True
        # if role != constants.DISPLAY_ROLE and self.strip_styling:
        #     return None
        label = index.data(constants.DISPLAY_ROLE)
        if not label:
            return ""
        label = markdownizer.escape_markdown(label)
        font = index.data(constants.FONT_ROLE)
        if font and font.bold():
            label = f"**{label}**"
        if font and font.italic():
            label = f"*{label}*"
        foreground = index.data(constants.FOREGROUND_ROLE)
        # background = index.data(constants.BACKGROUND_ROLE)
        if isinstance(foreground, gui.QColor):
            label = f'<span style="color:{foreground.name()}">{label}</span>'
        match index.data(constants.CHECKSTATE_ROLE):
            case True | constants.CheckState.Checked:
                # :black_square_button:
                label = f"- [x] {label}"
            case False | constants.CheckState.Unchecked:
                # :heavy_check_mark:
                label = f"- [ ] {label}"
        return label


if __name__ == "__main__":
    import random

    from prettyqt import debugging, itemdelegates, widgets

    app = widgets.app()

    val_range = ["- [x] fksdjkk", "fkdsjkl", "jfdsk", "fdsklfjd", "fdskjdfkj", "fdskx"]
    data = dict(
        a=random.sample(val_range, k=5),
        b=random.sample(val_range, k=5),
        c=random.sample(val_range, k=5),
    )
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    # table.proxifier[:, :].color_categories()
    font = gui.QFont()
    font.setBold(True)
    table.proxifier[:, :].style(font=font, foreground="red")
    table.proxifier.get_proxy("to_markdown")
    table.proxifier[:, :].map_role(
        SliceToMarkdownProxyModel.Roles.MarkdownRole, constants.DISPLAY_ROLE
    )
    table.set_size_adjust_policy("content")
    table.setWindowTitle("Color values")
    table.set_icon("mdi.palette")
    # table.show()
    table.adjustSize()
    delegate = itemdelegates.HtmlItemDelegate(mode="markdown_commonmark")
    widget = debugging.ProxyComparerWidget(table.model(), delegate=delegate)

    widget.show()
    with app.debug_mode():
        app.exec()
