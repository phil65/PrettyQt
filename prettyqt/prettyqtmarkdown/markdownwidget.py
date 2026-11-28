import logging

import mknodes

from prettyqt import custom_widgets, prettyqtmarkdown, widgets
from prettyqt.utils import helpers


logger = logging.getLogger(__name__)


class MarkdownWidget(widgets.Widget):
    """A widget used for displaying a preview of a generated mknodes tree."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = widgets.TreeView()
        self.textbox = custom_widgets.CodeEditor()
        self.textbox.set_syntaxhighlighter("markdown")
        layout = self.set_layout("grid")
        layout[0, 0] = self.tree
        layout[0, 1] = self.textbox

    def set_markdown(self, item: mknodes.MkNode):
        model = prettyqtmarkdown.MkNodesModel(item)
        self.tree.set_model(model)
        self.tree.selectionModel().currentRowChanged.connect(self._on_current_change)

    def _on_current_change(self, new, old):
        if not new.isValid() or new.model() is None:
            return
        text = new.data(new.model().Roles.MarkdownRole)
        self.textbox.set_text(text)


if __name__ == "__main__":
    app = widgets.app()
    page = mknodes.MkPage()
    page += mknodes.MkAdmonition("test")
    data: dict[str, list[mknodes.MkNode | str]] = dict(a=["1", "2"], b=["c", "D"])
    page += mknodes.MkTable(data=data, header="From mapping")
    page += mknodes.MkDocStrings(helpers, header="DocStrings")
    widget = MarkdownWidget()
    widget.set_markdown(page)
    widget.show()
    app.exec()
