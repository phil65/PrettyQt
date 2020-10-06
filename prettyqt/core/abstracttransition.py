# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


TRANSITION_TYPES = bidict(
    exclusive=QtCore.QAbstractTransition.ExternalTransition,
    parallel=QtCore.QAbstractTransition.InternalTransition,
)


QtCore.QAbstractTransition.__bases__ = (core.Object,)


class AbstractTransition(QtCore.QAbstractTransition):
    def set_transition_type(self, typ: str):
        """Set transition type.

        Allowed values are "exclusive", "parallel"

        Args:
            typ: transition type to use

        Raises:
            InvalidParamError: transition type does not exist
        """
        if typ not in TRANSITION_TYPES:
            raise InvalidParamError(typ, TRANSITION_TYPES)
        self.setTransitionType(TRANSITION_TYPES[typ])

    def get_transition_type(self) -> str:
        """Return current transition type.

        Possible values: "exclusive", "parallel"

        Returns:
            transition type
        """
        return TRANSITION_TYPES.inv[self.transitionType()]
