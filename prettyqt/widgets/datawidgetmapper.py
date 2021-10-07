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

QtWidgets.QDataWidgetMapper.__bases__ = (core.Object,)


class DataWidgetMapper(QtWidgets.QDataWidgetMapper):
    def serialize_fields(self):
        return dict(
            current_index=self.currentIndex(),
            orientation=self.get_orientation(),
            submit_policy=self.get_submit_policy(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_orientation(state["orientation"])
        self.set_submit_policy(state["submit_policy"])
        self.setCurrentIndex(state["current_index"])

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
        return bytes(self.mappedPropertyName(widget)).decode()
