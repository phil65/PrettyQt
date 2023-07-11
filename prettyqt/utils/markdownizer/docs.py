from __future__ import annotations

import contextlib
import importlib
import inspect
import logging
import os
import pathlib
import types

from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class Docs:
    def __init__(self, module_name: str, exclude_modules: list[str] | None = None):
        self.module_name = module_name
        self.root_path = pathlib.Path(f"./{module_name}")
        self._exclude = exclude_modules or []
        self.navs = []

    def write(self, document):
        pass

    def create_nav(self, path: str | os.PathLike):
        nav = markdownizer.LiterateNav(path=path)
        self.navs.append(nav)
        return nav

    def yield_files(self, glob: str = "*/*.py"):
        for path in sorted(self.root_path.rglob(glob)):
            if (
                all(i not in path.parts for i in self._exclude)
                and not any(i.startswith("__") for i in path.parent.parts)
                and not path.is_dir()
            ):
                yield path.relative_to(self.root_path)

    def yield_klasses_for_module(
        self,
        mod: types.ModuleType,
        recursive: bool = False,
        filter_by___all__: bool = False,
        _seen=None,
    ):
        if recursive:
            seen = _seen or set()
            for _submod_name, submod in inspect.getmembers(mod, inspect.ismodule):
                if submod.__name__.startswith(self.module_name) and submod not in seen:
                    seen.add(submod)
                    yield from self.yield_klasses_for_module(
                        submod, recursive=True, _seen=seen
                    )
        for klass_name, klass in inspect.getmembers(mod, inspect.isclass):
            if filter_by___all__ and (
                not hasattr(mod, "__all__") or klass_name not in mod.__all__
            ):
                continue
            if klass.__module__.startswith(self.module_name):
                yield klass

    def yield_modules_for_glob(self, glob="*/*.py"):
        for path in self.yield_files(glob):
            module_path = path.with_suffix("")
            parts = tuple(module_path.parts)
            complete_module_path = "prettyqt." + ".".join(parts)
            with contextlib.suppress(ImportError):
                yield importlib.import_module(complete_module_path)

    def yield_classes_for_glob(
        self, glob="*/*.py", recursive: bool = False, avoid_duplicates: bool = True
    ):
        seen = set()
        for path in self.yield_files(glob):
            module_path = path.with_suffix("")
            parts = tuple(module_path.parts)
            module_path = f"{self.module_name}." + ".".join(parts)
            try:
                module = importlib.import_module(module_path)
            except (ImportError, AttributeError):  # noqa: PERF203
                continue
            else:
                for klass in self.yield_klasses_for_module(module, recursive=recursive):
                    if (klass, path) not in seen or not avoid_duplicates:
                        seen.add((klass, path))
                        yield klass, path


if __name__ == "__main__":
    doc = Docs(module_name="prettyqt")
    print(list(doc.yield_files()))
