"""
This module provides utilities for parsing Accept-Language HTTP header
and determining the preferred language based on specified quality values.

Read more at https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language.
"""

from dataclasses import dataclass
from functools import cache, cached_property
from typing import Sequence

from src.i18n import DEFAULT_ISO_639, SUPPORTED_ISO_639

LANGUAGE_TAG_SEP = "-"
LANGUAGE_TAG_ISO_639_INDEX = 0
LANGUAGE_TAG_ISO_3166_INDEX = 1

LANGUAGE_PREFERENCE_SEP = ";"
LANGUAGE_PREFERENCE_CODE_INDEX = 0
LANGUAGE_PREFERENCE_QUALITY_INDEX = 1
LANGUAGE_PREFERENCE_QUALITY_PREFIX = "q="
LANGUAGE_PREFERENCE_QUALITY_MAX = 1.0

ACCEPT_LANGUAGE_SEP = ","


@dataclass(frozen=True)
class LanguageTag:
    """Represents a language tag consisting of ISO 639 and ISO 3166 components.

    Examples:
        >>> tag = LanguageTag("en-US")
        >>> tag.iso_639
        'en'
        >>> tag.iso_3166
        'US'
    """

    raw: str
    """
    The raw [BCP47](https://www.ietf.org/rfc/bcp/bcp47.txt) language code (e.g., "en-US").
    """

    @cached_property
    def _substrings(self) -> Sequence[str]:
        return self.raw.split(LANGUAGE_TAG_SEP)

    @cached_property
    def iso_639(self) -> str:
        """
        Returns the [ISO 639](https://wikipedia.org/wiki/ISO_639) part of the tag.
        """

        return self._substrings[LANGUAGE_TAG_ISO_639_INDEX].strip()

    @cached_property
    def iso_3166(self) -> str:
        """
        The [ISO 3166](https://wikipedia.org/wiki/ISO_3166) part of the tag.
        """

        return self._substrings[LANGUAGE_TAG_ISO_3166_INDEX].strip()


@dataclass(frozen=True)
class LanguagePreference:
    """Represents a language preference from the Accept-Language HTTP header.

    Examples:
        >>> preference = LanguagePreference("en;q=0.8")
        >>> preference.tag.iso_639
        'en'
        >>> preference.quality
        0.8
        >>> preference.is_quality_present
        True
    """

    raw: str
    """
    The raw language preference string (e.g., "en;q=0.8").
    """

    @cached_property
    def _substrings(self) -> Sequence[str]:
        return self.raw.split(LANGUAGE_PREFERENCE_SEP)

    @cached_property
    def _raw_tag(self) -> str:
        return self._substrings[LANGUAGE_PREFERENCE_CODE_INDEX].strip()

    @cached_property
    def _raw_quality(self) -> str:
        return self._substrings[LANGUAGE_PREFERENCE_QUALITY_INDEX].strip()

    @cached_property
    def tag(self) -> LanguageTag:
        """
        The parsed [BCP47](https://www.ietf.org/rfc/bcp/bcp47.txt) language code.
        """

        return LanguageTag(raw=self._raw_tag)

    @cached_property
    def quality(self) -> float:
        """
        The quality value of the language or 1.0 if not present.
        """

        if not self.is_quality_present:
            return LANGUAGE_PREFERENCE_QUALITY_MAX

        start_index = len(LANGUAGE_PREFERENCE_QUALITY_PREFIX)
        return float(self._raw_quality[start_index:])

    @cached_property
    def is_quality_present(self) -> bool:
        """Determines whether a quality value is present in the language preference."""

        is_index_present = len(self._substrings) > LANGUAGE_PREFERENCE_QUALITY_INDEX
        return is_index_present and self._raw_quality.startswith(LANGUAGE_PREFERENCE_QUALITY_PREFIX)


@cache
def get_preferred_iso_639(accept_language: str) -> str:
    """Parses the Accept-Language HTTP header into the preferred or default ISO 639 language.

    Args:
        accept_language (str): The Accept-Language HTTP header string.

    Returns:
        str: The preferred ISO 639 language code, or the default if none are supported.

    Examples:
        >>> get_preferred_iso_639("fr-CH, en;q=0.4, de;q=0.9, ru, *;q=0.5")
        'ru'
        >>> get_preferred_iso_639("es;q=0.5, fr;q=0.6") # NOTE: 'es' and 'fr' are not supported. 'en' is default.
        'en'
    """

    preferences = [LanguagePreference(raw=preference) for preference in accept_language.split(ACCEPT_LANGUAGE_SEP)]
    supported_preferences = [preference for preference in preferences if preference.tag.iso_639 in SUPPORTED_ISO_639]

    if not supported_preferences:
        return DEFAULT_ISO_639

    most_weighted_preference = max(supported_preferences, key=lambda tag: tag.quality)
    return most_weighted_preference.tag.iso_639


__all__ = [
    "LanguageTag",
    "LanguagePreference",
    "get_preferred_iso_639",
]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
