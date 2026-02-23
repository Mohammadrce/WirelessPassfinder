from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MASKED_PASSWORD = "********"


@dataclass(frozen=True)
class WifiProfile:
    name: str
    authentication: str = "Unknown"
    cipher: str = "Unknown"
    has_key: bool = False
    password: str | None = None

    @property
    def key_status(self) -> str:
        return "present" if self.has_key else "absent"

    def display_password(self, show_key_material: bool = False) -> str:
        if not self.has_key:
            return "N/A"
        if not self.password:
            return "<stored key unavailable>"
        if show_key_material:
            return self.password
        return MASKED_PASSWORD

    def to_dict(self, show_key_material: bool = False) -> dict[str, Any]:
        password: str | None
        if not self.has_key or not self.password:
            password = None
        elif show_key_material:
            password = self.password
        else:
            password = MASKED_PASSWORD

        return {
            "name": self.name,
            "authentication": self.authentication,
            "cipher": self.cipher,
            "has_key": self.has_key,
            "key_status": self.key_status,
            "password": password,
        }
