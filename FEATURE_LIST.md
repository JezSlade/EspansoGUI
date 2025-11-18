# Espanso Companion Pro – Shareable Feature List

Use this as the public-facing rundown when recruiting Reddit beta testers. Everything listed here ships in the current PyWebView build.

## Control & Visibility
- **Unified dashboard** with service controls (start/stop/restart), live snippet counts, config paths, and streaming connection steps.
- **Auto-refreshing telemetry**: Espanso logs and doctor diagnostics flow straight into dashboard preview cards and keep updating in the background.
- **Paths & Config Explorer** combines active path cards, overrides, environment/CLI breakdowns, and a browsable config/import tree.
- **Quick theme toggle** switches between light/dark presets with persistence, ARIA cues, and localized button text.
- **Storage relocation wizard** copies Espanso YAML/config folders and Companion backups to any directory while updating the CLI to load from the new path.

## Snippet Creation Suite
- **Snippet IDE**: Trigger + metadata editor (labels, enable/disable, backend, delay, boundaries, uppercase mode, image injection with preview/drag-drop).
- **Variable tooling**: Local variable modal with type-specific helpers, shell tester, date offset calculator, and inline insertion buttons.
- **Global variable browser** + IDE integration for reuse, editing, and promotion of globals.
- **Live previews** for snippet replacements, cursor markers, and metadata summaries so changes are instantly visible.
- **Bulk actions & pagination** for large libraries (50 per page) plus z-index-corrected checkboxes to avoid accidental navigation.

## Discovery & Libraries
- **Snippet Library** with advanced filters (file, enabled state, labels, has vars/form) and search summary counters.
- **Quick Insert palette** offering search-as-you-type cards, hover previews, and clipboard copy to drop triggers anywhere.
- **Variable Library** surfaces globals with context and jump-to-editor controls.

## Intelligent Automation
- **SnippetSense** background monitor (Windows/macOS/Linux) using pynput + psutil:
  - Configurable thresholds, idle pauses, and privacy-safe hashed storage (app whitelist/blacklist available on Windows).
  - Toast + panel suggestions (Accept/Reject/Never) limited to one-per-phrase, honoring handled hashes so repeats are ignored.
  - Accept flows auto-create snippets, load them inside the IDE for polishing, and refresh Espanso instantly.

## Advanced Authoring
- **Form & Regex builder**: Visual field designer (text, choice, list, radio, checkbox, select) plus regex tester with capture previews.
- **App-specific configs**: Wizards + templates (VS Code, Chrome, Slack, Terminal, Outlook) with filter_exec/filter_title helpers and explorer refreshes.
- **Import/Export** snippet packs (JSON/YAML) and Quick Templates for common snippets (email signatures, meeting notes, code comments, date, greeting).

## CLI & Maintenance
- **Logs viewer** with auto-scroll, manual refresh, and dashboard mirroring.
- **Doctor diagnostics** accessible from Diagnostics view or via auto refresh loops, with output captured in the dashboard preview for quick triage.
- **Package manager** (list/install/update/uninstall) with inline toasts and CLI output.
- **Match testing**, **backup/restore**, and **path overrides** wired to backend safeguards (timestamped backups, validations, restart hooks).

## Safety & Quality of Life
- **Auto backups** on every editor save plus manual backup/restore center with history, all pointing at your chosen Companion backup directory.
- **Keyboard shortcuts**: Ctrl/Cmd+K (search), Ctrl/Cmd+S (save), Ctrl/Cmd+N (new snippet), Esc (close modals/reset form).
- **Help view** carries the built-in manual mirroring README, making onboarding frictionless.
- **Resilient bootstrap** with retry logic, ready-state guard, automatic “Refresh Data” run post-initialization, and scheduled log/diagnostic refreshers.

## Platform Snapshot
- Built with **Python + PyWebView** so everything runs locally/offline.
- Cross-platform SnippetSense engine (pynput/psutil/ctypes); app-level filters currently require Windows APIs.
- Requirements pinned in `requirements.txt`; install + run via `pip install -r requirements.txt && python espansogui.py`.

Share this link/file directly or quote sections in your Reddit beta post to highlight the app’s breadth.

```
/*
CHANGELOG
2025-11-17 Codex
- Authored the public-facing feature list for Reddit beta outreach.
*/
```
