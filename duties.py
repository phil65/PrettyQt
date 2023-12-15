from __future__ import annotations

import os

from duty import duty


ENV_PREFIX = "poetry run "


@duty(capture=False)
def build(ctx, *args: str):
    """Build a MkNodes page."""
    args_str = " " + " ".join(args) if args else ""
    ctx.run(f"{ENV_PREFIX}mknodes build{args_str}")


@duty(capture=False)
def serve(ctx, *args: str):
    """Serve a MkNodes page."""
    args_str = " " + " ".join(args) if args else ""
    ctx.run(f"{ENV_PREFIX}mknodes serve{args_str}")


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
    ctx.run(f"{ENV_PREFIX}pytest{args_str}")


@duty(capture=False)
def test_pyqt6(ctx, *args: str):
    """Serve a MkNodes page."""
    os.environ["QT_API"] = "pyqt6"
    args = ("--cov-report=xml", *args)
    args_str = " " + " ".join(args)
    ctx.run(f"{ENV_PREFIX}pytest{args_str}")


@duty(capture=False)
def clean(ctx):
    """Clean all files from the Git directory except checked-in files."""
    ctx.run("git clean -dfX")


@duty(capture=False)
def update(ctx, *args: str):
    """Update all environment packages using pip directly."""
    ctx.run("poetry update")
    ctx.run("poetry install --all-extras")


@duty(capture=False)
def lint(ctx):
    """Update all environment packages using pip directly."""
    ctx.run(f"{ENV_PREFIX}lint")


@duty(capture=False)
def lint_check(ctx):
    """Update all environment packages using pip directly."""
    ctx.run(f"{ENV_PREFIX}lint-check")


@duty(capture=False)
def profile(ctx, *args: str):
    """Run generating the docs using pyinstrument."""
    args_str = " " + " ".join(args) if args else ""
    ctx.run(f"{ENV_PREFIX}pyinstrument mknodes/manual/root.py{args_str}")


@duty(capture=False)
def version(ctx, *args: str):
    """Bump package version."""
    args_str = " " + " ".join(args) if args else ""
    ctx.run(f"hatch version{args_str}")


@duty(capture=False)
def bump(ctx):
    """Bump package version."""
    ctx.run("poetry run cz bump --no-verify")
