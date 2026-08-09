"""Test configuration for zephyrex-rpg consumer project.

Sets up the extensions path so test imports like
``from zephyrex.extensions.rpg_state.BLL_RPGState import ...``
resolve to the local ``./extensions/`` directory.
"""

import os
import sys
from pathlib import Path

# Add the extensions directory to sys.path so Python can find
# the consumer extensions under the zephyrex.extensions namespace.
_project_root = Path(__file__).resolve().parent
_extensions_dir = _project_root / "extensions"

# Make extensions importable as zephyrex.extensions.* by extending
# the zephyrex.extensions namespace package path.
os.environ.setdefault("EXTENSIONS_PATH", str(_extensions_dir))
os.environ.setdefault("DATABASE_TYPE", "sqlite")
os.environ.setdefault("DATABASE_NAME", "test_rpg")
os.environ.setdefault("JWT_SECRET", "test-jwt-secret-32-bytes-or-more-aaaaaa")
os.environ.setdefault("SEED_DATA", "true")

import zephyrex.extensions  # noqa: E402

if str(_extensions_dir) not in zephyrex.extensions.__path__:
    zephyrex.extensions.__path__ = [str(_extensions_dir)] + list(zephyrex.extensions.__path__)
