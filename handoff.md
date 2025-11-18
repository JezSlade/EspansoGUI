# EspansoGUI – Handoff (2025-02-14)

## Overview
- PyWebView shell (`espansogui.py`) instantiates `EspansoAPI` and renders `webview_ui/espanso_companion.html` with three experiences: Dashboard, base YAML editor, and the newly completed Snippet & Variable IDE.
- The backend handles Espanso CLI discovery, path detection, YAML parsing, snippet CRUD, automatic backups, and global variable harvesting. All API methods are exposed directly to the webview via `window.pywebview.api`.
- Documentation (`README.md`, `SNIPPET_IDE_GUIDE.md`) now matches the shipped codebase; prior references to non-existent Streamlit or HTTP services were removed.

## Key Components

### `espansogui.py`
- Creates `EspansoAPI`, loads config paths, starts a watchdog, and registers graceful shutdown handlers.
- API surface:
  - Dashboard (`get_dashboard`, `refresh_files`) with connection steps + watcher events.
  - Settings/CLI helpers (`start_service`, `stop_service`, `restart_service`, `toggle_autostart`, package helpers).
  - YAML editor helpers (`get_base_yaml`, `save_base_yaml`) with validation + timezone-aware backups.
  - Snippet CRUD (`create_snippet`, `update_snippet`, `delete_snippet`, `get_snippet`) including duplicate protection and automatic reloads.
  - Variable helpers (`get_variable_types`, `get_global_variables`) used by the IDE’s modal + library.
  - Backup utility (`create_backup`) for ad-hoc snapshots.

### `webview_ui/espanso_companion.html`
- GitHub-dark UI with sidebar navigation.
- **Dashboard** – CLI status, snippet counts, connection diagnostics, service control buttons.
- **Base YAML Editor** – Large textarea, Save & Reload, auto status text.
- **Snippet & Variable IDE**
  - Editor pane with trigger fields, toggles, replacement text, and action buttons.
  - Variable builder list with Insert/Edit/Delete controls and a modal supporting every Espanso variable type.
  - Snippet list with search + live selection, refresh control, and file metadata.
  - Global variable cards (insertable) plus a Variable Toolkit grid describing available variable types.
  - Toast notifications for every action and inline status updates for saves/deletes.

## Context & Process
- `context/` directory established with `index`, `session`, `test-log`, `deploy-log`, and `decisions` notes per AGENTS.md.
- README and the Snippet IDE guide explain the actual workflow so future agents can ramp quickly.

## Testing
- `python verify_fixes.py` – Confirms CLI connectivity, path discovery, and API stand-up (requires `espanso` on PATH).
- `python test_gui_apis.py` – Calls every `EspansoAPI` method without launching the GUI, ensuring all endpoints resolve.
- Record any test runs in `context/test-log.md` with timestamps and outcomes.

## Next Steps
1. **Run verification scripts** once Espanso CLI is installed/configured locally; attach logs.
2. **Manual Smoke Test** – Launch the PyWebView app, create/update/delete snippets via the IDE, and confirm Espanso reloads without errors.
3. **Automation Ideas** – Add unit tests for snippet CRUD + variable serialization to guard future regressions.
4. **Packaging** – Consider bundling via `pyinstaller` or shipping stand-alone builds once the GUI is verified.

```
/*
CHANGELOG
2025-02-14 Codex
- Replaced outdated handoff content with the current PyWebView + Snippet IDE summary.
*/
```
