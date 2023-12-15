from __future__ import annotations

import logging
import re


_MAXCACHE = 20

logger = logging.getLogger(__name__)


class BaseResolver:
    _match_cache = {}

    def __init__(self, ignore_case: bool = False):
        """Base resolver. Subclass to get glob functionality.

        Keyword Args:
            name (str): Name of the node attribute to be used for resolving
            ignore_case (bool): Enable case insensisitve handling.
        """
        super().__init__()
        self.ignore_case = ignore_case

    def get_parent(self, node):
        return NotImplemented

    def get_children(self, node):
        return NotImplemented

    def get_attribute(self, node):
        return NotImplemented

    def get_root(self, node):
        prev = node
        while node:
            node = self.get_parent(node)
            prev = node
        return prev

    def get_separator(self, node) -> str:
        return "/"

    def get(self, path: str, root_node):
        """Return instance at `path`.

        An example module tree:

        >>> top = Node("top", parent=None)
        >>> sub0 = Node("sub0", parent=top)
        >>> sub0sub0 = Node("sub0sub0", parent=sub0)
        >>> sub0sub1 = Node("sub0sub1", parent=sub0)
        >>> sub1 = Node("sub1", parent=top)

        A resolver using the `name` attribute:

        >>> r = Resolver("name")

        Relative paths:

        >>> r.get(top, "sub0/sub0sub0")
        Node('/top/sub0/sub0sub0')
        >>> r.get(sub1, "..")
        Node('/top')
        >>> r.get(sub1, "../sub0/sub0sub1")
        Node('/top/sub0/sub0sub1')
        >>> r.get(sub1, ".")
        Node('/top/sub1')
        >>> r.get(sub1, "")
        Node('/top/sub1')
        >>> r.get(top, "sub2")
        Traceback (most recent call last):
          ...
        ChildResolverError: Node('/top') has no child sub2.
        Children are: 'sub0', 'sub1'.

        Absolute paths:

        >>> r.get(sub0sub0, "/top")
        Node('/top')
        >>> r.get(sub0sub0, "/top/sub0")
        Node('/top/sub0')
        >>> r.get(sub0sub0, "/")
        Traceback (most recent call last):
          ...
        ResolverError: root node missing. root is '/top'.
        >>> r.get(sub0sub0, "/bar")
        Traceback (most recent call last):
          ...
        ResolverError: unknown root node '/bar'. root is '/top'.

        Going above the root node raises a :any:`RootResolverError`:

        >>> r.get(top, "..")
        Traceback (most recent call last):
            ...
        RootResolverError: Cannot go above root node Node('/top')

        .. note:: Please not that :any:`get()` returned `None` in exactly that case above,
                  which was a bug until version 1.8.1.

        Case insensitive matching:

        >>> r.get(top, "/TOP")
        Traceback (most recent call last):
            ...
        ResolverError: unknown root node '/TOP'. root is '/top'.

        >>> r = Resolver("name", ignore_case=True)
        >>> r.get(top, "/TOp")
        Node('/top')
        """
        node, parts = self.__start(root_node, path, self.__cmp)
        for part in parts:
            if part == "..":
                parent = self.get_parent(node)
                if parent is None:
                    raise RootResolverError(node)
                node = parent
            elif part not in ("", "."):
                node = self.__get(node, part)
        return node

    def __get(self, node, name):
        for child in self.get_children(node):
            if self.__cmp(self.get_attribute(child), str(name)):
                return child
        names = [repr(self.get_attribute(c)) for c in self.get_children(node)]
        raise ChildResolverError(node, name, names)

    def glob(self, path: str, root_node):
        """Return instances at `path` supporting wildcards.

        Behaves identical to :any:`get`, but accepts wildcards and returns
        a list of found nodes.

        * `*` matches any characters, except '/'.
        * `?` matches a single character, except '/'.

        An example module tree:

        >>> top = Node("top", parent=None)
        >>> sub0 = Node("sub0", parent=top)
        >>> sub0sub0 = Node("sub0", parent=sub0)
        >>> sub0sub1 = Node("sub1", parent=sub0)
        >>> sub1 = Node("sub1", parent=top)
        >>> sub1sub0 = Node("sub0", parent=sub1)

        A resolver using the `name` attribute:

        >>> r = Resolver("name")

        Relative paths:

        >>> r.glob(top, "sub0/sub?")
        [Node('/top/sub0/sub0'), Node('/top/sub0/sub1')]
        >>> r.glob(sub1, ".././*")
        [Node('/top/sub0'), Node('/top/sub1')]
        >>> r.glob(top, "*/*")
        [Node('/top/sub0/sub0'), Node('/top/sub0/sub1'), Node('/top/sub1/sub0')]
        >>> r.glob(top, "*/sub0")
        [Node('/top/sub0/sub0'), Node('/top/sub1/sub0')]
        >>> r.glob(top, "sub1/sub1")
        Traceback (most recent call last):
            ...
        ChildResolverError: Node('/top/sub1') has no child sub1.
        Children are: 'sub0'.

        Non-matching wildcards are no error:

        >>> r.glob(top, "bar*")
        []
        >>> r.glob(top, "sub2")
        Traceback (most recent call last):
          ...
        ChildResolverError: Node('/top') has no child sub2.
        Children are: 'sub0', 'sub1'.

        Absolute paths:

        >>> r.glob(sub0sub0, "/top/*")
        [Node('/top/sub0'), Node('/top/sub1')]
        >>> r.glob(sub0sub0, "/")
        Traceback (most recent call last):
          ...
        ResolverError: root node missing. root is '/top'.
        >>> r.glob(sub0sub0, "/bar")
        Traceback (most recent call last):
          ...
        ResolverError: unknown root node '/bar'. root is '/top'.

        Going above the root node raises a :any:`RootResolverError`:

        >>> r.glob(top, "..")
        Traceback (most recent call last):
            ...
        RootResolverError: Cannot go above root node Node('/top')
        """
        node, parts = self.__start(root_node, path, self.__match)
        return self.__glob(node, parts)

    def __start(self, node, path: str, cmp_):
        sep = self.get_separator(node)
        parts = path.split(sep)
        # resolve root
        if path.startswith(sep):
            node = self.get_root(node)
            rootpart = self.get_attribute(node)
            parts.pop(0)
            if not parts[0]:
                msg = f"root node missing. root is '{sep}{rootpart}'."
                raise ResolverError(node, "", msg)
            if not cmp_(rootpart, parts[0]):
                msg = f"unknown root node '{sep}{parts[0]}'. root is '{sep}{rootpart}'."
                raise ResolverError(node, "", msg)
            parts.pop(0)
        return node, parts

    def __glob(self, node, parts):
        assert node is not None
        nodes = []
        if parts:
            name = parts[0]
            remainder = parts[1:]
            # handle relative
            if name == "..":
                parent = self.get_parent(node)
                if parent is None:
                    raise RootResolverError(node)
                else:
                    nodes += self.__glob(parent, remainder)
            elif name in ("", "."):
                nodes += self.__glob(node, remainder)
            elif matches := self.__find(node, name, remainder):
                nodes += matches
            elif self.is_wildcard(name):
                nodes += matches
            else:
                names = [repr(self.get_attribute(c)) for c in self.get_children(node)]
                raise ChildResolverError(node, name, names)
        else:
            nodes = [node]
        return nodes

    def __find(self, node, pat, remainder):
        matches = []
        for child in self.get_children(node):
            name = self.get_attribute(child)
            try:
                if self.__match(name, pat):
                    if remainder:
                        matches += self.__glob(child, remainder)
                    else:
                        matches.append(child)
            except ResolverError as exc:
                if not self.is_wildcard(pat):
                    raise exc
        return matches

    @staticmethod
    def is_wildcard(path: str) -> bool:
        """Return `True` is a wildcard."""
        return "?" in path or "*" in path

    def __match(self, name, pat):
        k = (pat, self.ignore_case)
        try:
            re_pat = self._match_cache[k]
        except KeyError:
            res = self.__translate(pat)
            if len(self._match_cache) >= _MAXCACHE:
                self._match_cache.clear()
            flags = 0
            if self.ignore_case:
                flags |= re.IGNORECASE
            self._match_cache[k] = re_pat = re.compile(res, flags=flags)
        return re_pat.match(name) is not None

    def __cmp(self, name, pat):
        return name.upper() == pat.upper() if self.ignore_case else name == pat

    @staticmethod
    def __translate(pat):
        re_pat = ""
        for char in pat:
            if char == "*":
                re_pat += ".*"
            elif char == "?":
                re_pat += "."
            else:
                re_pat += re.escape(char)
        return f"(?ms){re_pat}" + r"\Z"


class ResolverError(RuntimeError):
    def __init__(self, node, child, msg):
        """Resolve Error at `node` handling `child`."""
        super().__init__(msg)
        self.node = node
        self.child = child


class RootResolverError(ResolverError):
    def __init__(self, root):
        """Root Resolve Error, cannot go above root node."""
        msg = f"Cannot go above root node {root!r}"
        super().__init__(root, None, msg)


class ChildResolverError(ResolverError):
    def __init__(self, node, child, names):
        """Child Resolve Error at `node` handling `child`."""
        msg = "{!r} has no child {}. Children are: {}.".format(
            node, child, ", ".join(names)
        )
        super().__init__(node, child, msg)


if __name__ == "__main__":
    from prettyqt import core, itemmodels, widgets

    app = widgets.app()
    model = itemmodels.ParentClassTreeModel(core.AbstractAnimation)
    widget = widgets.TreeView()
    widget.set_model(model)
    resolver = itemmodels.ItemModelResolver(model)
    print("here")
    # widget.show()
    # app.exec()
    test = resolver.glob("/")
    print(test)
