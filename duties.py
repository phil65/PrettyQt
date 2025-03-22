from __future__ import annotations

import os

from duty import duty


@duty(capture=False)
def build(ctx, *args: str):
    """Build a MkNodes page."""
    args_str = " " + " ".join(args) if args else ""
    ctx.run(f"uv run mknodes build{args_str}")


@duty(capture=False)
def serve(ctx, *args: str):
    """Serve a MkNodes page."""
    args_str = " " + " ".join(args) if args else ""
    ctx.run(f"uv run mknodes serve{args_str}")


@duty(capture=False)
def test(ctx, *args: str):
    """Serve a MkNodes page."""
    test_pyqt6(ctx, *args)
    test_pyside6(ctx, *args)


@duty(capture=False)
def test_pyside6(ctx, *args: str):
    """Serve a MkNodes page."""
    os.environ["QT_API"] = "pyside6"
    args = ("--cov-report=xml", *args)
    args_str = " " + " ".join(args)
    ctx.run(f"uv run pytest{args_str}")


@duty(capture=False)
def test_pyqt6(ctx, *args: str):
    """Serve a MkNodes page."""
    os.environ["QT_API"] = "pyqt6"
    args = ("--cov-report=xml", *args)
    args_str = " " + " ".join(args)
    ctx.run(f"uv run pytest{args_str}")


@duty(capture=False)
def clean(ctx):
    """Clean all files from the Git directory except checked-in files."""
    ctx.run("git clean -dfX")


@duty(capture=False)
def update(ctx):
    """Update all environment packages using pip directly."""
    ctx.run("uv lock --upgrade")
    ctx.run("uv sync --all-extras")


@duty(capture=False)
def lint(ctx):
    """Lint and fix the code."""
    ctx.run("uv run ruff check --fix .")
    ctx.run("uv run ruff format .")
    ctx.run("uv run mypy prettyqt/")


@duty(capture=False)
def lint_check(ctx):
    """Lint the code."""
    ctx.run("uv run ruff check .")
    ctx.run("uv run ruff format --check .")
    ctx.run("uv run mypy prettyqt/")


@duty(capture=False)
def profile(ctx, *args: str):
    """Run generating the docs using pyinstrument."""
    args_str = " " + " ".join(args) if args else ""
    ctx.run(f"uv run pyinstrument mknodes/manual/root.py{args_str}")


@duty(capture=False)
def version(ctx, *args: str):
    """Bump package version."""
    args_str = " " + " ".join(args) if args else ""
    ctx.run(f"hatch version{args_str}")
