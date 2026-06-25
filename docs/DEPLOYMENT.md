# Deploying Home Assistant + Todotree

This guide explains exactly how paths interact between host and container, and how to configure the Todotree integration.
This only covers running from Docker. If you are using HAOS, shell into your system and just run `todotree init` to setup from scratch or git clone to the correct location. 

## Two Deployment Modes

### Mode A: XDG Default (simplest)

No `config.yaml` required. Todotree auto-discovers files at `$XDG_DATA_HOME/todotree`.
Inside the HA container (running as root): `/root/.local/share/todotree`.

Mount your host todotree folder directly to that path:
```yaml
volumes:
  - ./todotree:/root/.local/share/todotree
```

Your host `./todotree/` folder just needs `todo.txt` (and optionally `done.txt`, `recur.txt`, `stale.txt`). If you want git sync, add a minimal `config.yaml`:
```yaml
git:
  mode: full
```

### Mode B: Custom Path (explicit)

Mount anywhere and point the integration to it:
```yaml
volumes:
  - ./todotree:/data/todotree
```

Requires `config.yaml` in the folder with at least the `paths` section:
```yaml
git:
  mode: full
paths:
  folder: .
  todo_file: todo.txt
  done_file: done.txt
```

## Components and Paths

- Home Assistant container internal paths:
  - `/config` — Home Assistant configuration directory
  - `/root/.local/share/todotree` — XDG default todotree data (Mode A)
  - `/data/todotree` — Custom mount point (Mode B)

- Host paths (you choose):
  - `./ha-config` — Bind-mounted to `/config`
  - `./todotree` — Bind-mounted to either XDG path or custom path

## Docker Compose

See `docker-compose.yaml` in this folder. Key points:

- Mount Home Assistant config:
  - `./ha-config:/config`
- Mount Todotree folder:
  - Mode A (XDG): `./todotree:/root/.local/share/todotree`
  - Mode B (Custom): `./todotree:/data/todotree`
- Optional: mount SSH keys for git:
  - `~/.ssh:/root/.ssh:ro`

## Todotree Integration Configuration

In Home Assistant UI:

1. Go to Settings → Devices & Services → Integrations → Add integration → "Todotree".
2. Choose ONE of the following for "Data Path":
   - XDG default (simplest): leave empty, or enter `/root/.local/share/todotree`.
     - This uses Todotree's default at `$XDG_DATA_HOME/todotree` inside the container.
     - No `config.yaml` required. If present, it's used (e.g. to enable git mode).
   - Custom path (explicit): `/data/todotree` (directory) or `/data/todotree/config.yaml` (file).
     - Requires `config.yaml` in the directory when using explicit path mode.
3. Submit.

### How Relative Paths Resolve

- If your `config.yaml` uses relative paths (e.g., `paths.todo_file: "todo.txt"`), they resolve **relative to the working directory**:
  - XDG default: `/root/.local/share/todotree`
  - Custom path directory: `/data/todotree`
  - Custom path file: parent of `/data/todotree/config.yaml` → `/data/todotree`

### Git Full Sync

- Ensure the mounted folder is a valid git repository with `origin` configured.
- Configure `config.yaml` (only needed to enable git):

```yaml
git:
  mode: full    # disabled | local | full
  pull_delay: 1 # minutes between pulls
```

- The integration uses Todotree's Python API directly. When git mode is `full`:
  - Pulls occur automatically on operations (rate-limited to 1 minute).
  - File changes trigger commit and push.

### Verifying Git Access Inside Container

- SSH method (recommended):
  - Mount `~/.ssh` read-only to `/root/.ssh`.
  - Permissions: `~/.ssh` (700), private keys (600), known_hosts contains your git host.
- HTTPS method:
  - Pre-configure credentials in the repo or use a credentials helper inside the container.
- Check status:

```bash
docker compose exec homeassistant git -C /root/.local/share/todotree status
```

## Directory Preparation

```bash
mkdir -p ./ha-config/custom_components
mkdir -p ./todotree
# Copy or initialize your todotree repo into ./todotree
```

## Start Stack

```bash
docker compose up -d
```

Then add the integration in the UI and set the Data Path as described.
