# -*- coding: utf-8 -*-

from qtpy import QtWidgets, QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError

ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)

SUBMIT_POLICIES = bidict(
    auto=QtWidgets.QDataWidgetMapper.AutoSubmit,
    manual=QtWidgets.QDataWidgetMapper.ManualSubmit,
)

QtWidgets.QDataWidgetMapper.__bases__ = (core.Object,)


class DataWidgetMapper(QtWidgets.QDataWidgetMapper):
    def serialize_fields(self):
        return dict(
            current_index=self.currentIndex(),
            orientation=self.get_orientation(),
            submit_policy=self.get_submit_policy(),
        )

    def set_orientation(self, orientation: str):
        """Set the orientation of the splitter.

        Allowed values are "horizontal", "vertical"

        Args:
            orientation: orientation for the splitter

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in ORIENTATIONS:
            raise InvalidParamError(orientation, ORIENTATIONS)
        self.setOrientation(ORIENTATIONS[orientation])

    def get_orientation(self) -> str:
        """Return current orientation.

        Possible values: "horizontal", "vertical"

        Returns:
            orientation
        """
        return ORIENTATIONS.inv[self.orientation()]

    def set_submit_policy(self, policy: str):
        """Set the submit policy of the mapper.

        Allowed values are "auto", "manual"

        Args:
            submit_policy: submit_policy for the splitter

        Raises:
            InvalidParamError: submit_policy does not exist
        """
        if policy not in SUBMIT_POLICIES:
            raise InvalidParamError(policy, SUBMIT_POLICIES)
        self.setSubmitPolicy(SUBMIT_POLICIES[policy])

    def get_submit_policy(self) -> str:
        """Return current submit policy.

        Possible values: "auto", "manual"

        Returns:
            submit policy
        """
        return SUBMIT_POLICIES.inv[self.submitPolicy()]
