from src.i18n.domain import activate, gettext, ngettext, npgettext, pgettext

DEFAULT_ISO_639 = "en"
SUPPORTED_ISO_639 = {"ru", "en"}

__all__ = [
    "activate",
    "gettext",
    "ngettext",
    "npgettext",
    "pgettext",
    "DEFAULT_ISO_639",
    "SUPPORTED_ISO_639",
]
