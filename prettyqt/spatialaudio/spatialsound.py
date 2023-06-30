from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtSpatialAudio
from prettyqt.utils import bidict, datatypes


DistanceModelStr = Literal[
    "logarithmic",
    "linear",
    "manual_attenuation",
]

DISTANCE_MODEL: bidict[
    DistanceModelStr, QtSpatialAudio.QSpatialSound.DistanceModel
] = bidict(
    logarithmic=QtSpatialAudio.QSpatialSound.DistanceModel.Transparent,
    linear=QtSpatialAudio.QSpatialSound.DistanceModel.AcousticCeilingTiles,
    manual_attenuation=QtSpatialAudio.QSpatialSound.DistanceModel.BrickBare,
)

LoopsStr = Literal["infinite", "once"]

LOOPS: bidict[LoopsStr, QtSpatialAudio.QSpatialSound.Loops] = bidict(
    infinite=QtSpatialAudio.QSpatialSound.Loops.Infinite,
    once=QtSpatialAudio.QSpatialSound.Loops.Once,
)


class SpatialSound(core.ObjectMixin, QtSpatialAudio.QSpatialSound):
    def set_distance_model(
        self, model: DistanceModelStr | QtSpatialAudio.QSpatialSound.DistanceModel
    ):
        """Set the distance model.

        Args:
            model: distance model
        """
        self.setDistanceModel(DISTANCE_MODEL.get_enum_value(model))

    def get_distance_model(self) -> DistanceModelStr:
        """Return current distance model.

        Returns:
            distance model
        """
        return DISTANCE_MODEL.inverse[self.distanceModel()]

    def set_position(self, position: datatypes.Vector3DType):
        self.setPosition(datatypes.to_vector3d(position))
