from __future__ import annotations

import logging

from prettyqt import constants, core, gui, itemmodels
from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)

# HTML <h{i}> to font px size map
FONT_SIZE_MAP = {1: 34, 2: 30, 3: 24, 4: 20, 5: 18, 6: 16}


class SliceToMarkdownProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model which transforms cell contents to markdown.

    Mainly used for documentation files.
    Text is formatted based on FontRole, Checkstate role, etc.
    """

    ID = "to_markdown"
    ICON = "mdi.palette-outline"

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not self.indexer_contains(index):
            return super().data(index, role)
        if role != constants.DISPLAY_ROLE:
            return None
        # self.strip_styling = True
        # if role != constants.DISPLAY_ROLE and self.strip_styling:
        #     return None
        label = super().data(index, constants.DISPLAY_ROLE)
        checkstate = super().data(index, constants.CHECKSTATE_ROLE)
        # if not label and checkstate is None:
        #     return ""
        label = markdownizer.escaped(str(label) if label is not None else "")
        if label:
            # background = super().data(index, constants.BACKGROUND_ROLE)
            foreground = super().data(index, constants.FOREGROUND_ROLE)
            if isinstance(foreground, gui.QColor):
                label = f'<span style="color:{foreground.name()}">{label}</span>'
            font = super().data(index, constants.FONT_ROLE)
            if font and font.bold():
                label = f"**{label}**"
            if font and font.italic():
                label = f"*{label}*"
        match checkstate:
            case True | constants.CheckState.Checked | 2:
                # :black_square_button:
                label = f"☑ {label}"
            case False | constants.CheckState.Unchecked | 0:
                # :heavy_check_mark:
                label = f"☐ {label}"
        return label

    # def is_using_display_role(self):
    #     return True

    # def use_display_role(self, val: bool):
    #     pass

    # use_display_role = core.Property(bool, is_using_display_role, use_display_role)


if __name__ == "__main__":
    from prettyqt import debugging, itemdelegates, itemmodels, widgets

    app = widgets.app()

    model = itemmodels.QObjectPropertiesModel(app)
    table = widgets.TableView()
    table.set_model(model)
    # table.proxifier[:, :].color_categories()
    font = gui.QFont()
    font.setBold(True)
    table.proxifier[:, :].style(font=font, foreground="red")
    table.proxifier.get_proxy("to_markdown")
    table.set_size_adjust_policy("content")
    table.setWindowTitle("Color values")
    table.set_icon("mdi.palette")
    # table.show()
    table.adjustSize()
    delegate = itemdelegates.MarkdownItemDelegate(mode="commonmark")
    widget = debugging.ProxyComparerWidget(table.model(), delegate=None)

    widget.show()
    with app.debug_mode():
        app.exec()
