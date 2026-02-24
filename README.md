# WirelessPassfinder

[![CI](https://github.com/Mohammadrce/WirelessPassfinder/actions/workflows/python-app.yml/badge.svg)](https://github.com/Mohammadrce/WirelessPassfinder/actions/workflows/python-app.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

Windows CLI to audit saved WiFi profiles and export credentials with safe-by-default masking.

Who this is for:
- Windows users who want to review saved WiFi profiles on their own machine.
- Developers/admins who want quick, scriptable JSON exports.

## Table of Contents

- [What It Does](#what-it-does)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Security and Responsible Use](#security-and-responsible-use)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Upgrade Notes (v0.2.1)](#upgrade-notes-v021)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [فارسی (خلاصه)](#فارسی-خلاصه)

## What It Does

`WirelessPassfinder` is a WiFi profile auditor for Windows.
It reads WLAN profile data from your local machine using `netsh` and provides:

- Fast profile listing (`wpfinder list`)
- Detailed profile inspection (`wpfinder show`)
- JSON export for backup/automation (`wpfinder export`)
- Password masking by default (`********`)

## Requirements

- Windows (v1 scope)
- Python 3.10+

## Installation

### Option 1: pipx (recommended)

```bash
pipx install git+https://github.com/Mohammadrce/WirelessPassfinder.git
```

### Option 2: from source

```bash
git clone git@github.com:Mohammadrce/WirelessPassfinder.git
cd WirelessPassfinder
python -m pip install -e .
```

### Verify installation

```bash
wpfinder --help
```

## Usage

### 1) List profiles quickly (fast path)

```bash
wpfinder list
wpfinder list --json
wpfinder list --filter Home
```

### 2) List full details

```bash
wpfinder list --detailed
wpfinder list --detailed --json
```

### 3) Show plaintext keys intentionally

Warning: this prints sensitive credentials.

```bash
wpfinder list --detailed --show-keys
wpfinder show "HomeWiFi" --show-key
```

Notes:
- `--show-keys` is valid for `list` only when `--detailed` is present.
- `wpfinder list --show-keys` returns an explicit error by design.

### 4) Inspect one profile

```bash
wpfinder show "HomeWiFi"
wpfinder show "HomeWiFi" --json
```

### 5) Export JSON backup

```bash
wpfinder export --output wifi_profiles.json
wpfinder export --output wifi_profiles_plain.json --show-keys
```

## Security and Responsible Use

- This tool only reads credentials already stored on your own Windows system.
- It does not crack, brute-force, decrypt, or attack networks.
- Use plaintext key flags only when necessary.
- Avoid sharing terminal output or exported files that contain real passwords.

## Troubleshooting

### Non-Windows systems

The tool is Windows-only in v1. On non-Windows systems, it exits with a clear unsupported-platform error.

### `netsh` not available

If Windows cannot run `netsh`, ensure networking tools are available on your system image and run from a normal Windows shell.

### Missing key output / access limitations

Some environments may require appropriate privileges to reveal plaintext key material (`key=clear` behavior in `netsh`).

### Localization caveat

`netsh` output can vary by system language. Parsing is optimized for common output formats and may need adjustments on non-English environments.

### Local pytest plugin conflicts

If global pytest plugins interfere with local test runs, use:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest
```

## Development

```bash
python -m pip install -e .[dev]
ruff check .
mypy src
pytest
```

## Upgrade Notes (v0.2.1)

- `wpfinder list` is fast-by-default and prints profile names only.
- Use `wpfinder list --detailed` for auth/cipher/key/password fields.
- For `list`, `--show-keys` now requires `--detailed`.
- Legacy `python wifi.py` entry path was removed.

## Roadmap

- Improve parsing reliability for more localized `netsh` outputs
- Optional executable distribution workflow
- Evaluate Linux/macOS support in a future major version

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - see [LICENSE](LICENSE).

---

## فارسی (خلاصه)

این ابزار یک CLI ویندوزی برای ممیزی پروفایل‌های وای‌فای ذخیره‌شده روی سیستم خودت است.
خروجی رمزها به‌صورت پیش‌فرض ماسک می‌شود و فقط با فلگ‌های صریح نمایش داده می‌شود.
برای دیدن جزئیات کامل از `--detailed` و برای نمایش رمز واقعی با مسئولیت خودت از `--show-key` یا `--show-keys` استفاده کن.
