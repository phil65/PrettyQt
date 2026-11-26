from prettyqt import positioning
from prettyqt.qt import QtPositioning
from prettyqt.utils import get_repr


class GeoCircle(positioning.GeoShapeMixin, QtPositioning.QGeoCircle):
    def __init__(
        self,
        center_or_other: QtPositioning.QGeoShape
        | QtPositioning.QGeoCoordinate
        | tuple[float, float]
        | None = None,
        radius: float | None = None,
    ):
        match center_or_other:
            case None:
                super().__init__()
            case QtPositioning.QGeoShape():
                super().__init__(center_or_other)
            case tuple():
                center = QtPositioning.QGeoCoordinate(*center_or_other)
                super().__init__(center, -1 if radius is None else radius)
            case _:
                super().__init__(center_or_other, -1 if radius is None else radius)

    def __repr__(self):
        return get_repr(self, self.get_center(), self.radius())

    def get_center(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.center())


if __name__ == "__main__":
    coord = (1, 1)
    circle = GeoCircle(coord)
    print(circle)
    print(repr(circle))
