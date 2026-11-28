"""Project tasks."""

import os
import pathlib
import shutil
from typing import Literal

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
    ctx.run("uv run ty check")


@duty(capture=False)
def lint_check(ctx):
    """Lint the code."""
    ctx.run("uv run ruff check .")
    ctx.run("uv run ruff format --check .")
    ctx.run("uv run ty check")


@duty(capture=False)
def profile(ctx, *args: str):
    """Run generating the docs using pyinstrument."""
    args_str = " " + " ".join(args) if args else ""
    ctx.run(f"uv run pyinstrument mknodes/manual/root.py{args_str}")


@duty(capture=False)
def version(
    ctx,
    bump_type: Literal[
        "major", "minor", "patch", "stable", "alpha", "beta", "rc", "post", "dev"
    ] = "patch",
):
    """Release a new version with git operations. (major|minor|patch|stable|alpha|beta|rc|post|dev)."""  # noqa: E501
    # Check for uncommitted changes
    result = ctx.run("git status --porcelain", capture=True)
    if result.strip():
        msg = "Cannot release with uncommitted changes. Please commit or stash first."
        raise RuntimeError(msg)

    # Read current version
    old_version = ctx.run("uv version --short", capture=True).strip()
    print(f"Current version: {old_version}")
    ctx.run(f"uv version --bump {bump_type}")
    new_version = ctx.run("uv version --short", capture=True).strip()
    print(f"New version: {new_version}")
    ctx.run("git add pyproject.toml")
    ctx.run(f'git commit -m "chore: bump version {old_version} -> {new_version}"')

    # Create and push tag
    tag = f"v{new_version}"
    ctx.run(f"git tag {tag}")
    print(f"Created tag: {tag}")


# Project-specific: local OpenTelemetry trace/metric viewer via Aspire Dashboard.
@duty(capture=False)
def aspire(
    ctx,
    runtime: Literal["auto", "docker", "podman"] = "auto",
    port: int = 18888,
):
    """Run local .NET Aspire Dashboard (OTLP UI on :18888, gRPC :4317, HTTP :4318)."""
    if runtime == "auto":
        cmd = shutil.which("docker") or shutil.which("podman")
        if cmd is None:
            msg = "Neither 'docker' nor 'podman' found on PATH."
            raise RuntimeError(msg)
        engine = pathlib.Path(cmd).name
    else:
        engine = runtime
    print(f"Starting Aspire Dashboard via {engine}:")
    print(f"  UI:        http://localhost:{port}")
    print("  OTLP gRPC: localhost:4317")
    print("  OTLP HTTP: http://localhost:4318/v1/traces")
    ctx.run(
        f"{engine} run --rm -it"
        f" -p {port}:18888"
        " -p 4317:18889"
        " -p 4318:18890"
        " -e DOTNET_DASHBOARD_UNSECURED_ALLOW_ANONYMOUS=true"
        " -e DOTNET_DASHBOARD_OTLP_HTTP_ENDPOINT_URL=http://+:18890"
        " --name prettyqt-aspire-dashboard"
        " mcr.microsoft.com/dotnet/aspire-dashboard:latest"
    )
