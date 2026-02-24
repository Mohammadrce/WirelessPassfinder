from __future__ import annotations

from collections.abc import Iterable

from wireless_passfinder.models import WifiProfile


def format_profile_names_table(profile_names: Iterable[str]) -> str:
    names = list(profile_names)
    if not names:
        return "No WiFi profiles found."

    header = "Profile"
    width = max(len(header), *(len(name) for name in names))
    header_line = header.ljust(width)
    separator_line = "-" * width
    body = [name.ljust(width) for name in names]
    return "\n".join([header_line, separator_line, *body])


def format_profiles_table(
    profiles: Iterable[WifiProfile],
    *,
    show_key_material: bool = False,
) -> str:
    profile_list = list(profiles)
    if not profile_list:
        return "No WiFi profiles found."

    headers = ("Profile", "Authentication", "Cipher", "Security Key", "Password")
    rows = [
        (
            profile.name,
            profile.authentication,
            profile.cipher,
            profile.key_status,
            profile.display_password(show_key_material=show_key_material),
        )
        for profile in profile_list
    ]

    widths = [len(header) for header in headers]
    for row in rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len(value))

    def _render_row(values: tuple[str, str, str, str, str]) -> str:
        return " | ".join(value.ljust(widths[idx]) for idx, value in enumerate(values))

    header_line = " | ".join(headers[idx].ljust(widths[idx]) for idx in range(len(headers)))
    separator_line = "-+-".join("-" * widths[idx] for idx in range(len(headers)))
    body = [_render_row(row) for row in rows]
    return "\n".join([header_line, separator_line, *body])


def format_profile_details(profile: WifiProfile, *, show_key_material: bool = False) -> str:
    return "\n".join(
        [
            f"Profile: {profile.name}",
            f"Authentication: {profile.authentication}",
            f"Cipher: {profile.cipher}",
            f"Security key: {profile.key_status}",
            f"Password: {profile.display_password(show_key_material=show_key_material)}",
        ]
    )
