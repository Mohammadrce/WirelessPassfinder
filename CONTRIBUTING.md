# Contributing to WirelessPassfinder

Thanks for contributing.

## Development setup

```bash
git clone git@github.com:Mohammadrce/WirelessPassfinder.git
cd WirelessPassfinder
python -m pip install -e .[dev]
```

## Quality checks

Run all checks before opening a pull request:

```bash
ruff check .
mypy src
pytest
```

## Pull request guidelines

- Keep pull requests focused and small.
- Add or update tests for behavior changes.
- Update documentation when CLI behavior changes.
- Use clear commit messages.

## Reporting issues

Use GitHub Issues and include:

- Expected behavior
- Actual behavior
- Steps to reproduce
- Windows version and Python version
