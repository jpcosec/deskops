"""Shared ASCII slug helper for ids deskops derives from a title."""

from __future__ import annotations

import re
import unicodedata


def ascii_slug(text: str) -> str:
    """Lowercase ``text``, fold accents to ASCII (a-acute -> a, n-tilde -> n) and join [a-z0-9] runs with '-'.

    May return an empty string; callers apply their own default and maximum length.
    """
    folded = "".join(ch for ch in unicodedata.normalize("NFKD", str(text)) if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")
