"""eventfilters module.

Contains custom EventFilter classes
"""

from .hovericoneventfilter import HoverIconEventFilter
from .animatedtooltipeventfilter import AnimatedToolTipEventFilter
from .eventcatcher import EventCatcher


__all__ = ["HoverIconEventFilter", "AnimatedToolTipEventFilter", "EventCatcher"]
