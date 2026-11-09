"""Ensure packaged Jinja templates are complete and renderable."""

from __future__ import annotations

from jinja2 import Environment, PackageLoader, StrictUndefined
from jinja2 import select_autoescape

from liteit.cli import PROJECT_FILES, PROJECT_STATIC_FILES, _templates_root


REQUIRED_TEMPLATES = [
    "project/app/__init__.py.j2",
    "project/app/main.py.j2",
    "project/app/config.py.j2",
    "project/app/controllers/__init__.py.j2",
    "project/app/controllers/health.py.j2",
    "project/app/schemas/__init__.py.j2",
    "project/app/schemas/health.py.j2",
    "project/app/core/__init__.py.j2",
    "project/app/core/logging.py.j2",
    "project/app/core/security.py.j2",
    "project/tests/__init__.py.j2",
    "project/tests/conftest.py.j2",
    "project/tests/test_health.py.j2",
    "project/env.example.j2",
    "project/requirements.txt.j2",
    "project/README.md.j2",
    "project/gitignore",
    "project/Dockerfile",
    "project/pytest.ini",
    "controller/controller.py.j2",
    "controller/schemas.py.j2",
]


def test_templates_root_exists() -> None:
    root = _templates_root()
    assert root.is_dir()
    assert (root / "project").is_dir()
    assert (root / "controller").is_dir()


def test_required_templates_present() -> None:
    loader = PackageLoader("liteit", "templates")
    names = set(loader.list_templates())
    missing = [name for name in REQUIRED_TEMPLATES if name not in names]
    assert not missing, f"Missing templates: {missing}"


def test_project_file_map_covers_templates() -> None:
    loader = PackageLoader("liteit", "templates")
    names = set(loader.list_templates())
    for dest, template in PROJECT_FILES.items():
        assert template in names, f"{dest} maps to missing {template}"


def test_static_project_files_exist() -> None:
    root = _templates_root() / "project"
    for dest, src_name in PROJECT_STATIC_FILES.items():
        path = root / src_name
        assert path.is_file(), f"static source for {dest} missing: {path}"


def test_project_templates_render() -> None:
    env = Environment(
        loader=PackageLoader("liteit", "templates"),
        undefined=StrictUndefined,
        autoescape=select_autoescape(enabled_extensions=()),
    )
    for template_name in (
        "project/app/main.py.j2",
        "project/app/config.py.j2",
        "project/env.example.j2",
        "project/requirements.txt.j2",
        "project/README.md.j2",
    ):
        rendered = env.get_template(template_name).render(project_name="demoapi")
        assert "demoapi" in rendered


def test_controller_templates_render() -> None:
    env = Environment(
        loader=PackageLoader("liteit", "templates"),
        undefined=StrictUndefined,
        autoescape=select_autoescape(enabled_extensions=()),
    )
    context = {
        "name": "order_items",
        "class_prefix": "OrderItems",
        "title": "Order Items",
    }
    controller = env.get_template("controller/controller.py.j2").render(**context)
    schemas = env.get_template("controller/schemas.py.j2").render(**context)
    assert "class OrderItemsController" in controller
    assert "OrderItemsCreateDTO" in schemas
    assert "OrderItemsUpdateDTO" in schemas
    assert "OrderItemsResponseDTO" in schemas
