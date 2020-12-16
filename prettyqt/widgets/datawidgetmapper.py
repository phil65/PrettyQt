from typing import Literal

from qtpy import QtWidgets

from prettyqt import constants, core
from prettyqt.utils import InvalidParamError, bidict


SUBMIT_POLICY = bidict(
    auto=QtWidgets.QDataWidgetMapper.AutoSubmit,
    manual=QtWidgets.QDataWidgetMapper.ManualSubmit,
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
