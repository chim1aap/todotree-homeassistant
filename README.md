# Todotree Home Assistant Integration

[![hacs][hacsbadge]][hacs]

A custom Home Assistant integration for [Todotree](https://pypi.org/project/todotree/) — a todo.txt-based task manager with Git sync.

## Features

- **Todo entity**: Exposes your Todotree task list as a native Home Assistant `todo` entity.
- **Full CRUD**: Create, update (due date, description), and complete tasks through HA UI or automations.
- **Git full sync**: When Todotree is configured with `git.mode: full`, all changes automatically commit and push.
- **Local polling**: Tasks are refreshed every 5 minutes from local files (no cloud dependency).

## Requirements

- Home Assistant 2025.2+
- [Todotree](https://pypi.org/project/todotree/) installed and configured on the same machine
- A valid todotree data folder (typically `~/.local/share/todotree/` or `~/.config/todotree/`)
- **Git authentication must already be configured** in the container running Home Assistant (see below)

## Installation

### HACS (Recommended)

1. Add this repository as a custom repository in HACS.
2. Search for "Todotree" and install.
3. Restart Home Assistant.

### Manual

1. Copy `custom_components/todotree_homeassistant/` to your `config/custom_components/` folder.
2. Restart Home Assistant.

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for "Todotree".
3. Enter the path to your todotree data folder (e.g., `/root/.local/share/todotree`).
4. The integration validates the config and creates a `todo.todotree` entity.

## Supported Operations

| Operation | Description |
| --- | --- |
| Create item | Adds task to `todo.txt` with optional due date |
| Update item | Sets due date or appends description |
| Delete item | Marks task as done (moves to `done.txt`) |

## Git Sync

If your todotree `config.yaml` has `git.mode: full`:
- Every modification (add/complete/update) triggers `git commit && git push`.
- Task list refresh triggers `git pull` (rate-limited to once per minute).
- Multi-device sync works automatically.

### Prerequisites: Git Authentication in the Container

The todotree data folder must already be a working git repository with push/pull access configured **before** setting up this integration. The `data_path` you provide during configuration simply points to that location.

You must ensure:

1. **The git repo is cloned** into the container (e.g., `/data/todotree/` or `/config/todotree/`).
2. **Authentication is pre-configured** so that `git pull` and `git push` work without prompts. Common approaches:
   - SSH key with no passphrase mounted into the container
   - Git credential helper with a stored token
   - `.netrc` file with a personal access token
3. **Git user identity is set** (`user.name` and `user.email` in git config).

Example setup for an HA OS addon or Docker container:

```bash
# Inside the container:
git clone M9RaO7kRVeU0rcqKeYHbpa9c3vLYRZew24mrx5NCMWc=:youruser/todotree-data.git /data/todotree
cd /data/todotree
git config user.name "Home Assistant"
git config user.email "eRsVJAXNYBqcbIBZzVITbhA5jWuXGbdPNfm_PY_2bkU="
```

Then in the integration config flow, enter `/data/todotree` as the data path.

> **Note**: A future version may support cloning and configuring the repository directly from the UI.

## Development

```bash
# Clone with devcontainer
git clone <repo-url> && cd todotree-homeassistant
# Open in VS Code with devcontainer, or:
pip install -r requirements.txt
```

Run lint:
```bash
ruff check custom_components/ tests/
```

## License

MIT

[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg
