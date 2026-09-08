# 🛡️ mcpscan

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

`mcpscan` is a **passive security scanner** for Model Context Protocol (MCP) servers. It connects to a server, reads its exposed tools, resources, and prompts, and reports concrete risks — **without invoking tools or attempting exploitation**.

🪟 Works on **Windows**, 🍎 **macOS**, 🐧 **Linux**, and 🤖 **Android** (via Termux or Python distributions).

> **Note:** `mcpscan` is a text-based CLI tool. It does **not** support image inputs or image processing. If you encounter an error like `Cannot read "image.png" (this model does not support image input)`, it means an image file was provided where a text/stdio command or HTTP endpoint was expected.

---

### 📁 Project structure

```
📁 mcpscan/
├── 📦 mcpscan/
│   ├── 🐍 __init__.py
│   ├── ⌨️  cli.py          # Typer CLI entry point
│   ├── 🔌 client.py       # MCP client abstraction (stdio / HTTP / SSE)
│   ├── 🔍 scanner.py      # Manifest scanner and scoring
│   ├── 📋 models.py       # Pydantic data models
│   ├── 🖼️  report.py       # Terminal and JSON report renderers
│   ├── 🎬 demo_server.py  # Deliberately vulnerable demo server
│   └── 📂 checks/         # Passive check implementations
│       ├── 🏗️  base.py
│       ├── 🛠️  _helpers.py
│       ├── 📊 excessive_surface.py
│       ├── 💉 injection_susceptible_description.py
│       ├── 🔓 overprivileged_tool.py
│       ├── 🔑 secret_exposure.py
│       ├── 🌐 unscoped_remote_exposure.py
│       └── 🔓 weak_input_validation.py
├── 🧪 tests/
│   ├── 🧪 test_checks.py
│   └── 🧪 test_models.py
├── ⚙️ pyproject.toml
└── 📖 README.md
```


## 🚀 Quick start

```bash
# 🚀 Quick start
python -m mcpscan.cli scan "python -m mcpscan.demo_server" --transport stdio
```

Save the same report as JSON:

```bash
# 💾 Save the same report as JSON
python -m mcpscan.cli scan "python -m mcpscan.demo_server" \
  --transport stdio --severity-threshold medium --output report.json
```

For an HTTP MCP endpoint:

```bash
# 🌐 For an HTTP MCP endpoint
python -m mcpscan.cli scan https://example.test/mcp --transport http \
  --auth-header Authorization --cors restricted --rate-limit-signal "100 req/min"
```

---

## 🎯 Supported agents and capabilities

`mcpscan` is designed to audit MCP servers that are consumed by AI agents such as:

- 🤖 **Claude Desktop** — local stdio servers and remote HTTP/SSE servers
- 🔌 **Custom MCP clients** — any client that exposes tools, resources, or prompts over the MCP protocol
- 🖥️ **IDE integrations** — servers bundled with development environments

The scanner introspects the server manifest (tools, resources, prompts, and server info) and evaluates each item against a library of **passive, non-destructive checks**. It never executes tool logic, sends network requests through a tool, or modifies server state.

---

## 🔍 Detection coverage by scope

| Scope | Checks |
|-------|--------|
| 🛠️ **Tools** | Overprivileged tool, injection-susceptible description, weak input validation, secret exposure |
| 📦 **Resources** | Secret exposure, injection-susceptible description |
| 💬 **Prompts** | Secret exposure, injection-susceptible description |
| 🌐 **Remote (HTTP/SSE)** | Unscoped remote exposure (auth, CORS, rate limiting) |
| 🌍 **Global** | Excessive tool surface |

---

## 🛡️ Scanner Capabilities

### 🔓 Overprivileged tool
Detects tools that imply broad capabilities — shell execution, filesystem mutation, or unrestricted network access — without narrowing parameters.

### 💉 Injection-susceptible description
Finds instruction-like text in metadata that may steer an AI agent: imperative commands, system prompt leakage, or XML-style instructions.

### 🔓 Weak input validation
Flags string parameters that accept structured values (paths, URLs, commands) without schema constraints such as `enum`, `pattern`, `format`, or length bounds.

### 🔑 Secret exposure
Searches manifest metadata and schema defaults for hardcoded credentials: AWS keys, live API tokens, Bearer tokens, passwords, and private keys.

### 🌐 Unscoped remote exposure
For HTTP targets, verifies that the operator declared authentication, CORS policy, and rate-limiting signals.

### 📊 Excessive tool surface
Warns when a server exposes a large number of tools, which increases the agent's attack surface and permission footprint.

---

## ⚙️ How It Works

