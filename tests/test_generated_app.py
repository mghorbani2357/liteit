"""Integration smoke tests against a generated Litestar project."""

from __future__ import annotations

import ast
import importlib
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from liteit.cli import main

pytest.importorskip("litestar")
pytest.importorskip("httpx")


def _scaffold(runner: CliRunner, root: Path) -> Path:
    project = root / "myapi"
    init = runner.invoke(main, ["init", str(project)])
    assert init.exit_code == 0, init.output
    gen = runner.invoke(
        main, ["generate", "controller", "users", "--path", str(project)]
    )
    assert gen.exit_code == 0, gen.output
    return project


def test_generated_python_is_valid(runner: CliRunner, tmp_path: Path) -> None:
    project = _scaffold(runner, tmp_path)
    for path in project.rglob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


@pytest.mark.asyncio
async def test_generated_app_health_and_users(
    runner: CliRunner, tmp_path: Path
) -> None:
    from litestar.testing import AsyncTestClient

    project = _scaffold(runner, tmp_path)
    sys.path.insert(0, str(project))
    try:
        # Fresh imports for this generated tree
        for name in list(sys.modules):
            if name == "app" or name.startswith("app."):
                del sys.modules[name]

        create_app = importlib.import_module("app.main").create_app
        app = create_app()

        async with AsyncTestClient(app=app) as client:
            health = await client.get("/health")
            assert health.status_code == 200
            assert health.json() == {"status": "ok"}

            users = await client.get("/users")
            assert users.status_code == 200
            assert users.json() == []

            docs = await client.get("/docs/openapi.json")
            assert docs.status_code == 200
            payload = docs.json()
            assert "openapi" in payload or "paths" in payload
    finally:
        if str(project) in sys.path:
            sys.path.remove(str(project))
        for name in list(sys.modules):
            if name == "app" or name.startswith("app."):
                del sys.modules[name]


def test_generated_discovery_finds_controllers(
    runner: CliRunner, tmp_path: Path
) -> None:
    project = _scaffold(runner, tmp_path)
    sys.path.insert(0, str(project))
    try:
        for name in list(sys.modules):
            if name == "app" or name.startswith("app."):
                del sys.modules[name]

        discover = importlib.import_module("app.main").discover_controllers
        controllers = discover()
        names = {cls.__name__ for cls in controllers}
        assert "HealthController" in names
        assert "UsersController" in names
    finally:
        if str(project) in sys.path:
            sys.path.remove(str(project))
        for name in list(sys.modules):
            if name == "app" or name.startswith("app."):
                del sys.modules[name]
