from __future__ import annotations

import ast
import logging

from prettyqt import constants, core, custom_widgets, itemmodels, widgets


logger = logging.getLogger(__name__)


class AstViewer(widgets.Splitter):
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

    def set_ast(self, ast_tree: str):
        if self.tree.model() is None:
            model = itemmodels.AstModel(ast_tree, show_root=True, parent=self.tree)
            self.tree.set_model(model)
            self.tree.selectionModel().currentChanged.connect(self._on_current_change)
        else:
            self.tree.model().set_ast(ast_tree)
        self.tree.show_root(False)
        self.tree.expandAll()
        dumped = ast.dump(self.tree.model().ast_tree, indent=4)
        self.ast_textedit.set_text(dumped)

    def rename_variable(
        self,
        old: str,
        new: str,
        ignore: list[str] | None = None,
        scope: list[str] | None = None,
    ):
        if scope is None:
            scope = ["main"]
        if ignore is None:
            ignore = []
        tree = self.tree.model().ast_tree
        for i in ast.iter_fields(tree):
            if not isinstance(a := getattr(tree, i), list):
                if a == old and not {*scope} & {*ignore}:
                    setattr(tree, i, new)
            n = a if isinstance(a, list) else [a]
            s = [tree.name] if tree.__class__.__name__.endswith("Def") else scope
            for j in n:
                if isinstance(j, ast.AST):
                    self.rename_variable(j, old, new, ignore, s)


if __name__ == "__main__":
    app = widgets.app()
    w = AstViewer()
    w.show()
    with app.debug_mode():
        app.exec()
