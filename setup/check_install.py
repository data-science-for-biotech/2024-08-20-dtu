#!/usr/bin/env python3

import importlib
import shutil
import subprocess
import sys


class DependencyNotFoundError(RuntimeError):
    def __init__(self, name: str) -> None:
        self.name = name


def test_executable(program: str) -> None:
    path = shutil.which(program)
    if path is None:
        raise DependencyNotFoundError(program)

    if program == "unzip":
        # unzip wants -v instead of --version
        out = subprocess.check_output([path, "-v"], encoding="utf-8").split("\n")[0]
    else:
        out = subprocess.check_output([path, "--version"], encoding="utf-8").split(
            "\n"
        )[0]
    print(f"{program} found: {out}")


def test_lib(name: str) -> None:
    _ = importlib.import_module(name)
    print(f"{name} found.")


EXECUTABLES = [
    "bash",
    "git",
    "python3",
    "unzip",
]

MODULES = [
    "numpy",
    "pandas",
    "sklearn",
    "matplotlib",
    "altair",
    "odf",
    "openpyxl",
    "seaborn",
    "skbio",
    "skbio.diversity",
    "umap",
]


def main():
    errors = False
    for exe in EXECUTABLES:
        try:
            test_executable(exe)
        except DependencyNotFoundError as err:
            print(f"{err.name} not found, check your installation.")
            errors = True

    for mod in MODULES:
        try:
            test_lib(mod)
        except ModuleNotFoundError:
            print(f"{mod} not found, check your installation.")
            errors = True

    if errors:
        print("Failed to find all dependencies, please check the output above!")
        sys.exit(1)

    print("All dependencies installed!")
    sys.exit(0)


if __name__ == "__main__":
    main()
