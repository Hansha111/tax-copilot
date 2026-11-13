# Shortcuts for common tasks. More targets (data, recon, ui, demo) are added as those tasks land.
PYTHON ?= python

.PHONY: install test clean

install:
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m pytest

clean:
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; shutil.rmtree('.pytest_cache', ignore_errors=True)"
