from __future__ import annotations

import importlib
import logging
import os
import types

from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class DocStrings(markdownizer.Text):
    def __init__(
        self, obj: types.ModuleType | str | os.PathLike | type, header: str = "", **kwargs
    ):
        """Docstring section.

        Possible keyword arguments:

        allow_inspection (bool): Whether to allow inspecting modules when visiting
                                  them is not possible. Default: True.
        show_bases (bool): Show the base classes of a class. Default: True.
        show_source (bool): Show the source code of this object. Default: True.
        preload_modules (list[str] | None): Pre-load modules

        The modules must be listed as an array of strings. Default: None.

        Headings options:

        heading_level (int): The initial heading level to use. Default: 2.
        show_root_heading (bool): Show the heading of the object at the root of the
                                  documentation tree (i.e. the object referenced by
                                  the identifier after :::). Default: False.
        show_root_toc_entry (bool): If the root heading is not shown, at least
                                    add a ToC entry for it. Default: True.
        show_root_full_path (bool): Show the full Python path for the root
                                    object heading. Default: True.
        show_root_members_full_path (bool): Show the full Python path of the
                                            root members. Default: False.
        show_object_full_path (bool): Show the full Python path of every object.
                                      Default: False.
        show_category_heading (bool): When grouped by categories, show a heading
                                      for each category. Default: False.
        show_symbol_type_heading (bool): Show the symbol type in headings (e.g. mod,
                                         class, func and attr). Default: False.
        show_symbol_type_toc (bool): Show the symbol type in the Table of
                                     Contents (e.g. mod, class, func and attr).
                                     Default: False.
        Members options:

        members (list[str] | False | None): An explicit list of members to render.
                                            Default: None.
        members_order (str): The members ordering to use.
                             Options: alphabetical - order by the members names,
                             source - order members as they appear in the
                             source file. Default: "alphabetical".
        filters (list[str] | None): A list of filters applied to filter objects
                                    based on their name. A filter starting with !
                                    will exclude matching objects instead of
                                    including them. The members option takes
                                    precedence over filters (filters will still be
                                    applied recursively to lower members in the
                                    hierarchy). Default: ["!^_[^_]"].
        group_by_category (bool): Group the object's children by categories:
                                  attributes, classes, functions, and modules.
                                  Default: True.
        show_submodules (bool): When rendering a module, show its submodules
                                recursively. Default: False.
        DocStrings options:

        docstring_style (str): The docstring style to use: google, numpy, sphinx,
                               or None. Default: "google".
        docstring_options (dict): The options for the docstring parser. See
                                  parsers under griffe.docstrings.
        docstring_section_style (str): The style used to render docstring sections.
                                       Options: table, list, spacy. Default: "table".
        merge_init_into_class (bool): Whether to merge the __init__ method into
                                      the class' signature and docstring.
                                      Default: False.
        show_if_no_docstring (bool): Show the object heading even if it has no
                                     docstring or children with docstrings.
                                     Default: False.
        show_docstring_attributes (bool): Whether to display the "Attributes"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_description (bool): Whether to display the textual block
                                           (including admonitions) in the object's
                                           docstring. Default: True.
        show_docstring_examples (bool): Whether to display the "Examples"
                                        section in the object's docstring.
                                        Default: True.
        show_docstring_other_parameters (bool): Whether to display the
                                                "Other Parameters" section in the
                                                object's docstring. Default: True.
        show_docstring_parameters (bool): Whether to display the "Parameters"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_raises (bool): Whether to display the "Raises"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_receives (bool): Whether to display the "Receives"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_returns (bool): Whether to display the "Returns"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_warns (bool): Whether to display the "Warns"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_yields (bool): Whether to display the "Yields"
                                          section in the object's docstring.
                                          Default: True.
        Signatures/annotations options:

        annotations_path (str): The verbosity for annotations path: brief
                                (recommended), or source (as written in the source).
                                Default: "brief".
        line_length (int): Maximum line length when formatting code/signatures.
                           Default: 60.
        show_signature (bool): Show methods and functions signatures. Default: True.
        show_signature_annotations (bool): Show the type annotations in methods
                                           and functions signatures. Default: False.
        signature_crossrefs (bool): Whether to render cross-references for type
                                    annotations in signatures. Default: False.
        separate_signature (bool): Whether to put the whole signature in a code
                                  block below the heading. If Black is installed,
                                  the signature is also formatted using it.
                                  Default: False.
        """
        super().__init__(header=header)
        match obj:
            case types.ModuleType():
                self.module_path = obj.__name__
            case type():
                self.module_path = f"{obj.__module__}.{obj.__qualname__}"
            case str():
                self.module_path = obj
            case os.PathLike():
                mod = importlib.import_module(os.fspath(obj))
                self.module_path = mod.__name__
        self.options = kwargs

    def _to_markdown(self) -> str:
        md = f"::: {self.module_path}\n"
        if self.options:
            lines = [f"    {k} : {v}" for k, v in self.options]
            md = md + "\n" + "\n".join(lines)
        return f"{md}\n"
