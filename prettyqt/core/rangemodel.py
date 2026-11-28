from typing import Any, Literal

from prettyqt import core
import prettyqt.qt
from prettyqt.utils import bidict


AutoConnectPolicyStr = Literal["none", "full", "on_read"]

AUTO_CONNECT_POLICY: bidict[AutoConnectPolicyStr, core.QRangeModel.AutoConnectPolicy] = (
    bidict(
        none=core.QRangeModel.AutoConnectPolicy.None_,
        full=core.QRangeModel.AutoConnectPolicy.Full,
        on_read=core.QRangeModel.AutoConnectPolicy.OnRead,
    )
)

DropOperationStr = Literal[
    "automatic",
    "dont_drop",
    "insert_as_children",
    "insert_as_siblings",
    "overwrite_and_extend",
    "overwrite_and_ignore",
]

DROP_OPERATION: bidict[DropOperationStr, core.QRangeModel.DropOperation] = bidict(
    automatic=core.QRangeModel.DropOperation.Automatic,
    dont_drop=core.QRangeModel.DropOperation.DontDrop,
    insert_as_children=core.QRangeModel.DropOperation.InsertAsChildren,
    insert_as_siblings=core.QRangeModel.DropOperation.InsertAsSiblings,
    overwrite_and_extend=core.QRangeModel.DropOperation.OverwriteAndExtend,
    overwrite_and_ignore=core.QRangeModel.DropOperation.OverwriteAndIgnore,
)


class RangeModel(core.AbstractItemModelMixin, core.QRangeModel):
    """Item model wrapping a Python sequence or table range."""

    def __init__(self, data: Any, *args, **kwargs):
        if prettyqt.qt.PYQT6:
            abstract_range = getattr(core, "QPyAbstractRange", ())
            if not isinstance(data, abstract_range):
                if (
                    isinstance(data, (list, tuple))
                    and data
                    and isinstance(data[0], (list, tuple))
                ):
                    data = core.QPyTableRange(data)  # ty: ignore[missing-attribute]
                else:
                    data = core.QPySequenceRange(data)  # ty: ignore[missing-attribute]
        super().__init__(data, *args, **kwargs)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"autoConnectPolicy": AUTO_CONNECT_POLICY}
        return maps

    def set_auto_connect_policy(
        self, policy: AutoConnectPolicyStr | core.QRangeModel.AutoConnectPolicy
    ):
        """Set the auto-connect policy.

        Args:
            policy: auto-connect policy to use
        """
        self.setAutoConnectPolicy(AUTO_CONNECT_POLICY.get_enum_value(policy))

    def get_auto_connect_policy(self) -> AutoConnectPolicyStr:
        """Return current auto-connect policy.

        Returns:
            auto-connect policy
        """
        return AUTO_CONNECT_POLICY.inverse[self.autoConnectPolicy()]


if __name__ == "__main__":
    model = RangeModel([1, 2, 3])
    print(model.rowCount(), model.columnCount())
