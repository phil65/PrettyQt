from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


AccuracyStr = Literal["approximate", "precise"]

ACCURACY: bidict[AccuracyStr, QtCore.QLocationPermission.Accuracy] = bidict(
    approximate=QtCore.QLocationPermission.Accuracy.Approximate,
    precise=QtCore.QLocationPermission.Accuracy.Precise,
)

AvailabilityStr = Literal["when_in_use", "always"]

AVAILABILITY: bidict[AvailabilityStr, QtCore.QLocationPermission.Availability] = bidict(
    when_in_use=QtCore.QLocationPermission.Availability.WhenInUse,
    always=QtCore.QLocationPermission.Availability.Always,
)


class LocationPermission(QtCore.QLocationPermission):
    """Access the user's location."""

    def set_accuracy(self, accuracy: AccuracyStr | QtCore.QLocationPermission.Accuracy):
        """Set the desired location accuracy.

        Args:
            accuracy: accuracy to use
        """
        self.setAccuracy(ACCURACY.get_enum_value(accuracy))

    def get_accuracy(self) -> AccuracyStr:
        """Return current location accuracy.

        Returns:
            location accuracy
        """
        return ACCURACY.inverse[self.accuracy()]

    def set_availability(
        self, availability: AvailabilityStr | QtCore.QLocationPermission.Availability
    ):
        """Set the desired location availability.

        Args:
            availability: availability to use
        """
        self.setAvailability(AVAILABILITY.get_enum_value(availability))

    def get_availability(self) -> AvailabilityStr:
        """Return current location availability.

        Returns:
            location availability
        """
        return AVAILABILITY.inverse[self.availability()]
