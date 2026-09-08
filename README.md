# mcpscan

`mcpscan` is a passive security scanner for Model Context Protocol (MCP) servers. It connects to a server, reads its exposed tools/resources/prompts, and reports concrete risks without invoking tools or attempting exploitation.

## Quick start

The workspace already includes the Python 3.12 environment and dependencies. Run the deliberately flawed demo server through the scanner:

```bash
python -m mcpscan.cli scan "python -m mcpscan.demo_server" --transport stdio
```

Save the same report as JSON:

```bash
python -m mcpscan.cli scan "python -m mcpscan.demo_server" \
  --transport stdio --severity-threshold medium --output report.json
```

For an HTTP MCP endpoint:

```bash
python -m mcpscan.cli scan https://example.test/mcp --transport http \
  --auth-header Authorization --cors restricted --rate-limit-signal "100 req/min"
```

## Checks

- **Overprivileged tool** — broad shell, filesystem, or network capability without a narrowing parameter.
- **Injection-susceptible description** — imperative or formatting patterns that can steer an agent reading metadata.
- **Weak input validation** — structured inputs exposed as unconstrained strings.
- **Secret exposure** — credential and private-key patterns in metadata and schema defaults.
- **Unscoped remote exposure** — missing auth, permissive CORS, or missing rate-limit signal for HTTP targets.
- **Excessive tool surface** — a high number of agent-facing tools, flagged for human review.

## Development

```bash
pytest -q
python -m mcpscan.cli --help
```

The scanner is intentionally standalone and does not depend on the existing TypeScript services.