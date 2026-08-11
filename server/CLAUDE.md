# Zephyrex RPG

Consumer project built on [ServerFramework](https://github.com/JamesonRGrieve/ServerFramework). Provides RPG domain extensions — the framework handles all infrastructure.

## Architecture

This is a **consumer project**, not a framework fork. It depends on `zephyrex` via pip and provides only domain-specific extensions:

- **genealogy** — person/family tree models for RPG characters
- **rpg_state** — character state, inventory, progression tracking
- **rpg_log** — session/event logging for RPG campaigns

## Commands

```bash
pip install -e ".[dev]"      # Install with dev deps (pulls zephyrex from git)
python app.py                # Boot the server on port 2000
pytest extensions/           # Run extension tests
```

## How it works

`app.py` calls `zephyrex.run(extensions="genealogy,rpg_state,rpg_log", extensions_path="./extensions")`. The framework:

1. Discovers `BLL_*.py` models in `./extensions/<name>/`
2. Auto-generates SQLAlchemy tables (via `create_all` fallback — no Alembic migrations needed for dev)
3. Auto-generates REST CRUD endpoints at `/v1/<resource>`
4. Auto-generates GraphQL schema
5. Provides core auth (User, Team, Role, Session) out of the box
