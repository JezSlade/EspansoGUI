# Espanso Snippet IDE – User Guide

## Overview
The Snippet IDE inside `webview_ui/espanso_companion.html` provides a word-processor style workflow that combines snippet CRUD, variable management, and reusable global variables in a single PyWebView screen.

## Layout

- **Left Panel – Editor**
  - Trigger input with validation, plus `Word boundary` and `Propagate case` toggles.
  - Large replacement textarea (supports `$|$` cursor markers and `{{variable}}` placeholders).
  - Inline status text that reports save/update results.
  - Variable builder with a list of local variables and buttons to Insert/Edit/Delete each one.
- **Right Panel – Library**
  - Searchable snippet list (click to load for editing) with file + variable badges.
  - Global Variable Library showing every detected variable across your match files.
  - Variable Toolkit cards describing each Espanso variable type and its required parameters.

## Working With Snippets

1. **Create / New** – Click *New Snippet*, fill trigger + replacement, add variables, then *Save Snippet*.
2. **Update** – Select a snippet from the list, adjust fields, and *Save*; the IDE keeps track of the original trigger for you.
3. **Delete** – Load the snippet and click *Delete*; the app prompts before removing it from `base.yml`.
4. **Backups & Reloads** – Every write creates a timestamped backup inside your configured Companion backup directory (default `~/.espanso_companion/editor_backups/`) and triggers `espanso restart` so your changes are live immediately.

## Variable Builder & Modal

- Press **+ Add Variable** (or *Edit* on an existing one) to open the modal.
- Fields:
  - **Name** – Must match the `{{name}}` you plan to insert.
  - **Type** – Pick from Date/Time, Clipboard, Random Choice, Shell, Script, Echo Prompt, User Choice, Form, or Match Reference.
  - **Parameters** – Dynamically generated inputs per type:
    - Date: `format`, `offset` (seconds)
    - Random Choice: `choices` (one per line)
    - Shell: `cmd`, optional `shell` flag
    - Script: `args` (newline list)
    - Echo/Choice/Form/Match: prompts, values, field layout, or referenced trigger respectively
- Saving updates the local variable list; use *Insert* to drop `{{variable}}` at the current cursor position in the replacement field.

## Global Variable Library

- Automatically scans every snippet for variables (including those outside `base.yml`).
- Displays variable name, type, and the snippet where it was defined.
- Click *Insert* on any global variable to paste `{{name}}` into your active snippet.

## Tips

- Use the search bar to filter snippets by trigger or replacement text.
- Keep YAML valid – invalid snippets or malformed variable params will raise toast errors and prevent saves.
- Pair the IDE with the Dashboard’s Connection Steps when debugging CLI or watcher issues.

```
/*
CHANGELOG
2025-02-14 Codex
- Rewrote the guide to match the new in-app Snippet & Variable IDE.
*/
```
