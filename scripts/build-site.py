#!/usr/bin/env python3
"""Rebuild and validate every derived asset before rendering the static site."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ['PYTHONUTF8'] = '1'
for command in [
    ['scripts/build-classification.py', 'data/catalogue.json.gz'],
    ['scripts/build-search-index.py'],
    ['scripts/check-data.py'],
    ['scripts/check-docs.py'],
    ['-m', 'mkdocs', 'build', '--clean'],
    ['scripts/version-assets.py'],
    ['scripts/check-html.py'],
]:
    subprocess.run([sys.executable, *command], check=True)
