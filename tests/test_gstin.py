import random
import re

import pytest

from gstcopilot.datagen.gstin import (
    ALPHABET,
    checksum_char,
    is_valid_gstin,
    make_fake_gstin,
)

FORMAT = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")


@pytest.fixture
def gstins():
    rng = random.Random(42)
    states = [27, 29, 24, 7, 33, 9]
    return [make_fake_gstin(rng.choice(states), rng) for _ in range(1000)]


def test_1000_generated_gstins_are_valid(gstins):
    assert all(is_valid_gstin(g) for g in gstins)


def test_format_is_15_chars_and_matches_pattern(gstins):
    for g in gstins:
        assert len(g) == 15
        assert FORMAT.fullmatch(g)


def test_state_code_is_kept():
    rng = random.Random(1)
    assert make_fake_gstin(7, rng).startswith("07")
    assert make_fake_gstin("29", rng).startswith("29")


def test_changing_any_single_character_fails():
    rng = random.Random(7)
    for _ in range(25):
        g = make_fake_gstin(27, rng)
        for pos in range(15):
            for ch in ALPHABET:
                if ch == g[pos]:
                    continue
                mutated = g[:pos] + ch + g[pos + 1 :]
                assert not is_valid_gstin(mutated), (g, mutated)


def test_same_seed_gives_same_output():
    a = [make_fake_gstin(27, random.Random(42)) for _ in range(3)]
    rng1, rng2 = random.Random(42), random.Random(42)
    seq1 = [make_fake_gstin(27, rng1) for _ in range(50)]
    seq2 = [make_fake_gstin(27, rng2) for _ in range(50)]
    assert seq1 == seq2
    assert len(set(a)) == 1


def test_different_seeds_give_different_output():
    assert make_fake_gstin(27, random.Random(1)) != make_fake_gstin(27, random.Random(2))


def test_checksum_hand_worked_cases():
    # Synthetic inputs, worked by hand (no real GSTINs anywhere in this repo):
    # all zeros -> total 0 -> check value 0 -> "0"
    assert checksum_char("0" * 14) == "0"
    # "1" in position 0 (factor 1) -> total 1 -> (36 - 1) % 36 = 35 -> "Z"
    assert checksum_char("1" + "0" * 13) == "Z"
    # "1" in position 1 (factor 2) -> total 2 -> 34 -> "Y"
    assert checksum_char("01" + "0" * 12) == "Y"
    # "Z" (35) in position 1: 35*2 = 70 -> 70//36 + 70%36 = 1 + 34 = 35 -> check 1 -> "1"
    assert checksum_char("0Z" + "0" * 12) == "1"


def test_rejects_malformed_input():
    good = make_fake_gstin(27, random.Random(3))
    bad_inputs = [
        "",
        good[:14],          # too short
        good + "V",         # too long
        good.lower(),       # lowercase
        "00" + good[2:],    # state code 00 doesn't exist
        None,
        12345,
    ]
    for bad in bad_inputs:
        assert not is_valid_gstin(bad), bad


def test_unknown_state_code_raises():
    with pytest.raises(ValueError):
        make_fake_gstin(55, random.Random(0))
