"""Tests for ``liteit run`` Granian wrapper."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from liteit.cli import main


def test_run_requires_project(runner: CliRunner, tmp_path: Path) -> None:
    result = runner.invoke(main, ["run", "--path", str(tmp_path)])
    assert result.exit_code != 0
    assert "app/main.py" in result.output


def test_run_invokes_granian(runner: CliRunner, tmp_path: Path) -> None:
    project = tmp_path / "myapi"
    assert runner.invoke(main, ["init", str(project)]).exit_code == 0

    with patch("liteit.cli.subprocess.call", return_value=0) as call:
        result = runner.invoke(
            main,
            [
                "run",
                "--path",
                str(project),
                "--host",
                "0.0.0.0",
                "--port",
                "9000",
                "--workers",
                "2",
                "--reload",
            ],
        )

    assert result.exit_code == 0, result.output
    assert call.call_count == 1
    cmd = call.call_args.args[0]
    assert "-m" in cmd and "granian" in cmd
    assert cmd[cmd.index("-m") + 1] == "granian"
    assert "--interface" in cmd and "asgi" in cmd
    assert "app.main:app" in cmd
    assert "--host" in cmd and "0.0.0.0" in cmd
    assert "--port" in cmd and "9000" in cmd
    assert "--workers" in cmd and "2" in cmd
    assert "--runtime-threads" in cmd and "1" in cmd
    assert "--blocking-threads" in cmd and "4" in cmd
    assert "--reload" in cmd
    assert call.call_args.kwargs["cwd"] == project.resolve()


def test_run_help(runner: CliRunner) -> None:
    result = runner.invoke(main, ["run", "--help"])
    assert result.exit_code == 0
    assert "--host" in result.output
    assert "--port" in result.output
    assert "--reload" in result.output
    assert "--workers" in result.output
