from __future__ import annotations

import ast
import enum
import logging
from typing import ClassVar

from prettyqt import constants, core, gui, itemmodels
from prettyqt.utils import bidict


SOURCE_FONT = gui.Font.mono(as_qt=True)

NODE_MAP = bidict({
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
})


logger = logging.getLogger(__name__)


# AstTokens library would be worth out checking for this model.


class AstModel(itemmodels.TreeModel):
    """Tree model to display an Abstract syntax tree.

    The model shows a tree of all nodes from an
    [abstract syntax tree](https://docs.python.org/3/library/ast.html#node-classes)
    They are part of the builtin `ast` module.

    ### Example:
    ```py
    import ast

    view = TreeView()
    code = pathlib.Path(__file__).read_text()
    tree = ast.parse(code)
    model = AstModel(tree)
    view.set_model(model)
    ```
    """

    @core.Enum
    class Roles(enum.IntEnum):
        NodeRole = constants.USER_ROLE

    SUPPORTS = ast.AST
    HEADER: ClassVar = [
        "Node type",
        "Name",
        "Line range",
        "Column range",
        "Code segement",
        "Docstring",
    ]

    def __init__(self, ast_tree: ast.AST | str, **kwargs):
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
        """Set an AST tree for the model.

        Arguments:
            ast_tree: Abstract syntax tree
        """
        match ast_tree:
            case str():
                code = ast_tree
                try:
                    node = ast.parse(ast_tree)
                except SyntaxError as e:
                    logger.debug("caught %r when building AST", e)
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
    ):
        match orientation, role, section:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.HEADER[section]
        return None

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):  # noqa: PLR0911
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
                    return (
                        f"{node.lineno} - {node.end_lineno}"
                        if node.lineno != node.end_lineno
                        else str(node.lineno)
                    )
                return None
            case constants.DISPLAY_ROLE, 3:
                if hasattr(node, "col_offset"):
                    return (
                        f"{node.col_offset} - {node.end_col_offset}"
                        if node.col_offset != node.end_col_offset
                        else str(node.col_offset)
                    )
                return None
            case constants.DISPLAY_ROLE, 4:
                return ast.get_source_segment(self.code, node)
            case constants.FONT_ROLE, 4 | 5:
                return SOURCE_FONT
            case constants.DISPLAY_ROLE, 5:
                try:
                    return ast.get_docstring(node)
                except TypeError:
                    return None
            case self.Roles.NodeRole, _:
                return node

    def _fetch_object_children(self, item: AstModel.TreeItem) -> list[AstModel.TreeItem]:
        return [self.TreeItem(obj=i) for i in ast.iter_child_nodes(item.obj)]

    def _has_children(self, item: AstModel.TreeItem) -> bool:
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
            if not isinstance(a := getattr(root_tree, i), list):  # noqa: SIM102
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
    import pathlib

    from prettyqt import widgets

    app = widgets.app()
    with app.debug_mode():
        view = widgets.TreeView()
        code = pathlib.Path(__file__).read_text()
        tree = ast.parse(code)
        model = AstModel(tree)
        view.set_model(model)
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("editor")
        view.resize(1000, 1000)
        view.show()
        with app.debug_mode():
            app.exec()