1. 🔌 **Connect** — `mcpscan` launches or connects to the target MCP server using `stdio` or `streamable_http` / `sse`.
2. 🔍 **Introspect** — It calls `initialize`, then `list_tools`, `list_resources`, and `list_prompts` to build a complete manifest.
3. 🧠 **Analyze** — Each check runs against the manifest **without invoking any tool logic**.
4. 📊 **Report** — Findings are aggregated, scored, and rendered in the terminal or written as JSON.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  MCP Target │────▶│   mcpscan    │────▶│   Checks    │────▶│   Report     │
│  (stdio/http)│     │   Scanner    │     │  (passive)  │     │  (JSON/TTY)  │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
```

---

## 🖥️ CLI Parameters

```
Usage: mcpscan scan [OPTIONS] TARGET

Arguments:
  TARGET   stdio command or HTTP/SSE endpoint to inspect.

Options:
  -t, --transport [stdio|http]   Connection transport.  [default: stdio]
  -o, --output PATH              Write the full report as JSON.
  --severity-threshold [info|low|medium|high|critical]
                                 Only show findings at or above this level.
                                 [default: info]
  --checks CHECK_ID            Comma-separated check IDs to run.
  --list-checks                Print available check IDs and exit.
  -h, --help                   Show this message and exit.
```

### 📟 stdio-only options
| Flag | Description |
|------|-------------|
| `--cwd PATH` | Working directory for a stdio server process. |

### 🌐 HTTP-only options
| Flag | Description |
|------|-------------|
| `--auth-header TEXT` | Declared remote auth header name, for exposure checks. |
| `--cors TEXT` | Declared CORS policy signal, e.g. `restricted` or `*`. |
| `--rate-limit-signal TEXT` | Documented rate limit signal for an HTTP target. |

---

## 💡 Examples

Scan a local stdio server with default checks:

```bash
python -m mcpscan.cli scan "python -m mcpscan.demo_server" --transport stdio
```

Run only high-severity checks against a remote endpoint:

```bash
python -m mcpscan.cli scan https://example.test/mcp \
  --transport http \
  --severity-threshold high \
  --auth-header Authorization \
  --cors restricted \
  --rate-limit-signal "100 req/min" \
  --output report.json
```

List all available checks:

```bash
python -m mcpscan.cli list-checks
```

Run a subset of checks:

```bash
python -m mcpscan.cli scan target --checks secret-exposure,overprivileged-tool
```

---

## 🎬 Demo

The repository ships with a deliberately vulnerable demo server that triggers multiple planted flaws:

```bash
python -m mcpscan.cli scan "python -m mcpscan.demo_server" --transport stdio
```

Expected findings:
- 🟠 `overprivileged-tool` — broad filesystem write
- 🟠 `injection-susceptible-description` — imperative prompt injection
- 🟡 `weak-input-validation` — unconstrained path and content parameters
- 🔴 `secret-exposure` — hardcoded API key in description

---

## 🏗️ MVC Architecture

`mcpscan` follows a lightweight **Model-View-Controller** pattern to keep concerns separated:

| Layer | 🎯 Responsibility | 📁 Key files |
|-------|-------------------|--------------|
| **📦 Model** | Data structures and schemas | `mcpscan/models.py` |
| **🖼️ View** | Output formatting | `mcpscan/report.py` |
| **🎮 Controller** | Orchestration and routing | `mcpscan/cli.py`, `mcpscan/scanner.py`, `mcpscan/client.py` |

### 📦 Model
Defines the core data shapes: `MCPManifest`, `Finding`, `ScanReport`, and severity enums. All models use Pydantic for validation and serialization.

### 🖼️ View
Renders results for different audiences:
- **Terminal view** (`render_terminal`) — Rich-powered tables and panels
- **JSON view** (`write_json`) — Machine-readable reports for CI pipelines

### 🎮 Controller
Coordinates the scan flow:
- **CLI controller** (`cli.py`) — parses arguments, instantiates the client, triggers scans
- **Scanner controller** (`scanner.py`) — iterates checks, filters by severity, computes risk score
- **Client controller** (`client.py`) — manages stdio / HTTP / SSE connections and introspection

---

## 🛠️ Development Setup

```bash
# 📥 Clone the repository
git clone https://github.com/Gethubsathvik/MCP-Security-Scanner.git
cd MCP-Security-Scanner

# 🐍 Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 📦 Install dependencies
pip install -e .

# 🧪 Run tests
pytest -q

# 🎬 Run the scanner against the demo server
python -m mcpscan.cli scan "python -m mcpscan.demo_server" --transport stdio
```
---
## 📚 Documentation

### 📋 Models
- ✅ `Check` — a single check, with severity and description
- 📄 `Report` — a collection of checks, with risk score and metadata
