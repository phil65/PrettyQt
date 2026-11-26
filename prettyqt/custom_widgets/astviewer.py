import ast
import logging
from typing import TYPE_CHECKING

from prettyqt import constants, custom_widgets, itemmodels, widgets


if TYPE_CHECKING:
    from prettyqt import core


logger = logging.getLogger(__name__)


class AstViewer(widgets.Splitter):
    """Widget which displays an AST Tree next to the corresponding source code.

    Selecting a node in the tree will highlight the corresponing text section in source.

    ``` py
    widget = custom_widgets.AstViewer()
    widget.show()
    ```

    <figure markdown>
      ![Image title](../../images/astviewer.png)
      <figcaption>AstViewer widget</figcaption>
    </figure>
    """

    def __init__(
        self,
        object_name="ast_viewer",
        **kwargs,
    ):
        super().__init__(orientation="horizontal", object_name=object_name, **kwargs)
        self.tree = widgets.TreeView()
        self.ast_textedit = widgets.PlainTextEdit()
        self.tabwidget = widgets.TabWidget()
        self.tabwidget.add_tab(self.tree, "Tree")
        self.tabwidget.add_tab(self.ast_textedit, "Dumped")

        self.textedit = custom_widgets.CodeEditor()
        self.textedit.set_syntaxhighlighter("python")
        self.textedit.textChanged.connect(self._on_text_change)
        self.add(self.tabwidget)
        self.add(self.textedit)

    def _on_text_change(self):
        self.set_ast(self.textedit.get_value())

    def _on_current_change(self, new_index: core.ModelIndex, _):
        node = new_index.data(constants.USER_ROLE)
        if not hasattr(node, "lineno"):
            return
        with self.textedit.selecter.current_cursor() as cursor:
            cursor.select_text(
                (node.lineno - 1, node.col_offset),
                (node.end_lineno - 1, node.end_col_offset),
            )

    def set_ast(self, ast_or_str: str | ast.AST):
        model = self.tree.get_model(skip_proxies=True)
        if not isinstance(model, itemmodels.AstModel):
            model = itemmodels.AstModel(ast_or_str, show_root=True, parent=self.tree)
            self.tree.set_model(model)
            self.tree.selectionModel().currentChanged.connect(self._on_current_change)
        else:
            model.set_ast(ast_or_str)
        self.tree.show_root(False)
        self.tree.expandAll()
        ast_tree = model.ast_tree
        text = ast_or_str if isinstance(ast_or_str, str) else ast.unparse(ast_or_str)
        with self.textedit.signals_blocked():
            self.textedit.set_text(text)
        dumped = ast.dump(ast_tree, indent=4) if ast_tree is not None else ""
        self.ast_textedit.set_text(dumped)

    def rename_variable(
        self,
        old: str,
        new: str,
        ignore: list[str] | None = None,
        scope: list[str] | None = None,
    ):
        """Rename all identifiers named `old` to `new` (see AstModel.rename_variable)."""
        model = self.tree.get_model(skip_proxies=True)
        if not isinstance(model, itemmodels.AstModel):
            raise TypeError(model)
        model.rename_variable(old, new, ignore=ignore, scope=scope)
        if model.ast_tree is not None:
            self.set_ast(model.ast_tree)

    # @classmethod
    # def setup_example(cls):
    #     import pathlib

    #     widget = cls()
    #     code = pathlib.Path(__file__).read_text("utf-8")
    #     widget.set_ast(code)
    #     return widget


if __name__ == "__main__":
    app = widgets.app()
    w = AstViewer.setup_example()
    w.show()
    with app.debug_mode():
        app.exec()
