# Deploying Home Assistant + Todotree

This guide explains exactly how paths interact between host and container, and how to configure the Todotree integration.

## Components and Paths

- Home Assistant container internal paths:
  - `/config` — Home Assistant configuration directory
  - `/data/todotree` — Mounted Todotree data directory (your todo repo + files)

- Host paths (you choose):
  - `./ha-config` — Bind-mounted to `/config`
  - `./todotree` — Bind-mounted to `/data/todotree`

Update these to your own absolute paths if preferred.

## Docker Compose

See `docker-compose.yaml` in this folder. Key points:

- Mount Home Assistant config:
  - `./ha-config:/config`
- Mount Todotree folder:
  - `./todotree:/data/todotree`
- Optional: mount SSH keys for git:
  - `~/.ssh:/root/.ssh:ro`

## Todotree Integration Configuration

In Home Assistant UI:

1. Go to Settings → Devices & Services → Integrations → Add integration → "Todotree".
2. Set "Data Path" to either:
   - `/data/todotree` (directory) — integration looks for `config.yaml` inside and treats it as the working directory.
   - `/data/todotree/config.yaml` (absolute file) — integration uses this file and treats its parent as the working directory.
3. Submit.

### How Relative Paths Resolve

- If your `config.yaml` uses relative paths (e.g., `paths.todo_file: "todo.txt"`), they resolve **relative to the working directory**:
  - Directory mode: `/data/todotree`
  - File mode: parent of `/data/todotree/config.yaml` → `/data/todotree`

### Git Full Sync

- Ensure `/data/todotree` is a valid git repository with `origin` configured.
- Configure `config.yaml`:

```yaml
git:
  mode: full    # disabled | local | full
  pull_delay: 1 # minutes between pulls
paths:
  folder: .
  todo_file: todo.txt
  done_file: done.txt
  recur_file: recur.txt
  stale_file: stale.txt
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
docker compose exec homeassistant git -C /data/todotree status
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
