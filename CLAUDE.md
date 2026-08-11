# Zephyrex RPG

Full-stack RPG campaign manager built on the Zephyrex framework.

## Structure

```
server/     Python backend — custom extensions for the Zephyrex server
client/     Next.js frontend — consumes the `zephyrex` npm package
```

## Server

The server is a consumer of the `zephyrex` Python package (PyPI). It defines three domain extensions:

- `genealogy` — family tree / lineage tracking
- `rpg_state` — character stats, inventory, abilities
- `rpg_log` — session logging and campaign history

```bash
cd server
pip install -e "../../server-framework[all]"
python app.py
```

## Client

The client is a consumer of the `zephyrex` npm package. It defines one client extension (`rpg`) that adds RPG-specific pages and navigation.

```bash
cd client
pnpm install
pnpm dev
```

## Testing

```bash
# Server tests
cd server && python -m pytest extensions/

# Client unit tests
cd client && pnpm test

# Full stack e2e
cd client && pnpm test:e2e
```
