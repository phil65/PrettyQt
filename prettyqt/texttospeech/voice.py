import logging

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtTextToSpeech  # type: ignore
elif PYSIDE2:
    from PySide2 import QtTextToSpeech

from prettyqt.utils import bidict


logger = logging.getLogger()

AGE = bidict(
    child=QtTextToSpeech.QVoice.Child,
    teenager=QtTextToSpeech.QVoice.Teenager,
    adult=QtTextToSpeech.QVoice.Adult,
    senior=QtTextToSpeech.QVoice.Senior,
    other=QtTextToSpeech.QVoice.Other,
)

GENDER = bidict(
    male=QtTextToSpeech.QVoice.Male,
    female=QtTextToSpeech.QVoice.Female,
    unknown=QtTextToSpeech.QVoice.Unknown,
)


class Voice(QtTextToSpeech.QVoice):
    def get_age(self) -> str:
        return AGE.inverse[self.age()]

    def get_gender(self) -> str:
        return GENDER.inverse[self.gender()]


if __name__ == "__main__":
    val = Voice()
