from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtSpatialAudio
from prettyqt.utils import bidict, datatypes


MaterialStr = Literal[
    "transparent",
    "acoustic_ceiling_tiles",
    "brick_bare",
    "brick_painted",
    "concrete_block_coarse",
    "concrete_block_painted",
    "curtain_heavy",
    "fiber_glass_insulation",
    "glass_thin",
    "glass_thick",
    "grass",
    "linoleumon_concrete",
    "marble",
    "metal",
    "parquet_on_concrete",
    "plaste_rrough",
    "plaste_rsmooth",
    "plywood_panel",
    "polished_concrete_or_tile",
    "sheet_rock",
    "water_or_ice_surface",
    "wood_ceiling",
    "wood_panel",
    "uniform_material",
]

MATERIAL: bidict[MaterialStr, QtSpatialAudio.QAudioRoom.Material] = bidict(
    transparent=QtSpatialAudio.QAudioRoom.Material.Transparent,
    acoustic_ceiling_tiles=QtSpatialAudio.QAudioRoom.Material.AcousticCeilingTiles,
    brick_bare=QtSpatialAudio.QAudioRoom.Material.BrickBare,
    brick_painted=QtSpatialAudio.QAudioRoom.Material.BrickPainted,
    concrete_block_coarse=QtSpatialAudio.QAudioRoom.Material.ConcreteBlockCoarse,
    concrete_block_painted=QtSpatialAudio.QAudioRoom.Material.ConcreteBlockPainted,
    curtain_heavy=QtSpatialAudio.QAudioRoom.Material.CurtainHeavy,
    fiber_glass_insulation=QtSpatialAudio.QAudioRoom.Material.FiberGlassInsulation,
    glass_thin=QtSpatialAudio.QAudioRoom.Material.GlassThin,
    glass_thick=QtSpatialAudio.QAudioRoom.Material.GlassThick,
    grass=QtSpatialAudio.QAudioRoom.Material.Grass,
    linoleumon_concrete=QtSpatialAudio.QAudioRoom.Material.LinoleumOnConcrete,
    marble=QtSpatialAudio.QAudioRoom.Material.Marble,
    metal=QtSpatialAudio.QAudioRoom.Material.Metal,
    parquet_on_concrete=QtSpatialAudio.QAudioRoom.Material.ParquetOnConcrete,
    plaste_rrough=QtSpatialAudio.QAudioRoom.Material.PlasterRough,
    plaste_rsmooth=QtSpatialAudio.QAudioRoom.Material.PlasterSmooth,
    plywood_panel=QtSpatialAudio.QAudioRoom.Material.PlywoodPanel,
    polished_concrete_or_tile=QtSpatialAudio.QAudioRoom.Material.PolishedConcreteOrTile,
    sheet_rock=QtSpatialAudio.QAudioRoom.Material.Sheetrock,
    water_or_ice_surface=QtSpatialAudio.QAudioRoom.Material.WaterOrIceSurface,
    wood_ceiling=QtSpatialAudio.QAudioRoom.Material.WoodCeiling,
    wood_panel=QtSpatialAudio.QAudioRoom.Material.WoodPanel,
    uniform_material=QtSpatialAudio.QAudioRoom.Material.UniformMaterial,
)

WallStr = Literal[
    "left_wall",
    "right_wall",
    "floor",
    "ceiling",
    "front_wall",
    "back_wall",
]

WALL: bidict[WallStr, QtSpatialAudio.QAudioRoom.Wall] = bidict(
    left_wall=QtSpatialAudio.QAudioRoom.Wall.LeftWall,
    right_wall=QtSpatialAudio.QAudioRoom.Wall.RightWall,
    floor=QtSpatialAudio.QAudioRoom.Wall.Floor,
    ceiling=QtSpatialAudio.QAudioRoom.Wall.Ceiling,
    front_wall=QtSpatialAudio.QAudioRoom.Wall.FrontWall,
    back_wall=QtSpatialAudio.QAudioRoom.Wall.BackWall,
)


class AudioRoom(core.ObjectMixin, QtSpatialAudio.QAudioRoom):
    def set_wall_material(
        self,
        wall: WallStr | QtSpatialAudio.QAudioRoom.Wall,
        material: MaterialStr | QtSpatialAudio.QAudioRoom.Material,
    ):
        """Set the wall material.

        Args:
            wall: Wall to set
            material: material type
        """
        self.setWallMaterial(WALL.get_enum_value(wall), MATERIAL.get_enum_value(material))

    def get_wall_material(
        self, wall: WallStr | QtSpatialAudio.QAudioRoom.Wall
    ) -> MaterialStr:
        """Return wall material.

        Arguments:
            wall: wall to get material for
        """
        return MATERIAL.inverse[self.wallMaterial(WALL.get_enum_value(wall))]

    def set_dimensions(self, dimensions: datatypes.Vector3DType):
        self.setDimensions(datatypes.to_vector3d(dimensions))

    def set_position(self, position: datatypes.Vector3DType):
        self.setPosition(datatypes.to_vector3d(position))
