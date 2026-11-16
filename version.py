"""
Version metadata and release asset selection helpers for Algoo IDE.
"""

import re
import sys
from typing import Any, Dict, Optional, Sequence, Tuple

__version__ = "1.0.0"
APP_NAME = "Algoo"
ORG_NAME = "softsurgery"
GITHUB_REPO = "softsurgery/algoo"
GITHUB_RELEASES_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_RELEASES_URL = f"https://github.com/{GITHUB_REPO}/releases/latest"


def is_prerelease_version(v_str: str) -> bool:
    """Returns True if `v_str` represents a test or pre-release tag (e.g. 'v1.2.3-test', 'test-v1.2.3')."""
    cleaned = v_str.strip().lower()
    return cleaned.startswith("test-") or "-" in cleaned


def parse_version(v_str: str) -> Tuple[int, ...]:
    """Parses a semantic version string (e.g. 'v1.2.3') into a comparable tuple of ints."""
    cleaned = v_str.strip()
    if cleaned.lower().startswith("test-"):
        cleaned = cleaned[5:]
    cleaned = cleaned.lstrip("vV")
    core = cleaned.split("-", 1)[0].split("+", 1)[0]
    parts = re.findall(r"\d+", core)
    return tuple(int(p) for p in parts) if parts else (0,)


def is_newer_version(latest: str, current: str = __version__) -> bool:
    """Returns True if `latest` is a stable release strictly greater than `current`."""
    if is_prerelease_version(latest):
        return False
    return parse_version(latest) > parse_version(current)


def select_platform_asset(
    assets: Sequence[Dict[str, Any]],
    platform: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Selects the appropriate installer asset (.deb, .exe, .dmg) for the current OS."""
    plat = (platform or sys.platform).lower()
    if plat.startswith("linux"):
        ext = ".deb"
    elif plat.startswith("win"):
        ext = ".exe"
    elif plat == "darwin" or plat.startswith("mac"):
        ext = ".dmg"
    else:
        return None

    for asset in assets:
        name = str(asset.get("name", "")).lower()
        if name.endswith(ext):
            return asset
    return None
