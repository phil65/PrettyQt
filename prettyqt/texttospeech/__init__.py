"""TextToSpeech module.

Contains QtTextToSpeech-based classes
"""

from prettyqt.qt.QtTextToSpeech import *  # noqa: F403

from .voice import Voice
from .texttospeech import TextToSpeech

__all__ = [
    "Voice",
    "TextToSpeech",
]
