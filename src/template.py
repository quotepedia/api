from typing import Any

from jinja2 import Environment, FileSystemLoader, Template
from jinja2.ext import i18n

from src.config import settings

env = Environment(extensions=[i18n], loader=FileSystemLoader(settings.path.templates))


def render(name: str | Template, *args: Any, **kwargs: Any) -> str:
    _set_extra_kwargs(kwargs)
    template = env.get_template(name)
    return template.render(*args, **kwargs)


def _set_extra_kwargs(kwargs: Any):
    kwargs["organization"] = settings.app.name


__all__ = ["env", "render"]
