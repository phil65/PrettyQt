from __future__ import annotations

import dataclasses
import logging

from prettyqt.utils import helpers


logger = logging.getLogger(__name__)

# Link are created following the documentation here :
# https://mermaid.js.org/syntax/flowchart.html#links-between-nodes
LINK_SHAPES = {"normal": "---", "dotted": "-.-", "thick": "==="}

LINK_HEADS = {"none": "", "arrow": ">", "left-arrow": "<", "bullet": "o", "cross": "x"}


@dataclasses.dataclass
class NodeShape:
    start: str
    end: str


# Shapes are created following the documentation here :
# https://mermaid.js.org/syntax/flowchart.html#node-shapes


NODE_SHAPES = {
    "normal": NodeShape("[", "]"),
    "round-edge": NodeShape("(", ")"),
    "stadium-shape": NodeShape("([", "])"),
    "subroutine-shape": NodeShape("[[", "]]"),
    "cylindrical": NodeShape("[(", ")]"),
    "circle": NodeShape("((", "))"),
    "label-shape": NodeShape(">", "]"),
    "rhombus": NodeShape("{", ")"),
    "hexagon": NodeShape("{{", ")}"),
    "parallelogram": NodeShape("[/", "/]"),
    "parallelogram-alt": NodeShape("[\\", "\\]"),
    "trapezoid": NodeShape("[/", "\\]"),
    "trapezoid-alt": NodeShape("[\\", "/]"),
    "double-circle": NodeShape("(((", ")))"),
}


class Node:
    def __init__(
        self,
        identifier: str,
        content: str = "",
        shape: str = "normal",
        sub_nodes: list = None,
    ):
        sub_nodes = sub_nodes or []
        self.id = helpers.to_snake(identifier)
        self.content = content if content else self.id
        self.shape = NODE_SHAPES[shape]
        self.sub_nodes = sub_nodes

        # TODO: verify that content match a working string pattern

    def add_sub_nodes(self, new_nodes: list[Node] = None):
        if new_nodes is None:
            new_nodes = []
        self.sub_nodes = self.sub_nodes + new_nodes

    def __repr__(self):
        return f"{self.id}['{self.content}'] Nb_children:{len(self.sub_nodes)}"

    def __str__(self):
        return "" + (
            "\n".join(
                [
                    f'subgraph {self.id} ["{self.content}"]',
                    "\n".join([str(node) for node in self.sub_nodes]),
                    "end",
                ]
            )
            if len(self.sub_nodes)
            else "".join([self.id, self.shape.start, f'"{self.content}"', self.shape.end])
        )


class Link:
    def __init__(
        self,
        origin: Node,
        end: Node,
        shape: str = "normal",
        head_left: str = "none",
        head_right: str = "arrow",
        message: str = "",
    ):
        self.origin = origin
        self.end = end
        self.head_left = LINK_HEADS[head_left]
        self.head_right = LINK_HEADS[head_right]
        self.shape = LINK_SHAPES[shape]
        self.message = message

    def __str__(self):
        elements = [
            f"{self.origin.id} ",
            self.head_left,
            self.shape,
            self.head_right,
            f"|{self.message}|" if self.message else "",
            f" {self.end.id}",
        ]
        return "".join(elements)


if __name__ == "__main__":
    pass
