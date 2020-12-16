from typing import Optional

from qtpy import QtLocation

from prettyqt import positioning
from prettyqt.utils import InvalidParamError, bidict


INSTRUCTION_DIRECTION = bidict(
    none=QtLocation.QGeoManeuver.NoDirection,
    forward=QtLocation.QGeoManeuver.DirectionForward,
    bear_right=QtLocation.QGeoManeuver.DirectionBearRight,
    light_right=QtLocation.QGeoManeuver.DirectionLightRight,
    right=QtLocation.QGeoManeuver.DirectionRight,
    hard_right=QtLocation.QGeoManeuver.DirectionHardRight,
    u_turn_right=QtLocation.QGeoManeuver.DirectionUTurnRight,
    u_turn_left=QtLocation.QGeoManeuver.DirectionUTurnLeft,
    hard_left=QtLocation.QGeoManeuver.DirectionHardLeft,
    left=QtLocation.QGeoManeuver.DirectionLeft,
    light_left=QtLocation.QGeoManeuver.DirectionLightLeft,
    bear_left=QtLocation.QGeoManeuver.DirectionBearLeft,
)


class GeoManeuver(QtLocation.QGeoManeuver):
    def __bool__(self):
        return self.isValid()

    def __str__(self):
        return self.instructionText()

    def __setitem__(self, index: str, val):
        attrs = self.extendedAttributes()
        attrs[index] = val
        self.setExtendedAttributes(attrs)

    def __getitem__(self, index: str):
        attr = self.extendedAttributes()
        if index not in attr:
            raise KeyError(f"Key {index!r} does not exist.")
        return attr[index]

    def get_position(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.position())

    def get_waypoint(self) -> Optional[positioning.GeoCoordinate]:
        wp = self.waypoint()
        if not wp.isValid():
            return None
        return positioning.GeoCoordinate(wp)

    def set_direction(self, direction: str):
        """Set the direction.

        Allowed values are "none", "forward", "bear_right", "light_right", "right",
                           "hard_right", "u_turn_right", "bear_left", "light_left",
                           "left", "hard_left", "u_turn_left"

        Args:
            direction: Direction

        Raises:
            InvalidParamError: direction does not exist
        """
        if direction not in INSTRUCTION_DIRECTION:
            raise InvalidParamError(direction, INSTRUCTION_DIRECTION)
        self.setDirection(INSTRUCTION_DIRECTION[direction])

    def get_direction(self) -> str:
        """Return current direction.

        Possible values: "none", "forward", "bear_right", "light_right", "right",
                         "hard_right", "u_turn_right", "bear_left", "light_left", "left",
                         "hard_left", "u_turn_left"

        Returns:
            Direction
        """
        return INSTRUCTION_DIRECTION.inverse[self.direction()]


if __name__ == "__main__":
    maneuver = GeoManeuver()
    print(bool(maneuver))
    maneuver.setExtendedAttributes(dict(a="a"))
    maneuver["test"] = "test"
    print(bool(maneuver))
    waypoint = maneuver.get_waypoint()
    print(bool(waypoint))
    print(maneuver.extendedAttributes())
