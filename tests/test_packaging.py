"""Packaging checks: wheel contains templates needed by the CLI."""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def wheel_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    dist = tmp_path_factory.mktemp("dist")
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.fail(
            f"python -m build failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    wheels = list(dist.glob("liteit-*.whl"))
    assert wheels, "no wheel produced"
    return wheels[0]


def test_wheel_contains_templates(wheel_path: Path) -> None:
    with zipfile.ZipFile(wheel_path) as zf:
        names = set(zf.namelist())

    required = [
        "liteit/templates/project/app/main.py.j2",
        "liteit/templates/project/env.example.j2",
        "liteit/templates/project/gitignore",
        "liteit/templates/project/Dockerfile",
        "liteit/templates/controller/controller.py.j2",
        "liteit/templates/controller/schemas.py.j2",
    ]
    missing = [path for path in required if path not in names]
    assert not missing, f"Wheel missing template files: {missing}"
