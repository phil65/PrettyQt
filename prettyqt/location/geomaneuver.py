from __future__ import annotations

from typing import Literal

from prettyqt import positioning
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


InstructionDirectionStr = Literal[
    "none",
    "forward",
    "bear_right",
    "light_right",
    "right",
    "hard_right",
    "u_turn_right",
    "u_turn_left",
    "hard_left",
    "left",
    "light_left",
    "bear_left",
]

INSTRUCTION_DIRECTION: bidict[
    InstructionDirectionStr, QtLocation.QGeoManeuver.InstructionDirection
] = bidict(
    none=QtLocation.QGeoManeuver.InstructionDirection.NoDirection,
    forward=QtLocation.QGeoManeuver.InstructionDirection.DirectionForward,
    bear_right=QtLocation.QGeoManeuver.InstructionDirection.DirectionBearRight,
    light_right=QtLocation.QGeoManeuver.InstructionDirection.DirectionLightRight,
    right=QtLocation.QGeoManeuver.InstructionDirection.DirectionRight,
    hard_right=QtLocation.QGeoManeuver.InstructionDirection.DirectionHardRight,
    u_turn_right=QtLocation.QGeoManeuver.InstructionDirection.DirectionUTurnRight,
    u_turn_left=QtLocation.QGeoManeuver.InstructionDirection.DirectionUTurnLeft,
    hard_left=QtLocation.QGeoManeuver.InstructionDirection.DirectionHardLeft,
    left=QtLocation.QGeoManeuver.InstructionDirection.DirectionLeft,
    light_left=QtLocation.QGeoManeuver.InstructionDirection.DirectionLightLeft,
    bear_left=QtLocation.QGeoManeuver.InstructionDirection.DirectionBearLeft,
)


class GeoManeuver(QtLocation.QGeoManeuver):
    """Represents info relevant to the point at which two QGeoRouteSegments meet."""

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
            msg = f"Key {index!r} does not exist."
            raise KeyError(msg)
        return attr[index]

    def get_position(self) -> positioning.GeoCoordinate:
        return positioning.GeoCoordinate(self.position())

    def get_waypoint(self) -> positioning.GeoCoordinate | None:
        wp = self.waypoint()
        return positioning.GeoCoordinate(wp) if wp.isValid() else None

    def set_direction(
        self,
        direction: InstructionDirectionStr | QtLocation.QGeoManeuver.InstructionDirection,
    ):
        """Set the direction.

        Args:
            direction: Direction
        """
        self.setDirection(INSTRUCTION_DIRECTION.get_enum_value(direction))

    def get_direction(self) -> InstructionDirectionStr:
        """Return current direction.

        Returns:
            Direction
        """
        return INSTRUCTION_DIRECTION.inverse[self.direction()]


if __name__ == "__main__":
    maneuver = GeoManeuver()
    maneuver.setExtendedAttributes(dict(a="a"))
    maneuver["test"] = "test"
    waypoint = maneuver.get_waypoint()
