"""Fake GSTIN generator and checksum validator.

A GSTIN is 15 characters:

    27  ABCDE 1234 F  1  Z  5
    |   |          |  |  |  check character (mod-36, computed below)
    |   |          |  |  always 'Z' (default)
    |   |          |  entity number for the same PAN in the state (1-9, A-Z)
    |   PAN-shaped part: 5 letters, 4 digits, 1 letter
    state code (2 digits)

The PAN-shaped part here is random, so these are FAKE identifiers that only
look valid. They are for synthetic demo data only, always paired with vendors
and clients whose names start with "DEMO".
"""

from __future__ import annotations

import random
import re
import string

ALPHABET = string.digits + string.ascii_uppercase  # "0-9A-Z": value of a char = its index (0-35)
_BASE = len(ALPHABET)  # 36

GSTIN_PATTERN = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")

# GST state/UT codes (01-38) plus 97 (Other Territory) and 99 (Centre Jurisdiction).
VALID_STATE_CODES = frozenset({f"{n:02d}" for n in range(1, 39)} | {"97", "99"})


def checksum_char(first14: str) -> str:
    """Return the GSTIN check character for the first 14 characters.

    Luhn mod-36: walk the 14 chars, multiply every second one by 2, fold each
    product back into base 36 (quotient + remainder), add them up, and pick the
    character that brings the total to a multiple of 36.
    """
    if len(first14) != 14:
        raise ValueError("expected exactly 14 characters")
    total = 0
    for i, ch in enumerate(first14):
        value = ALPHABET.index(ch)
        product = value * (2 if i % 2 else 1)
        total += product // _BASE + product % _BASE
    return ALPHABET[(_BASE - total % _BASE) % _BASE]


def make_fake_gstin(state_code: int | str, rng: random.Random) -> str:
    """Build a random, checksum-valid (but fake) GSTIN for the given state code.

    Pass a seeded ``random.Random`` so the same seed always gives the same GSTINs.
    """
    code = f"{int(state_code):02d}"
    if code not in VALID_STATE_CODES:
        raise ValueError(f"unknown GST state code: {state_code!r}")

    letters, digits = string.ascii_uppercase, string.digits
    pan_like = (
        "".join(rng.choice(letters) for _ in range(5))
        + "".join(rng.choice(digits) for _ in range(4))
        + rng.choice(letters)
    )
    entity = rng.choice(ALPHABET[1:])  # 1-9 or A-Z (never 0)
    first14 = code + pan_like + entity + "Z"
    return first14 + checksum_char(first14)


def is_valid_gstin(s: str) -> bool:
    """True if ``s`` has the GSTIN shape, a known state code and a correct check character."""
    if not isinstance(s, str) or not GSTIN_PATTERN.fullmatch(s):
        return False
    if s[:2] not in VALID_STATE_CODES:
        return False
    return checksum_char(s[:14]) == s[14]
