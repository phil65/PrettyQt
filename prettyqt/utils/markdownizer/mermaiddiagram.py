from __future__ import annotations

import textwrap

from typing import Literal

from prettyqt.utils import helpers, markdownizer


GraphTypeStr = Literal["TODO"]


class MermaidDiagram(markdownizer.Code):
    TYPE_MAP = dict(
        flow="graph",
        sequence="sequenceDiagram",
        state="stateDiagram-v2",
    )
    ORIENTATION = dict(
        default="",
        left_right="LR",
        top_down="TD",
        right_left="RL",
        down_top="DT",
    )

    def __init__(
        self,
        graph_type: GraphTypeStr,
        items,
        connections,
        orientation: str = "",
        attributes: dict[str, str] | None = None,
        header: str = "",
    ):
        super().__init__(language="mermaid", header=header)
        self.graph_type = (
            graph_type if graph_type not in self.TYPE_MAP else self.TYPE_MAP[graph_type]
        )
        self.orientation = (
            orientation
            if orientation not in self.ORIENTATION
            else self.ORIENTATION[orientation]
        )
        self.items = set(items)
        self.connections = set(connections)
        self.attributes = attributes or {}

    @classmethod
    def for_classes(cls, klasses, header: str = ""):
        items, connections = helpers.get_connections(
            klasses, child_getter=lambda x: x.__bases__
        )
        items = [markdownizer.label_for_class(i) for i in items]
        connections = [
            (markdownizer.label_for_class(i), markdownizer.label_for_class(j))
            for i, j in connections
        ]
        return cls(
            graph_type="flow",
            orientation="TD",
            items=items,
            connections=connections,
            header=header,
        )

    @classmethod
    def for_subclasses(cls, klasses, header: str = ""):
        items, connections = helpers.get_connections(
            klasses,
            child_getter=lambda x: x.__subclasses__(),
            id_getter=lambda x: x.__name__,
        )
        return cls(
            graph_type="flow",
            orientation="RL",
            items=items,
            connections=connections,
            header=header,
        )

    def _to_markdown(self) -> str:
        items = list(self.items) + [f"{a} --> {b}" for a, b in self.connections]
        item_str = textwrap.indent("\n".join(items), "  ")
        text = f"{self.graph_type} {self.orientation}\n{item_str}"
        return f"```mermaid\n{text}\n```"
