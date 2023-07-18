from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtQuick
from prettyqt.utils import bidict


DIRTY_STATE_BIT = bidict(
    matrix=QtQuick.QSGNode.DirtyStateBit.DirtyMatrix,
    node_added=QtQuick.QSGNode.DirtyStateBit.DirtyNodeAdded,
    node_removed=QtQuick.QSGNode.DirtyStateBit.DirtyNodeRemoved,
    geometry=QtQuick.QSGNode.DirtyStateBit.DirtyGeometry,
    material=QtQuick.QSGNode.DirtyStateBit.DirtyMaterial,
    opacity=QtQuick.QSGNode.DirtyStateBit.DirtyOpacity,
    # subtree_blocked=QtQuick.QSGNode.DirtyStateBit.DirtySubtreeBlocked,
)

DirtyStateBitStr = Literal[
    "matrix",
    "node_added",
    "node_removed",
    "geometry",
    "material",
    "opacity",
    "subtree_blocked",
]

FLAG = bidict(
    owned_by_parent=QtQuick.QSGNode.Flag.OwnedByParent,
    use_preprocess=QtQuick.QSGNode.Flag.UsePreprocess,
    owns_geometry=QtQuick.QSGNode.Flag.OwnsGeometry,
    owns_material=QtQuick.QSGNode.Flag.OwnsMaterial,
    owns_opaque_material=QtQuick.QSGNode.Flag.OwnsOpaqueMaterial,
)

FlagStr = Literal[
    "owned_by_parent",
    "use_preprocess",
    "owns_geometry",
    "owns_material",
    "owns_opaque_material",
]

NODE_TYPE = bidict(
    basic=QtQuick.QSGNode.NodeType.BasicNodeType,
    geometry=QtQuick.QSGNode.NodeType.GeometryNodeType,
    transform=QtQuick.QSGNode.NodeType.TransformNodeType,
    clip=QtQuick.QSGNode.NodeType.ClipNodeType,
    opacity=QtQuick.QSGNode.NodeType.OpacityNodeType,
    # render=QtQuick.QSGNode.NodeType.RenderNodeType,
)

NodeTypeStr = Literal[
    "basic",
    "geometry",
    "transform",
    "clip",
    "opacity",
    "render",
]


class SGNode(QtQuick.QSGNode):
    """The base class for all nodes in the scene graph."""

    def __getitem__(self, index: int) -> QtQuick.QSGNode:
        return self.childAtIndex(index)

    def __delitem__(self, item: int | QtQuick.QSGNode):
        if isinstance(item, int):
            item = self.childAtIndex(item)
        self.removeChildNode(item)

    def get_type(self) -> NodeTypeStr:
        """Get the type of the node.

        Returns:
            Node type
        """
        return NODE_TYPE.inverse[self.type()]

    def get_flags(self) -> list[FlagStr]:
        return FLAG.get_list(self.flags())

    def get_children(self, recursive: bool = False) -> list[SGNode]:
        """Get children of this item.

        recursive option is written iteratively to also support original QTreeWidgetItems.
        """
        if not recursive:
            return [self.childAtIndex(i) for i in range(self.childCount())]
        results = []
        nodes = [self]
        while nodes:
            items = []
            for node in nodes:
                results.append(node)
                items.extend(node.childAtIndex(i) for i in range(node.childCount()))
            nodes = items
        return results[1:]


if __name__ == "__main__":
    node = SGNode()
