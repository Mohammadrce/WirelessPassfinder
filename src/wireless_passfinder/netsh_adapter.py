from __future__ import annotations

import os
import re
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from wireless_passfinder.models import WifiProfile

PROFILE_NAME_RE = re.compile(r"All User Profile\s*:\s*(.+)")
AUTH_RE = re.compile(r"Authentication\s*:\s*(.+)")
CIPHER_RE = re.compile(r"Cipher\s*:\s*(.+)")
SECURITY_KEY_RE = re.compile(r"Security key\s*:\s*(.+)")
KEY_CONTENT_RE = re.compile(r"Key Content\s*:\s*(.+)")


class WifiAdapterError(RuntimeError):
    """Base class for adapter-level errors."""


class NotSupportedOSError(WifiAdapterError):
    """Raised when the tool is run on non-Windows systems."""


class NetshNotAvailableError(WifiAdapterError):
    """Raised when netsh cannot be executed."""


@dataclass
class NetshExecutionError(WifiAdapterError):
    command: str
    returncode: int
    stdout: str
    stderr: str

    def __str__(self) -> str:
        details = self.stderr.strip() or self.stdout.strip() or "No details."
        return f"{self.command} failed with exit code {self.returncode}: {details}"


class ProfileNotFoundError(WifiAdapterError):
    """Raised when a requested WiFi profile does not exist."""


def parse_profiles_output(raw_output: str) -> list[str]:
    profiles: list[str] = []
    for match in PROFILE_NAME_RE.finditer(raw_output):
        profile_name = match.group(1).strip()
        if profile_name and profile_name not in profiles:
            profiles.append(profile_name)
    return profiles


def _first_match(pattern: re.Pattern[str], text: str, default: str = "Unknown") -> str:
    match = pattern.search(text)
    if not match:
        return default
    return match.group(1).strip() or default


def _optional_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1).strip() or None


def parse_profile_output(profile_name: str, raw_output: str) -> WifiProfile:
    authentication = _first_match(AUTH_RE, raw_output)
    cipher = _first_match(CIPHER_RE, raw_output)
    password = _optional_match(KEY_CONTENT_RE, raw_output)
    security_key_value = _optional_match(SECURITY_KEY_RE, raw_output)

    if security_key_value is None:
        has_key = password is not None
    else:
        normalized = security_key_value.lower()
        if normalized in {"present", "yes"}:
            has_key = True
        elif normalized in {"absent", "no"}:
            has_key = False
        else:
            has_key = password is not None

    if not has_key:
        password = None

    return WifiProfile(
        name=profile_name,
        authentication=authentication,
        cipher=cipher,
        has_key=has_key,
        password=password,
    )


class NetshAdapter:
    def __init__(
        self,
        runner: Callable[[Sequence[str]], subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        self._runner = runner or self._default_runner

    @staticmethod
    def _default_runner(args: Sequence[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["netsh", *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def _run(self, args: Sequence[str]) -> str:
        if os.name != "nt":
            raise NotSupportedOSError(
                "wireless-passfinder currently supports Windows only "
                "(non-Windows execution is disabled)."
            )

        try:
            completed = self._runner(args)
        except FileNotFoundError as exc:
            raise NetshNotAvailableError(
                "netsh is not available on this machine. "
                "Ensure Windows networking tools are installed."
            ) from exc

        if completed.returncode != 0:
            raise NetshExecutionError(
                command=f"netsh {' '.join(args)}",
                returncode=completed.returncode,
                stdout=completed.stdout or "",
                stderr=completed.stderr or "",
            )

        return completed.stdout or ""

    def list_profile_names(self) -> list[str]:
        raw_output = self._run(["wlan", "show", "profiles"])
        return parse_profiles_output(raw_output)

    def get_profile(self, profile_name: str) -> WifiProfile:
        args = ["wlan", "show", "profile", f"name={profile_name}", "key=clear"]
        try:
            raw_output = self._run(args)
        except NetshExecutionError as exc:
            details = f"{exc.stdout}\n{exc.stderr}".lower()
            if "not found" in details or "there is no profile" in details:
                raise ProfileNotFoundError(f'WiFi profile "{profile_name}" was not found.') from exc
            raise

        return parse_profile_output(profile_name=profile_name, raw_output=raw_output)

    def list_profiles_detailed(self) -> list[WifiProfile]:
        profiles: list[WifiProfile] = []
        for profile_name in self.list_profile_names():
            profiles.append(self.get_profile(profile_name))
        return profiles
