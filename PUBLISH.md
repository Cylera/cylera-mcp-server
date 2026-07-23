# Publishing to PyPI

This document describes how to publish `cylera-mcp-server` to PyPI using the automated release workflow.

## Prerequisites

- Write access to the GitHub repository
- Membership of the `release` environment (required reviewer)
- Version bumped in `pyproject.toml` and committed to `main`
- `uv.lock` updated and committed (`uv lock`)

## Steps

### 1. Update the version

Edit the version in `pyproject.toml`:

```toml
[project]
version = "1.3.0"
```

Follow [semantic versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

### 2. Update the lockfile

```bash
uv lock
```

Commit both files:

```bash
git add pyproject.toml uv.lock
git commit -m "chore: bump version to 1.3.0"
git push
```

### 3. Dry run (recommended)

Before doing a real release, validate the full pipeline against TestPyPI:

1. Go to **Actions → Release → Run workflow**
2. Enter the version (e.g. `1.3.0`)
3. Leave **dry_run** checked (default)
4. Click **Run workflow**
5. Approve the release environment prompt when it appears

The workflow will:
- Validate the version against `pyproject.toml` and TestPyPI
- Run all CI checks (pyright, ruff, shellcheck, bandit, pip-audit, tests)
- Publish to TestPyPI
- Verify the package installs from TestPyPI by starting the server via `uvx` and confirming it responds to an MCP `tools/list` request

### 4. Publish to PyPI

Once the dry run passes:

1. Go to **Actions → Release → Run workflow**
2. Enter the version (e.g. `1.3.0`)
3. **Uncheck dry_run**
4. Click **Run workflow**
5. Approve the release environment prompt when it appears

The workflow will:
- Validate the version against `pyproject.toml` and PyPI
- Run all CI checks
- Publish to PyPI
- Verify the package installs from PyPI by starting the server via `uvx` and confirming it responds to an MCP `tools/list` request
- Create a `v1.3.0` git tag
- Auto-generate a changelog from commit history
- Create a GitHub Release with the changelog and build artifacts attached

## Secrets

| Secret | Location | Purpose |
|--------|----------|---------|
| `UV_PUBLISH_TOKEN` | `release` environment | PyPI API token |
| `TEST_UV_PUBLISH_TOKEN` | `release` environment | TestPyPI API token |

Both tokens are scoped to the `release` GitHub environment and are only accessible during release workflow runs.

## Checklist

- [ ] Version bumped in `pyproject.toml`
- [ ] `uv.lock` updated with `uv lock`
- [ ] Changes committed and pushed to `main`
- [ ] Dry run passes against TestPyPI
- [ ] Real release workflow passes
- [ ] GitHub Release created with correct tag and changelog
