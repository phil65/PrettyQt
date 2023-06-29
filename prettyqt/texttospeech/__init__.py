"""TextToSpeech module.

Contains QtTextToSpeech-based classes
"""

from prettyqt.qt.QtTextToSpeech import *  # noqa: F403

from .texttospeech import TextToSpeech
from .voice import Voice


__all__ = [
    "Voice",
    "TextToSpeech",
]
