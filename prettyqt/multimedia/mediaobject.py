from typing import Literal

from qtpy import QtMultimedia

from prettyqt import core
from prettyqt.utils import bidict


AVAILABILITY_STATUS = bidict(
    available=QtMultimedia.QMultimedia.Available,
    service_missing=QtMultimedia.QMultimedia.ServiceMissing,
    resource_error=QtMultimedia.QMultimedia.ResourceError,
    busy=QtMultimedia.QMultimedia.Busy,
)

AvailabilityStatusStr = Literal["available", "service_missing", "resource_error", "busy"]

QtMultimedia.QMediaObject.__bases__ = (core.Object,)


class MediaObject(QtMultimedia.QMediaObject):
    def __getitem__(self, value: str):
        return self.metaData(value)

    def get_availability(self) -> AvailabilityStatusStr:
        """Return availability status.

        Returns:
            availability status
        """
        return AVAILABILITY_STATUS.inverse[self.availability()]
