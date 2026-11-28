from prettyqt import core, widgets


class GraphicsAnchor(core.ObjectMixin, widgets.QGraphicsAnchor):
    """Represents an anchor between two items in a QGraphicsAnchorLayout."""

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"sizePolicy": widgets.sizepolicy.SIZE_POLICY}
        return maps

    def set_size_policy(
        self, policy: widgets.sizepolicy.SizePolicyStr | widgets.QSizePolicy.Policy
    ):
        """Set the size policy of the anchor.

        Args:
            policy: size policy to use
        """
        self.setSizePolicy(widgets.sizepolicy.SIZE_POLICY.get_enum_value(policy))

    def get_size_policy(self) -> widgets.sizepolicy.SizePolicyStr:
        """Return current size policy.

        Returns:
            size policy
        """
        return widgets.sizepolicy.SIZE_POLICY.inverse[self.sizePolicy()]
