# WirelessPassfinder

[![CI](https://github.com/Mohammadrce/WirelessPassfinder/actions/workflows/python-app.yml/badge.svg)](https://github.com/Mohammadrce/WirelessPassfinder/actions/workflows/python-app.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

WirelessPassfinder is a Windows WiFi profile auditor CLI.
It reads saved WLAN profiles from your own machine via `netsh` and shows them with secure defaults.

## Why this exists

- Audit your stored WiFi profiles quickly.
- Export profile metadata to JSON for personal backup workflows.
- Keep plaintext keys hidden by default to reduce accidental leakage in screenshots or logs.

## Features

- `wpfinder list`: fast list of profile names (table or JSON)
- `wpfinder list --detailed`: full profile metadata and password field
- `wpfinder show <profile>`: inspect one profile
- `wpfinder export --output <file.json>`: export all profiles to JSON
- Password masking by default (`********`)
- Optional plaintext output only with explicit flags (`--detailed --show-keys` / `--show-key`)

## Requirements

- Windows (v1 target)
- Python 3.10+

## Installation

### With `pipx` (recommended)

```bash
pipx install git+https://github.com/Mohammadrce/WirelessPassfinder.git
```

### From source

```bash
git clone git@github.com:Mohammadrce/WirelessPassfinder.git
cd WirelessPassfinder
python -m pip install -e .
```

## Usage

```bash
wpfinder list
wpfinder list --json
wpfinder list --filter Home
wpfinder list --detailed
wpfinder list --detailed --show-keys

wpfinder show "HomeWiFi"
wpfinder show "HomeWiFi" --show-key
wpfinder show "HomeWiFi" --json

wpfinder export --output wifi_profiles.json
wpfinder export --output wifi_profiles_plain.json --show-keys
```

## Upgrade notes (v0.2.1)

- `wpfinder list` is now fast-by-default and prints profile names only.
- Use `wpfinder list --detailed` for authentication/cipher/key/password columns.
- `--show-keys` now requires `--detailed` for `list`.
- Legacy `python wifi.py` entry path has been removed.

## Security notice

- This tool is for auditing credentials already stored on your own system.
- It does not crack, decrypt, or attack networks.
- Use plaintext password flags carefully.

## Development

```bash
python -m pip install -e .[dev]
ruff check .
mypy src
pytest
```

## Roadmap

- Improve localization handling for non-English `netsh` output
- Add optional executable packaging workflow
- Evaluate Linux/macOS support in a future major version

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - see [LICENSE](LICENSE).

---

## فارسی (خلاصه)

این ابزار برای ممیزی پروفایل‌های وای‌فای ذخیره‌شده روی ویندوز است.
به‌صورت پیش‌فرض رمزها را ماسک می‌کند و فقط با فلگ صریح رمز واقعی را نشان می‌دهد.
برای مشارکت، فایل `CONTRIBUTING.md` را ببینید.
