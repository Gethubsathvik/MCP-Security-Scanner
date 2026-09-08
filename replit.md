# mcpscan

`mcpscan` is a standalone Python CLI that passively audits MCP server metadata and emits Rich terminal and JSON security reports.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string
- `python -m mcpscan.cli scan "python -m mcpscan.demo_server" --transport stdio` — scan the intentionally vulnerable local demo
- `python -m pytest -q` — run the Python unit suite

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)
- Scanner: Python 3.12, official `mcp` SDK, Typer, Rich, Pydantic v2, pytest

## Where things live

- `mcpscan/client.py` — official SDK transport wrappers and read-only introspection
- `mcpscan/checks/` — six passive finding checks
- `mcpscan/scanner.py` — orchestration, threshold filtering, and scoring
- `mcpscan/report.py` — Rich terminal renderer and JSON export
- `mcpscan/demo_server.py` — deliberately vulnerable local MCP server
- `tests/` — check and serialization coverage

## Architecture decisions

- The scanner never calls MCP tools, resources, or prompts; it only initializes a session and lists metadata.
- The Python scanner stays standalone from the existing TypeScript API artifact so it can evolve into a CLI package independently.
- Remote exposure findings are based on explicit CLI-declared signals because auth, CORS, and rate-limit policy are not reliably inferable from a passive MCP manifest.

## Product

Users can scan local stdio MCP servers or HTTP endpoints, filter findings by severity, see a scored Rich report, and export the full report as JSON.

## User preferences

The MVP is intentionally passive and standalone; active exploitation, dashboards, databases, and continuous monitoring are deferred.

## Gotchas

- Use `python -m mcpscan.cli` or the installed `mcpscan` entry point; the existing TypeScript workflows are unrelated to the CLI.
- The demo server intentionally contains a fake credential pattern for scanner regression coverage; never use it as a real secret.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
