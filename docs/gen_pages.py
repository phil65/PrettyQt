# """Generate the code reference pages and navigation."""

# from __future__ import annotations

# from pathlib import Path

# import mkdocs_gen_files

# nav = mkdocs_gen_files.Nav()
# for path in sorted(Path("./prettyqt").rglob("*/*.py")):
#     if "__pyinstaller" in str(path):
#         continue
#     if path.is_dir():
#         continue
#     module_path = path.relative_to("./prettyqt").with_suffix("")
#     doc_path = path.relative_to("./prettyqt").with_suffix(".md")
#     full_doc_path = Path("reference", doc_path)
#     print(module_path, doc_path, full_doc_path)
#     parts = tuple(module_path.parts)

#     if parts[-1] == "__init__":
#         continue
#         parts = parts[:-1]
#         doc_path = doc_path.with_name("index.md")
#         full_doc_path = full_doc_path.with_name("index.md")
#     elif parts[-1] == "__main__":
#         continue
#     print(parts)
#     nav[parts] = doc_path.as_posix()

#     with mkdocs_gen_files.open(full_doc_path, "w") as fd:
#         ident = ".".join(parts)
#         fd.write(f"::: prettyqt.{ident}")

#     mkdocs_gen_files.set_edit_path(full_doc_path, path)

# with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
#     nav_file.writelines(nav.build_literate_nav())
