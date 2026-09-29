# zephyrex-rpg

RPG campaign manager built on the Zephyrex framework: characters, family trees, factions, quests and session logs.

The framework supplies auth, the database layer, REST and GraphQL, and the admin UI. This repo only adds the RPG domain: three server extensions and one client extension.

Status: early alpha. The server data model is in place and tested. The client currently mounts a placeholder dashboard at `/rpg`.

## Layout

```
server/   FastAPI backend, a consumer of the zephyrex Python package
client/   Next.js frontend, a consumer of the zephyrex npm package
```

## Server extensions

| Extension   | Depends on                          | Provides |
|-------------|-------------------------------------|----------|
| `genealogy` | nothing                             | Persons and labelled relationships, family-tree algorithms, GEDCOM-importable |
| `rpg_state` | `genealogy`, `acl_rbac` (optional)  | Present campaign state: characters, factions, items, quests, locations, traits |
| `rpg_log`   | `rpg_state`                         | Event log: encounters, combat, dialogue, interactions, transactions |

`rpg_state` has no character table of its own. It widens `genealogy`'s person model, so every character is a person in the family tree. When `acl_rbac` is loaded it controls per-row visibility (GM-only NPCs, hidden quests), so `rpg_state` never stores a visibility flag itself.

## Requirements

- Python 3.11+
- Node.js and pnpm (client only)
- For the client: the framework packages checked out as siblings of this repo (`../client-framework`, `../auth`, `../zod2gql`, `../dynamic-form`). The client depends on them with `file:` paths.

## Running the server

```bash
cd server
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
python app.py
```

This installs the framework from GitHub. To work against a local framework checkout instead, run `pip install -e "../../server-framework[all]"` before the line above.

The API listens on port 2000. On first boot it creates a SQLite database and seeds it.

### Configuration

`app.py` sets development defaults. Anything already present in the environment takes precedence.

| Variable        | Default                                  |
|-----------------|------------------------------------------|
| `APP_NAME`      | `Zephyrex RPG`                           |
| `DATABASE_TYPE` | `sqlite`                                 |
| `DATABASE_NAME` | `zephyrex_rpg`                           |
| `SEED_DATA`     | `true`                                   |
| `JWT_SECRET`    | a fixed development value                |

Set a real `JWT_SECRET` for anything other than local development. Every other framework setting (database host, email, OAuth providers) works as it does in the framework.

## Running the client

```bash
cd client
pnpm install
pnpm dev
```

The client runs on port 1109 and talks to `http://localhost:2000`. Set `NEXT_PUBLIC_API_URI` to point it somewhere else.

## Tests

```bash
cd server
python -m pytest extensions/
```

Each extension keeps its tests next to the code (`BLL_*_test.py`, `EXT_*_test.py`).

## License

[AGPL-3.0-or-later](./server/LICENSE)
