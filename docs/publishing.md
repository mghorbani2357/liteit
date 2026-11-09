# Publish

The distribution name on PyPI is **`liteit`** (`pip install liteit`). The import package and console script are also `liteit`.

Versions are set in `pyproject.toml` (`[project].version`). Tag releases to match.

## Tag and push

```bash
git tag -a v0.1.0 -m "liteit 0.1.0"
git push origin v0.1.0
```

Tags matching `v*` trigger [`.github/workflows/publish.yml`](https://github.com/mghorbani2357/liteit/blob/master/.github/workflows/publish.yml). The workflow builds with Python 3.12 and uploads to PyPI automatically.

After a tag push, confirm:

- PyPI: https://pypi.org/project/liteit/
- Docs: rebuild **latest** from `master` on Read the Docs (Versions → ensure `latest` tracks `master`)

## GitHub configuration

Only one secret is required (repository **Settings → Secrets and variables → Actions**):

| Name | Purpose |
|------|---------|
| `PYPI_API_TOKEN` | PyPI API token (`pypi-...`) |

## Local build check

```bash
pip install -U build
python -m build
```

Confirm the wheel contains `liteit/templates/project/` (including `env.example.j2` and `gitignore`) so `liteit init` works from the installed package.
