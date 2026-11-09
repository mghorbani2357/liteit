"""CLI tests for ``liteit init`` and ``liteit generate controller``."""

from __future__ import annotations

import ast
from pathlib import Path

from click.testing import CliRunner
from jinja2 import PackageLoader

from liteit.cli import main

EXPECTED_INIT_FILES = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/controllers/__init__.py",
    "app/controllers/health.py",
    "app/schemas/__init__.py",
    "app/schemas/health.py",
    "app/core/__init__.py",
    "app/core/logging.py",
    "app/core/security.py",
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_health.py",
    ".env.example",
    ".gitignore",
    "requirements.txt",
    "Dockerfile",
    "pytest.ini",
    "README.md",
]


def _assert_valid_python_tree(root: Path) -> None:
    for path in root.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        try:
            ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            raise AssertionError(f"Invalid Python in {path}: {exc}") from exc


def test_init_creates_expected_tree(runner: CliRunner, tmp_path: Path) -> None:
    project = tmp_path / "myapi"
    result = runner.invoke(main, ["init", str(project)])
    assert result.exit_code == 0, result.output
    assert "Initialized" in result.output

    for relative in EXPECTED_INIT_FILES:
        assert (project / relative).is_file(), f"missing {relative}"

    _assert_valid_python_tree(project)

    main_src = (project / "app" / "main.py").read_text(encoding="utf-8")
    assert "discover_controllers" in main_src
    assert 'path="/docs"' in main_src
    assert "SwaggerRenderPlugin" in main_src
    assert "blocking thread pool" in main_src

    dockerfile = (project / "Dockerfile").read_text(encoding="utf-8")
    assert "granian" in dockerfile.lower()
    assert "app.main:app" in dockerfile


def test_init_refuses_nonempty_directory(runner: CliRunner, tmp_path: Path) -> None:
    project = tmp_path / "existing"
    project.mkdir()
    (project / "marker.txt").write_text("nope", encoding="utf-8")
    result = runner.invoke(main, ["init", str(project)])
    assert result.exit_code != 0
    assert "not empty" in result.output.lower()


def test_generate_controller(runner: CliRunner, tmp_path: Path) -> None:
    project = tmp_path / "myapi"
    init = runner.invoke(main, ["init", str(project)])
    assert init.exit_code == 0, init.output

    result = runner.invoke(
        main,
        ["generate", "controller", "users", "--path", str(project)],
    )
    assert result.exit_code == 0, result.output
    assert "Generated" in result.output

    controller = project / "app" / "controllers" / "users.py"
    schema = project / "app" / "schemas" / "users.py"
    assert controller.is_file()
    assert schema.is_file()

    controller_src = controller.read_text(encoding="utf-8")
    schema_src = schema.read_text(encoding="utf-8")
    assert "class UsersController" in controller_src
    assert "@get" in controller_src
    assert "@post" in controller_src
    assert "@delete" in controller_src
    assert "class UsersCreateDTO" in schema_src
    assert "class UsersUpdateDTO" in schema_src
    assert "class UsersResponseDTO" in schema_src

    _assert_valid_python_tree(project)


def test_gen_alias_controller(runner: CliRunner, tmp_path: Path) -> None:
    project = tmp_path / "myapi"
    assert runner.invoke(main, ["init", str(project)]).exit_code == 0

    result = runner.invoke(
        main,
        ["gen", "controller", "order_items", "--path", str(project)],
    )
    assert result.exit_code == 0, result.output
    assert (project / "app" / "controllers" / "order_items.py").is_file()
    src = (project / "app" / "controllers" / "order_items.py").read_text(
        encoding="utf-8"
    )
    assert "class OrderItemsController" in src


def test_generate_requires_init(runner: CliRunner, tmp_path: Path) -> None:
    result = runner.invoke(
        main,
        ["generate", "controller", "users", "--path", str(tmp_path)],
    )
    assert result.exit_code != 0
    assert "liteit init" in result.output


def test_generate_refuses_overwrite(runner: CliRunner, tmp_path: Path) -> None:
    project = tmp_path / "myapi"
    assert runner.invoke(main, ["init", str(project)]).exit_code == 0
    assert (
        runner.invoke(
            main, ["generate", "controller", "users", "--path", str(project)]
        ).exit_code
        == 0
    )
    again = runner.invoke(
        main, ["generate", "controller", "users", "--path", str(project)]
    )
    assert again.exit_code != 0
    assert "already exists" in again.output.lower()


def test_generate_rejects_invalid_name(runner: CliRunner, tmp_path: Path) -> None:
    project = tmp_path / "myapi"
    assert runner.invoke(main, ["init", str(project)]).exit_code == 0
    result = runner.invoke(
        main, ["generate", "controller", "Users", "--path", str(project)]
    )
    assert result.exit_code != 0
    assert "snake_case" in result.output


def test_help_lists_commands(runner: CliRunner) -> None:
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "init" in result.output
    assert "generate" in result.output
    assert "gen" in result.output
    assert "run" in result.output


def test_version(runner: CliRunner) -> None:
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "liteit" in result.output.lower()


def test_init_writes_env_example_and_gitignore(
    runner: CliRunner, tmp_path: Path
) -> None:
    project = tmp_path / "payments"
    result = runner.invoke(main, ["init", str(project)])
    assert result.exit_code == 0, result.output

    env_example = (project / ".env.example").read_text(encoding="utf-8")
    assert "APP_NAME=payments" in env_example
    assert "TIMEZONE=" in env_example

    gitignore = (project / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore
    assert "__pycache__/" in gitignore

    requirements = (project / "requirements.txt").read_text(encoding="utf-8")
    assert "litestar" in requirements
    assert "granian" in requirements
    assert "structlog" in requirements


def test_init_allows_empty_directory(runner: CliRunner, tmp_path: Path) -> None:
    project = tmp_path / "emptyproj"
    project.mkdir()
    result = runner.invoke(main, ["init", str(project)])
    assert result.exit_code == 0, result.output
    assert (project / "app" / "main.py").is_file()


def test_generate_help(runner: CliRunner) -> None:
    result = runner.invoke(main, ["generate", "--help"])
    assert result.exit_code == 0
    assert "controller" in result.output


def test_templates_packaged() -> None:
    loader = PackageLoader("liteit", "templates")
    names = set(loader.list_templates())
    assert "project/app/main.py.j2" in names
    assert "project/env.example.j2" in names
    assert "project/gitignore" in names
    assert "controller/controller.py.j2" in names
    assert "controller/schemas.py.j2" in names
