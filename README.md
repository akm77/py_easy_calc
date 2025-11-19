# Py Easy Calc

`py-easy-calc` is a compact financial calculator library that evaluates arithmetic expressions with percentage-aware operators. It is designed for bots and automation where users submit calculation requests as plain text.

## Features

- Percentage-aware arithmetic (`+`, `-`, `*`, `/` with `%` suffix support).
- Safe evaluation returning `None` for invalid expressions or division by zero.
- Decimal precision control with automatic trimming of trailing zeros.

## Installation

Install directly from the public GitHub repository.

- Using pip:

```bash
pip install git+https://github.com/akm77/py_easy_calc.git
```

- Using poetry:

```bash
poetry add git+https://github.com/akm77/py_easy_calc.git
```

Or declare the dependency in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
py-easy-calc = { git = "https://github.com/akm77/py_easy_calc.git", rev = "main" }
```

## Usage

```python
from calculator import calc_expression

result = calc_expression("100 + 2%")
print(result)  # Decimal("102")
```

Control precision (default `precision=4`, trailing zeros are trimmed automatically):

```python
calc_expression("10 / 3")  # Decimal("3.3333")
calc_expression("10 / 3", precision=3)  # Decimal("3.333")
```

## Percent-aware Syntax

Expressions support attaching `%` directly after terms when performing arithmetic so they behave like `value * percent / 100`. The parser recognizes patterns such as `A + B%`, `A - B%`, `A * B%`, `A / B%`, and combinations inside parentheses. Percent notation only applies to the immediately preceding operand, so `100 + 5% * 2` is interpreted as `100 + (5% * 2)` rather than `(100 + 5%) * 2`.

## Publishing to PyPI

1. Update `pyproject.toml` and bump `version`. Save changelog entry.
2. Build
```
poetry build
```
3. Upload
```
poetry publish --username <username> --password <password>
```

## GitHub Release Template

- **Title**: `v{version}`
- **Description**: summary of changes and highlights.
- **Checklist**:
  - [ ] Update README & changelog
  - [ ] Run `poetry build`
  - [ ] Upload distribution via `poetry publish`

## Release Checklist

- Bump `version` in `pyproject.toml` and add a note in `CHANGELOG.md` (if present).
- Run `poetry run ruff check .` and `poetry run pytest` to cover lint and regression tests.
- Build distributions (`poetry build`) and verify the generated artifacts in `dist/`.
- Tag the release on GitHub (`git tag vX.Y.Z` + `git push --tags`).
- Publish on PyPI (`poetry publish --with dev --username <user> --password <pass>` or use `twine`).
- Update the GitHub Release notes using the template above and merge any pending docs updates.

## Automated Release Notes

Run `scripts/generate_release_notes.py` after tagging a new version to summarize all commits since the previous release. You can redirect the output to a file for reuse in GitHub releases:

```bash
python scripts/generate_release_notes.py --version v0.1.0 > RELEASE_NOTES.md
```

Pass `--since <tag>` to override the default base reference, or `--output <path>` to write the notes to a specific file without piping through the shell.

## License

MIT © akm77