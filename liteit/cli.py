"""liteit command-line interface."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from importlib import resources
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound
from jinja2 import select_autoescape
from rich.console import Console
from rich.panel import Panel

MODULE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")

TEMPLATE_ALIASES = {
    "project/.env.example.j2": "project/env.example.j2",
    "project/.gitignore": "project/gitignore",
}

console = Console(stderr=False)

# Relative destination path -> template path under templates/
PROJECT_FILES: dict[str, str] = {
    "app/__init__.py": "project/app/__init__.py.j2",
    "app/main.py": "project/app/main.py.j2",
    "app/config.py": "project/app/config.py.j2",
    "app/controllers/__init__.py": "project/app/controllers/__init__.py.j2",
    "app/controllers/health.py": "project/app/controllers/health.py.j2",
    "app/schemas/__init__.py": "project/app/schemas/__init__.py.j2",
    "app/schemas/health.py": "project/app/schemas/health.py.j2",
    "app/core/__init__.py": "project/app/core/__init__.py.j2",
    "app/core/logging.py": "project/app/core/logging.py.j2",
    "app/core/security.py": "project/app/core/security.py.j2",
    "tests/__init__.py": "project/tests/__init__.py.j2",
    "tests/conftest.py": "project/tests/conftest.py.j2",
    "tests/test_health.py": "project/tests/test_health.py.j2",
    ".env.example": "project/env.example.j2",
    "requirements.txt": "project/requirements.txt.j2",
    "README.md": "project/README.md.j2",
}

PROJECT_STATIC_FILES: dict[str, str] = {
    ".gitignore": "gitignore",
    "Dockerfile": "Dockerfile",
    "pytest.ini": "pytest.ini",
}


def _templates_root() -> Path:
    """Return filesystem path to packaged Jinja templates."""
    traversable = resources.files("liteit").joinpath("templates")
    try:
        path = Path(os.fspath(traversable))  # type: ignore[arg-type]
    except TypeError:
        path = Path(str(traversable))
    if not path.is_dir():
        raise click.ClickException(
            "liteit templates are missing from the installation. "
            "Reinstall with: pip install -e ."
        )
    return path


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(_templates_root()),
        undefined=StrictUndefined,
        autoescape=select_autoescape(enabled_extensions=()),
        keep_trailing_newline=True,
    )


def _render(template_name: str, **context: object) -> str:
    name = TEMPLATE_ALIASES.get(template_name, template_name)
    env = _env()
    try:
        return env.get_template(name).render(**context)
    except TemplateNotFound as exc:
        available = sorted(env.list_templates())
        raise click.ClickException(
            f"Template not found: {template_name} (resolved: {name}). "
            f"Available: {', '.join(available) or '(none)'}."
        ) from exc


def _write(path: Path, content: str, *, force: bool = False) -> None:
    if path.exists() and not force:
        raise click.ClickException(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _class_prefix(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


@click.group(
    name="liteit",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(package_name="liteit", prog_name="liteit")
def main() -> None:
    """Scaffold Litestar + Granian projects and controllers.

    \b
    Examples:
      liteit init myapi
      liteit generate controller users
      liteit gen controller order_items
      liteit run --reload
      python -m liteit -h

    \b
    After init (Python 3.11+):
      cd myapi
      python -m venv .venv
      pip install -r requirements.txt
      liteit generate controller users
      liteit run --reload
    """


@main.command("init")
@click.argument("project_name")
def init_project(project_name: str) -> None:
    """Create a new liteit project under PROJECT_NAME/.

    \b
    Examples:
      liteit init myapi
      liteit init ./services/payments
    """
    raw = Path(project_name)
    target = raw.resolve()
    display_name = raw.name

    if not MODULE_NAME_RE.match(display_name.replace("-", "_")) and not re.match(
        r"^[A-Za-z][A-Za-z0-9_-]*$", display_name
    ):
        raise click.ClickException(
            "Project name must start with a letter and contain only "
            "letters, digits, hyphens, or underscores."
        )

    if target.exists() and any(target.iterdir()):
        # Allow empty dir; refuse non-empty
        raise click.ClickException(
            f"Directory is not empty: {target}. Choose a new path or empty folder."
        )

    # Refuse if a key file would collide after mkdir
    sentinel = target / "app" / "main.py"
    if sentinel.exists():
        raise click.ClickException(f"Project already initialized (found {sentinel})")

    target.mkdir(parents=True, exist_ok=True)
    context = {"project_name": display_name}

    try:
        for dest_name, template_name in PROJECT_FILES.items():
            dest = target / dest_name
            if dest.exists():
                raise click.ClickException(
                    f"Project already initialized (found {dest_name})"
                )
            _write(dest, _render(template_name, **context))

        package_root = _templates_root() / "project"
        for dest_name, src_name in PROJECT_STATIC_FILES.items():
            dest = target / dest_name
            if dest.exists():
                raise click.ClickException(
                    f"Project already initialized (found {dest_name})"
                )
            src = package_root / src_name
            if not src.is_file():
                raise click.ClickException(
                    f"Missing packaged file templates/project/{src_name}. "
                    "Reinstall liteit."
                )
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    except Exception:
        if target.exists() and target != Path.cwd().resolve():
            shutil.rmtree(target, ignore_errors=True)
        raise

    console.print(
        Panel.fit(
            f"[bold green]Initialized[/] liteit project "
            f"[cyan]{display_name}[/] in [dim]{target}[/]",
            border_style="green",
        )
    )
    console.print("[bold]Next steps:[/]")
    cwd = Path.cwd().resolve()
    if target == cwd:
        console.print("  1. (already in the project directory)")
    else:
        try:
            cd_arg = str(target.relative_to(cwd))
        except ValueError:
            cd_arg = str(target)
        console.print(f"  1. cd {cd_arg}")
    console.print("  2. python -m venv .venv && activate it  # Python 3.11+")
    console.print("  3. pip install -U pip && pip install -r requirements.txt")
    console.print("  4. copy .env.example to .env and edit as needed")
    console.print("  5. liteit generate controller <name>")
    console.print("  6. liteit run --reload")
    console.print(
        f"  # production: docker build -t {display_name} ."
    )


def _register_generate(group: click.Group) -> None:
    """Attach generate/gen command group to *group*."""

    @group.group("generate")
    def generate() -> None:
        """Generate project artifacts.

        \b
        Examples:
          liteit generate controller users
          liteit gen controller order_items --path ./myapi
        """

    @generate.command("controller")
    @click.argument("name")
    @click.option(
        "--path",
        "project_path",
        default=".",
        type=click.Path(file_okay=False, exists=True, path_type=Path),
        help="Project root containing app/controllers/ (default: current directory).",
    )
    def generate_controller(name: str, project_path: Path) -> None:
        """Generate a Litestar Controller and Pydantic schemas.

        Creates app/controllers/<name>.py and app/schemas/<name>.py with CRUD stubs.

        \b
        Examples:
          liteit generate controller users
          liteit gen controller order_items
          liteit generate controller invoices --path ./myapi
        """
        if not MODULE_NAME_RE.match(name):
            raise click.ClickException(
                "Controller name must be snake_case starting with a letter "
                "(e.g. users, order_items)."
            )

        root = project_path.resolve()
        controllers_dir = root / "app" / "controllers"
        schemas_dir = root / "app" / "schemas"
        if not controllers_dir.is_dir():
            raise click.ClickException(
                f"No app/controllers/ directory in {root}. Run 'liteit init' first."
            )
        if not schemas_dir.is_dir():
            raise click.ClickException(
                f"No app/schemas/ directory in {root}. Run 'liteit init' first."
            )

        controller_path = controllers_dir / f"{name}.py"
        schema_path = schemas_dir / f"{name}.py"
        if controller_path.exists():
            raise click.ClickException(f"Controller already exists: {controller_path}")
        if schema_path.exists():
            raise click.ClickException(f"Schema already exists: {schema_path}")

        class_prefix = _class_prefix(name)
        context = {
            "name": name,
            "class_prefix": class_prefix,
            "title": name.replace("_", " ").title(),
        }

        written: list[Path] = []
        try:
            _write(
                controller_path,
                _render("controller/controller.py.j2", **context),
            )
            written.append(controller_path)
            _write(
                schema_path,
                _render("controller/schemas.py.j2", **context),
            )
            written.append(schema_path)
        except Exception:
            for path in written:
                path.unlink(missing_ok=True)
            raise

        console.print(
            f"[bold green]Generated[/] controller [cyan]app/controllers/{name}.py[/] "
            f"and schemas [cyan]app/schemas/{name}.py[/]"
        )
        console.print(
            f"  classes: {class_prefix}Controller, "
            f"{class_prefix}CreateDTO / UpdateDTO / ResponseDTO"
        )
        console.print("Restart the app to pick up the controller in OpenAPI.")

    group.add_command(generate, "gen")


_register_generate(main)


@main.command("run")
@click.option("--host", default="127.0.0.1", show_default=True, help="Bind host.")
@click.option("--port", default=8000, show_default=True, type=int, help="Bind port.")
@click.option("--reload", is_flag=True, default=False, help="Enable auto-reload.")
@click.option(
    "--workers",
    default=1,
    show_default=True,
    type=int,
    help="Number of Granian worker processes.",
)
@click.option(
    "--app",
    "app_target",
    default="app.main:app",
    show_default=True,
    help="ASGI app target for Granian.",
)
@click.option(
    "--path",
    "project_path",
    default=".",
    type=click.Path(file_okay=False, exists=True, path_type=Path),
    help="Project root (default: current directory).",
)
def run_server(
    host: str,
    port: int,
    reload: bool,
    workers: int,
    app_target: str,
    project_path: Path,
) -> None:
    """Run the project with Granian (ASGI).

    \b
    Examples:
      liteit run
      liteit run --reload
      liteit run --host 0.0.0.0 --port 8000 --workers 2
    """
    root = project_path.resolve()
    main_py = root / "app" / "main.py"
    if not main_py.is_file():
        raise click.ClickException(
            f"No app/main.py in {root}. Run this from a liteit project "
            "(or pass --path)."
        )

    cmd = [
        sys.executable,
        "-m",
        "granian",
        "--interface",
        "asgi",
        app_target,
        "--host",
        host,
        "--port",
        str(port),
        "--workers",
        str(workers),
        "--runtime-threads",
        "1",
        "--blocking-threads",
        "4",
    ]
    if reload:
        cmd.append("--reload")

    console.print(
        f"[bold]Starting Granian[/] [dim]{app_target}[/] on "
        f"[cyan]{host}:{port}[/] "
        f"(workers={workers}, runtime-threads=1, blocking-threads=4"
        f"{', reload' if reload else ''})"
    )
    try:
        raise SystemExit(subprocess.call(cmd, cwd=root))
    except FileNotFoundError as exc:
        raise click.ClickException(
            "granian is not installed. Install project deps: pip install -r requirements.txt"
        ) from exc


if __name__ == "__main__":
    main()
