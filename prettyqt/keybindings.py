from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from prettyqt import constants


@dataclasses.dataclass
class Command:
    keycombo: str
    description: str
    context: str
    method: Callable


_registry = dict()


def register(
    keybinding: str | Iterable[str], command: str
) -> Callable[[Callable], Callable]:
    def decorator(fn: Callable) -> Callable:
        if isinstance(keybinding, str):
            bind(keybinding, command, fn)
        else:
            for binding in keybinding:
                bind(binding, command, fn, allow_override=False)
        return fn

    return decorator


def bind(
    keybinding: str,
    command: str,
    fn: Callable,
    mode: constants.ShortcutContextStr = "application",
    allow_override: bool = True,
) -> None:
    if not allow_override and keybinding in _registry:
        msg = f"Duplicate keybinding for '{keybinding}'"
        raise ValueError(msg)
    _registry[keybinding] = (command, fn)


def unbind(keybinding: str, mode: constants.ShortcutContextStr = "application") -> None:
    """Remove keybinding from registry.

    See config/configcommands.unbind for the corresponding command.
    """
    if keybinding not in _registry:
        msg = f"No binding found for '{keybinding}'"
        raise KeyError(msg)
    del _registry[keybinding]
