from pathlib import Path
import os


def get_latest_url(fn: Path) -> str:
    try:
        with open(fn, 'r') as f:
            return f.read().strip()
    except Exception:
        return ''


def set_latest_url(fn: Path, url):
    with open(fn, 'w') as f:
        f.write(url.strip())
