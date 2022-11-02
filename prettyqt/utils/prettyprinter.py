from __future__ import annotations

from collections.abc import Generator
from typing import Any, Callable


class PrettyPrinter:
    serialize: Callable

    def __pretty__(
        self, fmt: Callable[[Any], Any], **kwargs: Any
    ) -> Generator[Any, None, None]:
        """Provide a human readable representations of objects.

        Used by devtools (https://python-devtools.helpmanual.io/).
        """
        yield type(self).__name__ + "("
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
            else:
                if hasattr(v, "__pretty__"):
                    yield from v.__pretty__(fmt, **kwargs)
                else:
                    yield f"{v!r}"
            yield 0
        yield -1
        yield ")"
