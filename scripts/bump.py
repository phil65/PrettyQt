import os
import toml
import subprocess


if __name__ == "__main__":
    output = subprocess.check_output("git stash --include-untracked")
    stashed = output != b"No local changes to save\n"
    print(output)
    os.system("cz bump --no-verify")
    dct = toml.load("pyproject.toml")
    version = dct["tool"]["poetry"]["version"]
    print(version)
    os.system(f'cz changelog --unreleased-version "v{version}"')
    os.system("cp CHANGELOG.md docs/changelog.md")
    os.system("git add --all")
    os.system("git commit --amend --no-edit --no-verify")
    os.system(f"git tag -d v{version}")
    os.system(f"git tag v{version}")
    if stashed:
        os.system("git stash apply")
