from __future__ import annotations

import logging
from typing import Literal

from prettyqt.qt import QtTextToSpeech
from prettyqt.utils import bidict


logger = logging.getLogger()
AgeStr = Literal["child", "teenager", "adult", "senior", "other"]

AGE = bidict[AgeStr, QtTextToSpeech.QVoice.Age](
    child=QtTextToSpeech.QVoice.Age.Child,
    teenager=QtTextToSpeech.QVoice.Age.Teenager,
    adult=QtTextToSpeech.QVoice.Age.Adult,
    senior=QtTextToSpeech.QVoice.Age.Senior,
    other=QtTextToSpeech.QVoice.Age.Other,
)

GenderStr = Literal["male", "female", "unknown"]

GENDER = bidict[GenderStr, QtTextToSpeech.QVoice.Gender](
    male=QtTextToSpeech.QVoice.Gender.Male,
    female=QtTextToSpeech.QVoice.Gender.Female,
    unknown=QtTextToSpeech.QVoice.Gender.Unknown,
)


class Voice(QtTextToSpeech.QVoice):
    def get_age(self) -> AgeStr:
        return AGE.inverse[self.age()]

    def get_gender(self) -> GenderStr:
        return GENDER.inverse[self.gender()]


if __name__ == "__main__":
    val = Voice()
