# Espanso Companion Pro Overview

Espanso Companion Pro is a PyWebView desktop shell that exposes the `EspansoAPI` backend to an embedded HTML/JS dashboard. The backend handles Espanso CLI discovery, YAML parsing, snippet management, backups, and file-watcher driven telemetry.

## Current State (2025-11-15)

### Completed Features (Phases 1-4)
- ✅ **Phase 1**: Core infrastructure (path detection, CLI integration, YAML parsing, file watcher)
- ✅ **Phase 2**: Basic snippet management (CRUD, search, word boundaries, case propagation)
- ✅ **Phase 3**: Variable system basics (9 variable types, modal editor, global library)
- ✅ **Phase 4**: Path explorer & config tree (import graph, cycle detection, $CONFIG resolution)

### Application Structure
- PyWebView window loads `webview_ui/espanso_companion.html` with 6 main views:
  - Dashboard (connection status, metrics, service controls)
  - YAML Editor (base.yml editing with validation and backup)
  - Snippet IDE (create/edit/delete with live preview)
  - Snippet Library (searchable list of all snippets)
  - Variable Library (variable types and global variables)
  - Paths & Explorer (config tree, import graph, path overrides)

### Backend Architecture
- `EspansoAPI` class exposes 30+ methods to JavaScript
- ConfigLoader handles path discovery with environment and CLI fallbacks
- YamlProcessor parses and validates YAML files
- FileWatcher streams real-time file change events
- Automatic timestamped backups on every edit

### Data Flow
1. Initialization: Load preferences → Discover paths → Parse YAML → Populate cache
2. Dashboard: Cache is populated ONCE, reused for all subsequent requests
3. Edits: Validate → Backup → Write → Reload Espanso → Refresh cache
4. File changes: Watcher detects → Event logged → UI can refresh

## Current Status
- **Performance**: Fixed critical cache pollution bug (get_dashboard was re-parsing on every call)
- **Data safety**: User's base.yml restored from backup after data loss incident
- **Logging**: Added informative logging throughout initialization and critical paths
- **Stability**: Defensive null checks prevent UI errors with empty/missing data

## Next Steps (See context/ROADMAP.md)
- **Phase 5**: Enhanced snippet features (labels, enable/disable, backend selector, delay, images)
- **Phase 6**: Forms & regex (form builder, regex triggers with validation)
- **Phase 7**: App-specific configs (per-app overrides, filter rules)
- **Phase 8**: Enhanced variables (global vars, dependencies, fallbacks, syntax highlighting)

## Testing & Verification
- CLI verification scripts: `verify_fixes.py`, `test_gui_apis.py`
- Manual smoke testing required for each release
- Test output should be logged to `context/test-log.md`

## Documentation

**For Users:**
- `README.md` - Quick start guide and basic usage
- `feature_set.md` - Master TODO checklist (for agents)

**For Agents:**
- `feature_set.md` - **Master TODO list** with checkboxes for all features
- `context/ROADMAP.md` - 12-phase implementation roadmap with estimates
- `context/index.md` - Current state and architecture overview (this file)
- `context/session.md` - Session-by-session development log
- `context/decisions.md` - Architecture decisions and rationale
- `context/FIXES_2025-11-15.md` - Recent bug fixes and resolutions

**Agent Workflow:**
1. Check `feature_set.md` for unchecked items
2. Review `context/ROADMAP.md` for current phase priorities
3. Implement features according to phase plan
4. Mark items complete in `feature_set.md` with `[x]`
5. Update `context/session.md` with progress notes
6. Run tests and update documentation

```
/*
CHANGELOG
2025-02-14 Codex
- Documented the PyWebView + Snippet IDE state and next steps.
2025-11-15 Codex
- Updated with current status post-Phase 4 completion
- Added completed features list and next steps reference
- Documented data flow and recent performance/stability fixes
*/
```
