from __future__ import annotations

from pathlib import Path

from wireless_passfinder.netsh_adapter import (
    parse_profile_output,
    parse_profiles_output,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def test_parse_profiles_output_extracts_names() -> None:
    raw_output = _read_fixture("netsh_profiles.txt")
    profiles = parse_profiles_output(raw_output)
    assert profiles == ["HomeWiFi", "OfficeNet", "CoffeeShop"]


def test_parse_profile_output_with_key() -> None:
    raw_output = _read_fixture("netsh_profile_with_key.txt")
    profile = parse_profile_output("HomeWiFi", raw_output)

    assert profile.name == "HomeWiFi"
    assert profile.authentication == "WPA2-Personal"
    assert profile.cipher == "CCMP"
    assert profile.has_key is True
    assert profile.password == "supersecret123"


def test_parse_profile_output_without_key() -> None:
    raw_output = _read_fixture("netsh_profile_without_key.txt")
    profile = parse_profile_output("OfficeNet", raw_output)

    assert profile.name == "OfficeNet"
    assert profile.authentication == "WPA2-Enterprise"
    assert profile.cipher == "GCMP"
    assert profile.has_key is False
    assert profile.password is None
