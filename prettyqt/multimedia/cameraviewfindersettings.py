# -*- coding: utf-8 -*-
from dataclasses import dataclass, asdict
from typing import Tuple, Dict, Any

from qtpy import QtMultimedia

from prettyqt import multimedia
from prettyqt.utils import InvalidParamError

PIXEL_FORMAT = multimedia.videoframe.PIXEL_FORMAT  # type: ignore


@dataclass
class Settings(object):
    maximum_framerate: int
    minimum_framerate: int
    pixel_aspect_ratio: Tuple[int, int]
    pixel_format: str
    resolution: Tuple[int, int]


class CameraViewfinderSettings(QtMultimedia.QCameraViewfinderSettings):
    def __getitem__(self, index: str):
        return self.to_dict()[index]

    def __setitem__(self, index: str, value):
        if index == "maximum_framerate":
            self.setMaximumFrameRate(value)
        elif index == "minimum_framerate":
            self.setMinimumFrameRate(value)
        elif index == "pixel_aspect_ratio":
            self.setPixelAspectRatio(*value)
        elif index == "pixel_format":
            self.set_pixel_format(value)
        elif index == "resolution":
            self.setResolution(*value)

    def __iter__(self):
        return iter(self.to_dict().keys())

    def __len__(self):
        return len(self.to_dict())

    def set_pixel_format(self, fmt: str):
        if fmt not in PIXEL_FORMAT:
            raise InvalidParamError(fmt, PIXEL_FORMAT)
        self.setPixelFormat(PIXEL_FORMAT[fmt])

    def get_pixel_format(self) -> str:
        return PIXEL_FORMAT.inv[self.pixelFormat()]

    def to_dataclass(self) -> Settings:
        size = self.resolution()
        ar = self.pixelAspectRatio()
        return Settings(
            maximum_framerate=self.maximumFrameRate(),
            minimum_framerate=self.minimumFrameRate(),
            pixel_aspect_ratio=(ar.width(), ar.height()),
            pixel_format=self.get_pixel_format(),
            resolution=(size.width(), size.height()),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self.to_dataclass())

    @classmethod
    def from_dataclass(cls, data: Settings) -> "CameraViewfinderSettings":
        instance = cls()
        instance.setMaximumFrameRate(data.maximum_framerate)
        instance.setMinimumFrameRate(data.minimum_framerate)
        instance.setPixelAspectRatio(*data.pixel_aspect_ratio)
        instance.set_pixel_format(data.pixel_format)
        instance.setResolution(*data.resolution)
        return instance

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CameraViewfinderSettings":
        settings = Settings(**data)
        return cls.from_dataclass(settings)
