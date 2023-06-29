from __future__ import annotations

import logging

from typing import Literal

from prettyqt import core, texttospeech
from prettyqt.utils import bidict


logger = logging.getLogger()

STATE = bidict(
    ready=texttospeech.QTextToSpeech.State.Ready,
    speaking=texttospeech.QTextToSpeech.State.Speaking,
    paused=texttospeech.QTextToSpeech.State.Paused,
    error=texttospeech.QTextToSpeech.State.Error,
)

StateStr = Literal["ready", "speaking", "paused", "error"]


class TextToSpeech(core.ObjectMixin, texttospeech.QTextToSpeech):
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
    app.exec()
