# Espanso IDE

A comprehensive GUI IDE and dashboard for creating, managing, and configuring Espanso snippets.

## Features

- **Visual Snippet Builder** - Create snippets with forms, variables, and all Espanso features
- **Template Library** - Pre-built templates for common snippet types
- **Live Testing** - Test your snippets before saving
- **Analytics Dashboard** - View statistics and usage patterns
- **Backup & Restore** - Complete backup system with history
- **Import/Export** - Share snippets between machines
- **Dark/Light Mode** - Toggle themes with persistent preference
- **Keyboard Shortcuts** - Full keyboard navigation

## Quick Start

### Prerequisites

- Python 3.10+
- Espanso installed and configured
- Edge WebView2 runtime (Windows) or a compatible WebKit/Chromium engine

### Installation

1. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch the WebView-driven desktop shell:
   ```bash
   python pywebview_app.py
   ```

3. The workspace auto-detects your Espanso config, enables the watcher, and surfaces protobuf analytics/features directly from the embedded HTML (inspired by the Figma layout and the previous `espanso-ide.html` experience).

You can also inspect `webview_ui/espanso_companion.html` to iterate on the hero cards, feature catalog, and snippet tiles that expose every item in `feature_set.md`.

## Streamlit Companion Pro

This repository also ships a Python/Streamlit experience that mirrors the requested architecture:

- **Core modules** for configuration discovery, recursive YAML parsing, CLI integration, file watching, and variable metadata.
- **Pages** for Dashboard, Snippet Library, Word Processor IDE, Package Manager, and Analytics that surface real-time watcher data, CLI responses, and inline variable tooling.
- **Feature catalog** content, inline workflows, and success criteria are surfaced inside the Streamlit UI so the app can be validated against the original spec.

### Running the Streamlit App

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch the Streamlit UI:
   ```bash
   streamlit run streamlit_app.py
   ```

3. Connect to your local Espanso configuration and explore the Dashboard, snippet editor, and analytics panels.

## How It Works

The IDE uses a local HTTP server to access your Espanso configuration files without browser security restrictions. The server runs on `localhost:3850` and provides a REST API for reading and writing Espanso YAML files.

## Feature Set

**Espanso Editor Config & Feature List**

### Directory & Path Handling

* Auto-detect Espanso config directory (`~/.config/espanso`, `%APPDATA%\espanso`)
* Custom config path override via GUI
* Parse `ESPANSO_CONFIG_DIR`, `ESPANSO_PACKAGE_DIR`, `ESPANSO_RUNTIME_DIR`
* Validate Espanso installation (`shutil.which`)
* Integration with `espanso path` and `espanso start`

### Configuration Management

* YAML treeview for `match/` and `config/` directories
* Imports parsing with cycle detection
* `$CONFIG` variable resolution
* Recursive include/import support

### Match System

* Trigger/replace editor with treeview
* Word boundary toggles (`word`, `left_word`, `right_word`)
* Case propagation (`propagate_case`, `uppercase_style`)
* Labels and search terms
* Per-match enable/disable, backend/delay overrides
* Cursor position markers ($|$)
* Markdown/HTML/rich text preview
* Image insertion (`image_path`)
* Nested match references (`type: match`, `params`)

### Variable System

* Local `vars` and global `global_vars`
* Dependency ordering and drag-reorder
* Injection highlighting with fallback values
* Variable types include `str`, `date`, `random`, `choice`, `clipboard`, `echo`, `shell`, `script`, `form`, `match`, `global`

### Forms

* Template layout (`form` / `layout`)
* Field types: `text`, `choice`, `list`
* Multiline and default values
* Choice/list values with trimming
* Preview simulation dialog

### Regex Triggers

* Pattern-based match (`regex`)
* Named groups with auto vars
* Regex validation and substitution preview
* Buffer size overrides

### App-Specific Configs

* `<app>.yml` creation with priority merge
* Filter rules (`filter_exec`, `filter_title`, `filter_class`, `filter_os`)
* Active config detection (`espanso status`)
* Per-app overrides

### CLI Integration

* Daemon control (start/stop/reload)
* Status/path popups (`espanso status/path`)
* Log viewer (`espanso log --follow`)
* Runtime toggle commands
* Match management (`list`, `exec`, `search`)
* Package management (`list`, `update`, `install`, `uninstall`)

### Server API Endpoints

- `GET /api/status` - Check Espanso installation status
- `GET /api/snippets` - Load all snippets
- `POST /api/snippets` - Save a new snippet
- `DELETE /api/snippets/:filename` - Delete a snippet
- `GET /api/config` - Load Espanso config
- `POST /api/config` - Save Espanso config
- `POST /api/restart` - Restart Espanso

## Espanso Directory Locations

- **Linux**: `~/.config/espanso`
- **macOS**: `~/Library/Application Support/espanso`
- **Windows**: `%APPDATA%\espanso`

## Keyboard Shortcuts

- `Ctrl+N` - New snippet
- `Ctrl+S` - Save snippet
- `Ctrl+F` - Search snippets
- `Ctrl+P` - Show preview
- `?` - Show help

## Troubleshooting

### Server won't start

Make sure Node.js is installed:
\`\`\`bash
node --version
\`\`\`

### Can't find Espanso directory

Run this command to find your Espanso path:
\`\`\`bash
espanso path
\`\`\`

### Snippets not loading

Make sure Espanso is installed:
\`\`\`bash
espanso --version
\`\`\`

## License

MIT
