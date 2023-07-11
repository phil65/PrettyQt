from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict


SubmitPolicyStr = Literal["auto", "manual"]

SUBMIT_POLICY: bidict[SubmitPolicyStr, widgets.QDataWidgetMapper.SubmitPolicy] = bidict(
    auto=widgets.QDataWidgetMapper.SubmitPolicy.AutoSubmit,
    manual=widgets.QDataWidgetMapper.SubmitPolicy.ManualSubmit,
)


class DataWidgetMapper(core.ObjectMixin, widgets.QDataWidgetMapper):
    """Mapping between a section of a data model to widgets."""

    def __setitem__(self, key: int, value: widgets.QWidget):
        self.addMapping(value, key)

    def __getitem__(self, key: int) -> widgets.QWidget:
        return self.mappedWidgetAt(key)

    def __delitem__(self, key_or_widget: int | widgets.QWidget):
        widget = (
            self.mappedWidgetAt(key_or_widget)
            if isinstance(key_or_widget, int)
            else key_or_widget
        )
        self.removeMapping(widget)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"submitPolicy": SUBMIT_POLICY, "orientation": constants.ORIENTATION}
        return maps

    def set_orientation(
        self, orientation: constants.OrientationStr | constants.Orientation
    ):
        """Set the orientation of the data widget mapper.

        Args:
            orientation: orientation for the data widget mapper
        """
        self.setOrientation(constants.ORIENTATION.get_enum_value(orientation))

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]

    def set_submit_policy(
        self, policy: SubmitPolicyStr | widgets.QDataWidgetMapper.SubmitPolicy
    ):
        """Set the submit policy of the mapper.

        Args:
            policy: submit_policy for the data widget mapper
        """
        self.setSubmitPolicy(SUBMIT_POLICY.get_enum_value(policy))

    def get_submit_policy(self) -> SubmitPolicyStr:
        """Return current submit policy.

        Returns:
            submit policy
        """
        return SUBMIT_POLICY.inverse[self.submitPolicy()]

    def add_mapping(
        self, widget: widgets.QWidget, section: int, property_name: str | None = None
    ):
        if property_name is None:
            self.addMapping(widget, section)
        else:
            ba = core.QByteArray(property_name.encode())
            self.addMapping(widget, section, ba)

    def get_mapped_property_name(self, widget: widgets.QWidget) -> str:
        return self.mappedPropertyName(widget).data().decode()


if __name__ == "__main__":
    mapper = DataWidgetMapper()
