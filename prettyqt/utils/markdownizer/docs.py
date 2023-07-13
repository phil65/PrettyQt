from __future__ import annotations

import contextlib
import importlib
import inspect
import logging
import os
import pathlib
import types

import mkdocs_gen_files

from prettyqt.utils import classhelpers, markdownizer


logger = logging.getLogger(__name__)


class Docs(markdownizer.Nav):
    def __init__(
        self, module_name: str, exclude_modules: list[str] | None = None, **kwargs
    ):
        super().__init__(module_name=module_name, section="", **kwargs)
        self.module_name = module_name
        self.root_path = pathlib.Path(f"./{module_name}")
        self._editor = mkdocs_gen_files.editor.FilesEditor.current()
        self._docs_dir = pathlib.Path(self._editor.config["docs_dir"])
        self._exclude = exclude_modules or []

    def get_files(self):
        return self._editor.files

    def get_dependency_table(self) -> markdownizer.Table:
        return markdownizer.Table.get_dependency_table(self.module_name)

    def add_dependency_page(self, path: str | os.PathLike, **kwargs):
        page = markdownizer.Document(path=self._docs_dir / path, **kwargs)
        page += self.get_dependency_table()
        page.write()
        return page

    def create_nav(self, section: str | os.PathLike) -> markdownizer.Nav:
        nav = markdownizer.Nav(section=section, module_name=self.module_name)
        self.navs.append(nav)
        return nav

    def iter_files(self, glob: str = "*/*.py"):
        for path in sorted(self.root_path.rglob(glob)):
            if (
                all(i not in path.parts for i in self._exclude)
                and not any(i.startswith("__") for i in path.parent.parts)
                and not path.is_dir()
            ):
                yield path.relative_to(self.root_path)

    def iter_classes_for_module(
        self,
        module: types.ModuleType | str | tuple | list,
        recursive: bool = False,
        filter_by___all__: bool = False,
        _seen=None,
    ):
        mod = classhelpers.to_module(module)
        if mod is None:
            return
        if recursive:
            seen = _seen or set()
            for _submod_name, submod in inspect.getmembers(mod, inspect.ismodule):
                if submod.__name__.startswith(self.module_name) and submod not in seen:
                    seen.add(submod)
                    yield from self.iter_classes_for_module(
                        submod, recursive=True, _seen=seen
                    )
        for klass_name, klass in inspect.getmembers(mod, inspect.isclass):
            if filter_by___all__ and (
                not hasattr(mod, "__all__") or klass_name not in mod.__all__
            ):
                continue
            if klass.__module__.startswith(self.module_name):
                yield klass

    def iter_modules_for_glob(self, glob="*/*.py"):
        for path in self.iter_files(glob):
            module_path = path.with_suffix("")
            parts = tuple(module_path.parts)
            complete_module_path = f"{self.module_name}." + ".".join(parts)
            with contextlib.suppress(ImportError, AttributeError):
                yield importlib.import_module(complete_module_path)

    def iter_classes_for_glob(
        self, glob="*/*.py", recursive: bool = False, avoid_duplicates: bool = True
    ):
        """Yields (class, path) tuples."""
        seen = set()
        for path in self.iter_files(glob):
            module_path = path.with_suffix("")
            parts = tuple(self.module_name, *module_path.parts)
            module = classhelpers.to_module(parts)
            if not module:
                return
            for klass in self.iter_classes_for_module(module, recursive=recursive):
                if (klass, path) not in seen or not avoid_duplicates:
                    seen.add((klass, path))
                    yield klass, path


if __name__ == "__main__":
    doc = Docs(module_name="prettyqt")
    page = doc.get_overview_document()
