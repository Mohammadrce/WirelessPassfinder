from __future__ import annotations

import json
from pathlib import Path

from wireless_passfinder.cli import main
from wireless_passfinder.models import WifiProfile
from wireless_passfinder.netsh_adapter import NotSupportedOSError, ProfileNotFoundError


class FakeAdapter:
    @staticmethod
    def _profiles() -> list[WifiProfile]:
        return [
            WifiProfile(
                name="HomeWiFi",
                authentication="WPA2-Personal",
                cipher="CCMP",
                has_key=True,
                password="secret-home",
            ),
            WifiProfile(
                name="OfficeNet",
                authentication="WPA2-Enterprise",
                cipher="GCMP",
                has_key=False,
                password=None,
            ),
        ]

    def list_profile_names(self) -> list[str]:
        return [profile.name for profile in self._profiles()]

    def list_profiles_detailed(self) -> list[WifiProfile]:
        return self._profiles()

    def get_profile(self, profile_name: str) -> WifiProfile:
        if profile_name == "HomeWiFi":
            return self._profiles()[0]
        raise ProfileNotFoundError(f'WiFi profile "{profile_name}" was not found.')


def test_list_default_prints_name_only(monkeypatch, capsys) -> None:
    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", lambda: FakeAdapter())

    exit_code = main(["list"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "HomeWiFi" in captured.out
    assert "OfficeNet" in captured.out
    assert "Authentication" not in captured.out
    assert "secret-home" not in captured.out


def test_list_json_default_returns_names_only(monkeypatch, capsys) -> None:
    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", lambda: FakeAdapter())

    exit_code = main(["list", "--json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload == ["HomeWiFi", "OfficeNet"]


def test_list_detailed_masks_password_by_default(monkeypatch, capsys) -> None:
    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", lambda: FakeAdapter())

    exit_code = main(["list", "--detailed"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Authentication" in captured.out
    assert "********" in captured.out
    assert "secret-home" not in captured.out


def test_list_detailed_show_keys(monkeypatch, capsys) -> None:
    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", lambda: FakeAdapter())

    exit_code = main(["list", "--detailed", "--show-keys"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "secret-home" in captured.out


def test_list_detailed_json_returns_objects(monkeypatch, capsys) -> None:
    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", lambda: FakeAdapter())

    exit_code = main(["list", "--detailed", "--json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert isinstance(payload, list)
    assert payload[0]["name"] == "HomeWiFi"
    assert payload[0]["password"] == "********"


def test_list_show_keys_without_detailed_returns_error(monkeypatch, capsys) -> None:
    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", lambda: FakeAdapter())

    exit_code = main(["list", "--show-keys"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "--show-keys can only be used with --detailed" in captured.err


def test_show_json_masks_by_default(monkeypatch, capsys) -> None:
    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", lambda: FakeAdapter())

    exit_code = main(["show", "HomeWiFi", "--json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    assert payload["name"] == "HomeWiFi"
    assert payload["password"] == "********"


def test_export_json_file(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", lambda: FakeAdapter())
    output_file = tmp_path / "export" / "wifi.json"

    exit_code = main(["export", "--output", str(output_file)])

    captured = capsys.readouterr()
    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert output_file.exists()
    assert payload["profile_count"] == 2
    assert payload["profiles"][0]["password"] == "********"
    assert "Exported 2 profile(s)" in captured.out


def test_non_windows_path_returns_error(monkeypatch, capsys) -> None:
    class UnsupportedAdapter:
        def __init__(self) -> None:
            raise NotSupportedOSError("Windows only")

    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", UnsupportedAdapter)
    exit_code = main(["list"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Windows only" in captured.err


def test_show_invalid_profile_returns_error(monkeypatch, capsys) -> None:
    monkeypatch.setattr("wireless_passfinder.cli.NetshAdapter", lambda: FakeAdapter())

    exit_code = main(["show", "MissingWiFi"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "was not found" in captured.err
