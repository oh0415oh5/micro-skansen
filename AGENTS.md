# AGENTS.md

## Project status

`micro-skansen` is currently a **stub repository**. As of the initial commit, it contains only `README.md` with the project title. There is no application source code, dependency manifests (`package.json`, `requirements.txt`, etc.), Docker configuration, or test/lint scripts.

## Cursor Cloud specific instructions

### Services

| Service | Required? | Notes |
|---------|-----------|-------|
| Application server | N/A | No app exists yet |
| Database / cache | N/A | None configured |
| Docker Compose | N/A | No `docker-compose` files |

When application code is added, update this section with the services that must run for end-to-end development (for example: API, frontend dev server, Postgres).

### Dependency installation

There are **no project dependencies** to install today. The VM update script is a no-op until manifests are committed.

Once code lands, replace the update script with the appropriate install command for the stack (for example `pnpm install`, `pip install -r requirements.txt`, or `uv sync`).

### Lint / test / run

No lint, test, or dev-server commands are defined yet. Check `README.md`, `package.json` scripts, `Makefile`, or `CONTRIBUTING.md` after those files exist.

### VM tooling (pre-installed)

The cloud VM already provides common development runtimes:

- **Node.js** via nvm (`node`, `npm`, `pnpm`, `yarn`)
- **Python 3.12** (`python3`, `pip`)
- **Go 1.22**
- **Rust** (`rustc`, `cargo`)

Verify versions with `node -v`, `python3 --version`, `go version`, and `rustc --version`.

### Gotchas

- Do not assume a monorepo or Docker setup; none exists in the current tree.
- Only `main` exists on the remote; there are no feature branches with hidden code.
- Future agents should re-run full environment discovery after the first real application commit.
