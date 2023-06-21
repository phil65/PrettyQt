from __future__ import annotations

import ast

import logging

from prettyqt import constants, core, gui, custom_models
from prettyqt.utils import bidict, treeitem

NODE_MAP = bidict(
    {
        ast.Add: "+",
        ast.Sub: "-",
        ast.Mult: "*",
        ast.Div: "/",
        ast.Mod: "%",
        ast.Eq: "==",
        ast.In: "in",
        ast.Pow: "**",
        ast.MatMult: "@",
        ast.FloorDiv: "//",
        ast.BitAnd: "&",
        ast.BitOr: "|",
        ast.BitXor: "^",
        ast.Gt: ">",
        ast.GtE: ">=",
        ast.Lt: "<",
        ast.LtE: "<=",
        ast.Is: "is",
        ast.NotEq: "!=",
        ast.IsNot: "is not",
        ast.Not: "not ",
        ast.NotIn: "not in",
        ast.And: "and",
        ast.Or: "or",
        ast.Invert: "~",
    }
)


logger = logging.getLogger(__name__)


# AstTokens library would be worth out checking for this model.


class AstModel(custom_models.TreeModel):
    """Model to display the tree of an AST node."""

    HEADER = [
        "Node type",
        "Name",
        "Line range",
        "Column range",
        "Code segement",
        "Docstring",
    ]

    def __init__(self, ast_tree, **kwargs):
        super().__init__(None, **kwargs)
        self.ast_tree = None
        self.code = ""
        self.set_ast(ast_tree)

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, ast.AST)

    def columnCount(self, parent=None):
        return len(self.HEADER) if self.ast_tree is not None else 0

    def set_ast(self, ast_tree: ast.AST | str = ""):
        match ast_tree:
            case str():
                code = ast_tree
                try:
                    node = ast.parse(ast_tree)
                except SyntaxError as e:
                    logger.debug(f"caught {e!r} when building AST")
                    return
            case ast.AST():
                code = ast.unparse(ast_tree)
                node = ast.parse(code)  # makin a circle to make sure line numbers match.
            case _:
                raise TypeError(ast_tree)
        node = ast.fix_missing_locations(node)
        with self.reset_model():
            self.ast_tree = node
            self.set_root_item(node)
            self.code = code

    # def find_lineno(self, index):
    #     # not needed, thx to ast.fix_missing_locations
    #     while not hasattr(node := index.data(constants.USER_ROLE), "lineno"):
    #         index = index.parent()
    #     return node.lineno

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.HEADER[section]
        return None

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        node = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return type(node).__name__
            case constants.DISPLAY_ROLE, 1:
                match node:
                    case _ if type(node) in NODE_MAP:
                        return NODE_MAP[type(node)]
                    case (
                        ast.Name(id=name)
                        | ast.arg(arg=name)
                        | ast.Constant(value=name)
                        | ast.alias(name=name)
                        | ast.ClassDef(name=name)
                        | ast.FunctionDef(name=name)
                    ):
                        return name
                    case str():
                        return node
            case constants.DISPLAY_ROLE, 2:
                if hasattr(node, "lineno"):
                    return f"{node.lineno} - {node.end_lineno}"
            case constants.DISPLAY_ROLE, 3:
                if hasattr(node, "col_offset"):
                    return f"{node.col_offset} - {node.end_col_offset}"
            case constants.DISPLAY_ROLE, 4:
                return ast.get_source_segment(self.code, node)
            case constants.FONT_ROLE, 4 | 5:
                return gui.Font.mono(as_qt=True)
            case constants.DISPLAY_ROLE, 5:
                try:
                    return ast.get_docstring(node)
                except TypeError:
                    return None
            case constants.USER_ROLE, _:
                return node

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        return [treeitem.TreeItem(obj=i) for i in ast.iter_child_nodes(item.obj)]

    def _has_children(self, item: treeitem.TreeItem) -> bool:
        if item.obj is None:
            return False
        return any(True for _ in ast.iter_child_nodes(item.obj))

    def rename_variable(
        self,
        old: str,
        new: str,
        root_tree: ast.AST | None = None,
        ignore: list[str] | None = None,
        scope: list[str] | None = None,
    ):
        if scope is None:
            scope = ["main"]
        if ignore is None:
            ignore = []
        if root_tree is None:
            root_tree = self.ast_tree
        for i in ast.iter_fields(root_tree):
            if not isinstance(a := getattr(root_tree, i), list):
                if a == old and not {*scope} & {*ignore}:
                    setattr(root_tree, i, new)
            n = a if isinstance(a, list) else [a]
            s = [root_tree.name] if type(root_tree).__name__.endswith("Def") else scope
            for j in n:
                if isinstance(j, ast.AST):
                    self.rename_variable(j, old, new, ignore, s)

    def get_variable_names(self):
        current_names = set()
        for node in ast.walk(self.ast_tree):
            match node:
                case ast.Name(id=name) | ast.arg(arg=name):
                    current_names.add(name)
        return current_names


if __name__ == "__main__":
    from prettyqt import widgets
    import pathlib

    app = widgets.app()
    with app.debug_mode():
        view = widgets.TreeView()
        view.setRootIsDecorated(True)
        code = pathlib.Path(__file__).read_text()
        tree = ast.parse(code)

        model = AstModel(tree, show_root=True, parent=view)
        view.set_model(model)
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("variant")
        view.resize(1000, 1000)
        view.show()
        with app.debug_mode():
            app.exec()
