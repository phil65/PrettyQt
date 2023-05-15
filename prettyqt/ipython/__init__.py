"""ipython module.

contains IPython-based classes
"""

from .baseipythonwidget import BaseIPythonWidget
from .inprocessipythonwidget import InProcessIPythonWidget
from .outofprocessipythonwidget import OutOfProcessIPythonWidget


__all__ = ["InProcessIPythonWidget", "OutOfProcessIPythonWidget", "BaseIPythonWidget"]
