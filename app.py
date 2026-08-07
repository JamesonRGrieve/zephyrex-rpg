"""Zephyrex RPG — a consumer app built on ServerFramework.

Provides genealogy, RPG state tracking, and RPG logging extensions.
All infrastructure (auth, DB, REST, GraphQL, migrations) comes from
the framework; this project only provides the domain models.

    python app.py              # boot with uvicorn
    python -c "from app import create; create()"  # programmatic
"""
import os

os.environ.setdefault("APP_NAME", "Zephyrex RPG")
os.environ.setdefault("DATABASE_TYPE", "sqlite")
os.environ.setdefault("DATABASE_NAME", "zephyrex_rpg")
os.environ.setdefault("SEED_DATA", "true")
os.environ.setdefault("JWT_SECRET", "dev-only-change-in-production-32chars!")

from serverframework import run

EXTENSIONS = "genealogy,rpg_state,rpg_log"

if __name__ == "__main__":
    run(
        extensions=EXTENSIONS,
        extensions_path="./extensions",
        port=2000,
    )


def create():
    """Return a FastAPI app instance for testing or ASGI mounting."""
    from serverframework import instance, set_extensions_root

    set_extensions_root("./extensions")
    return instance(extensions=EXTENSIONS)
