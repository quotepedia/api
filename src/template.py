import os
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template
from jinja2.ext import i18n

from src.config import settings

DIRNAME = "templates"


def get_template_dirs() -> list[str]:
    return [os.path.join(root, DIRNAME) for root, dirs, _ in os.walk(settings.path.templates) if DIRNAME in dirs]


env = Environment(
    extensions=[i18n],
    auto_reload=settings.debug,
    loader=FileSystemLoader(get_template_dirs()),
)


def render(name: str | Template, *args: Any, **kwargs: Any) -> str:
    _set_extra_kwargs(kwargs)
    template = env.get_template(name)
    return template.render(*args, **kwargs)


def _set_extra_kwargs(kwargs: Any):
    kwargs["organization"] = settings.app.name


__all__ = ["env", "render"]
