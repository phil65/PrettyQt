from __future__ import annotations

import logging
import re

from prettyqt import constants, core, gui, itemmodels


logger = logging.getLogger(__name__)


def escape_markdown(text: str, version: int = 1, entity_type: str | None = None) -> str:
    """Helper function to escape telegram markup symbols.

    Args:
        text: The text.
        version: Use to specify the version of telegrams Markdown.
            Either ``1`` or ``2``. Defaults to ``1``.
        entity_type: For the entity types ``PRE``, ``CODE`` and the link
            part of ``TEXT_LINKS``, only certain characters need to be escaped in
            ``MarkdownV2``.
            See the official API documentation for details. Only valid in combination with
            ``version=2``, will be ignored else.
    """
    match version:
        case 1 | "1":
            escape_chars = r"_*`["
        case 2 | "2":
            if entity_type in ["pre", "code"]:
                escape_chars = r"\`"
            elif entity_type == "text_link":
                escape_chars = r"\)"
            else:
                escape_chars = r"_*[]()~`>#+-=|{}.!"
        case _:
            raise ValueError("Markdown version must be either 1 or 2!")

    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


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
        label = escape_markdown(label)
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
