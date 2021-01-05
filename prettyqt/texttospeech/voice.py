from __future__ import annotations

import logging
from typing import Literal

from prettyqt.qt import QtTextToSpeech
from prettyqt.utils import bidict


logger = logging.getLogger()

AGE = bidict(
    child=QtTextToSpeech.QVoice.Child,
    teenager=QtTextToSpeech.QVoice.Teenager,
    adult=QtTextToSpeech.QVoice.Adult,
    senior=QtTextToSpeech.QVoice.Senior,
    other=QtTextToSpeech.QVoice.Other,
)

AgeStr = Literal["child", "teenager", "adult", "senior", "other"]

GENDER = bidict(
    male=QtTextToSpeech.QVoice.Male,
    female=QtTextToSpeech.QVoice.Female,
    unknown=QtTextToSpeech.QVoice.Unknown,
)

GenderStr = Literal["male", "female", "unknown"]


class Voice(QtTextToSpeech.QVoice):
    def get_age(self) -> AgeStr:
        return AGE.inverse[self.age()]

    def get_gender(self) -> GenderStr:
        return GENDER.inverse[self.gender()]


if __name__ == "__main__":
    val = Voice()
