# Installation

Requires **Python 3.10+** for the CLI. Generated apps target **Python 3.11+**.

## From PyPI

```bash
pip install liteit
liteit --version
```

## From source (editable)

```bash
git clone https://github.com/mghorbani2357/liteit.git
cd liteit
pip install -e .
# with tests / docs:
pip install -e ".[test]"
pip install -e ".[docs]"
```

## Verify

```bash
liteit -h
liteit --version
```

After `pip install`, the `liteit` console script is installed into your Python **Scripts** directory. If the shell says `liteit` is not recognized:

- **Prefer a venv** (Scripts is added to `PATH` on activate):

  ```bash
  python -m venv .venv
  # Windows PowerShell:
  .\.venv\Scripts\Activate.ps1
  pip install -e .
  liteit --version
  ```

- **Microsoft Store Python on Windows:** user Scripts is often missing from `PATH`. Pip warns about this during install. Add that Scripts folder to your user `PATH`, then open a **new** terminal.

Fallback if the script is not on `PATH` yet: `python -m liteit`.

## Local documentation

```bash
pip install -e ".[docs]"
python -m mkdocs serve
```

Open http://127.0.0.1:8000/ (MkDocs default). Published docs: https://liteit.readthedocs.io/
