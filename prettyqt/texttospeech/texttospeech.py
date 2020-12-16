import logging
from typing import List

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtTextToSpeech  # type: ignore
elif PYSIDE2:
    from PySide2 import QtTextToSpeech

from prettyqt import core, texttospeech
from prettyqt.utils import bidict


logger = logging.getLogger()

STATE = bidict(
    ready=QtTextToSpeech.QTextToSpeech.Ready,
    speaking=QtTextToSpeech.QTextToSpeech.Speaking,
    paused=QtTextToSpeech.QTextToSpeech.Paused,
    backend_error=QtTextToSpeech.QTextToSpeech.BackendError,
)


QtTextToSpeech.QTextToSpeech.__bases__ = (core.Object,)


class TextToSpeech(QtTextToSpeech.QTextToSpeech):
    def get_state(self) -> str:
        return STATE.inverse[self.state()]

    def get_locale(self) -> core.Locale:
        return core.Locale(self.locale())

    def get_available_locales(self) -> List[core.Locale]:
        return [core.Locale(locale) for locale in self.availableLocales()]

    def get_voice(self) -> texttospeech.Voice:
        return texttospeech.Voice(self.voice())

    def get_available_voices(self) -> List[texttospeech.Voice]:
        return [texttospeech.Voice(voice) for voice in self.availableVoices()]


if __name__ == "__main__":
    app = core.app()
    print(TextToSpeech.availableEngines())
    val = TextToSpeech("sapi")
    print(val.get_available_voices())
    val.say("Test")
    app.main_loop()
