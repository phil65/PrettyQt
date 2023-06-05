from __future__ import annotations

from typing import Literal

from prettyqt import constants, core
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


SUBMIT_POLICY = bidict(
    auto=QtWidgets.QDataWidgetMapper.SubmitPolicy.AutoSubmit,
    manual=QtWidgets.QDataWidgetMapper.SubmitPolicy.ManualSubmit,
)

SubmitPolicyStr = Literal["auto", "manual"]


class DataWidgetMapper(core.ObjectMixin, QtWidgets.QDataWidgetMapper):
    def __setitem__(self, key: int, value: QtWidgets.QWidget):
        self.addMapping(value, key)

    def __getitem__(self, key: int) -> QtWidgets.QWidget:
        return self.mappedWidgetAt(key)

    def __delitem__(self, key_or_widget: int | QtWidgets.QWidget):
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

    def set_orientation(self, orientation: constants.OrientationStr):
        """Set the orientation of the data widget mapper.

        Args:
            orientation: orientation for the data widget mapper

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in constants.ORIENTATION:
            raise InvalidParamError(orientation, constants.ORIENTATION)
        self.setOrientation(constants.ORIENTATION[orientation])

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]

    def set_submit_policy(self, policy: SubmitPolicyStr):
        """Set the submit policy of the mapper.

        Args:
            policy: submit_policy for the data widget mapper

        Raises:
            InvalidParamError: submit_policy does not exist
        """
        if policy not in SUBMIT_POLICY:
            raise InvalidParamError(policy, SUBMIT_POLICY)
        self.setSubmitPolicy(SUBMIT_POLICY[policy])

    def get_submit_policy(self) -> SubmitPolicyStr:
        """Return current submit policy.

        Returns:
            submit policy
        """
        return SUBMIT_POLICY.inverse[self.submitPolicy()]

    def add_mapping(
        self, widget: QtWidgets.QWidget, section: int, property_name: str | None = None
    ):
        if property_name is None:
            self.addMapping(widget, section)
        else:
            ba = QtCore.QByteArray(property_name.encode())
            self.addMapping(widget, section, ba)

    def get_mapped_property_name(self, widget: QtWidgets.QWidget) -> str:
        return self.mappedPropertyName(widget).data().decode()


if __name__ == "__main__":
    mapper = DataWidgetMapper()
