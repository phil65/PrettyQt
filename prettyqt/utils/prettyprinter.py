from __future__ import annotations

from collections.abc import Callable, Generator
from typing import Any


class PrettyPrinter:
    serialize: Callable

    def __pretty__(
        self, fmt: Callable[[Any], Any], **kwargs: Any
    ) -> Generator[Any, None, None]:
        """Provide a human readable representations of objects.

        Used by devtools (https://python-devtools.helpmanual.io/).
        """
        yield f"{type(self).__name__}("
        yield 1
        for k, v in self.serialize().items():
            yield f"{k}="
            if isinstance(v, list):
                for item in v:
                    if hasattr(item, "__pretty__"):
                        yield from item.__pretty__(fmt, **kwargs)
                    else:
                        yield f"{item!r}"
                    yield 0
            elif hasattr(v, "__pretty__"):
                yield from v.__pretty__(fmt, **kwargs)
            else:
                yield f"{v!r}"
            yield 0
        yield -1
        yield ")"
