from qtpy import QtMultimedia

from prettyqt import core
from prettyqt.utils import bidict


AVAILABILITY_STATUS = bidict(
    available=QtMultimedia.QMultimedia.Available,
    service_missing=QtMultimedia.QMultimedia.ServiceMissing,
    resource_error=QtMultimedia.QMultimedia.ResourceError,
    busy=QtMultimedia.QMultimedia.Busy,
)


QtMultimedia.QMediaObject.__bases__ = (core.Object,)


class MediaObject(QtMultimedia.QMediaObject):
    def __getitem__(self, value: str):
        return self.metaData(value)

    def get_availability(self) -> str:
        """Return availability status.

        Possible values: "available", "service_missing", "resource_error", "busy"

        Returns:
            availability status
        """
        return AVAILABILITY_STATUS.inverse[self.availability()]
