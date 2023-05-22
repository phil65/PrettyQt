"""eventfilters module.

Contains custom EventFilter classes
"""

from .baseeventfilter import BaseEventFilter
from .hovericoneventfilter import HoverIconEventFilter
from .animatedtooltipeventfilter import AnimatedToolTipEventFilter
from .eventcatcher import EventCatcher


__all__ = [
    "BaseEventFilter",
    "HoverIconEventFilter",
    "AnimatedToolTipEventFilter",
    "EventCatcher",
]
