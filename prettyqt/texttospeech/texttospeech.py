from __future__ import annotations

import logging
from typing import Literal

from prettyqt import core, texttospeech
from prettyqt.qt import QtTextToSpeech
from prettyqt.utils import bidict


logger = logging.getLogger()

STATE = bidict(
    ready=QtTextToSpeech.QTextToSpeech.State.Ready,
    speaking=QtTextToSpeech.QTextToSpeech.State.Speaking,
    paused=QtTextToSpeech.QTextToSpeech.State.Paused,
    error=QtTextToSpeech.QTextToSpeech.State.Error,
)

StateStr = Literal["ready", "speaking", "paused", "error"]


class TextToSpeech(core.ObjectMixin, QtTextToSpeech.QTextToSpeech):
    def get_state(self) -> StateStr:
        return STATE.inverse[self.state()]

    def get_locale(self) -> core.Locale:
        return core.Locale(self.locale())

    def get_available_locales(self) -> list[core.Locale]:
        return [core.Locale(locale) for locale in self.availableLocales()]

    def get_voice(self) -> texttospeech.Voice:
        return texttospeech.Voice(self.voice())

    def get_available_voices(self) -> list[texttospeech.Voice]:
        return [texttospeech.Voice(voice) for voice in self.availableVoices()]


if __name__ == "__main__":
    app = core.app()
    print(TextToSpeech.availableEngines())
    val = TextToSpeech("sapi")
    print(val.get_available_voices())
    val.say("Test")
    app.main_loop()
