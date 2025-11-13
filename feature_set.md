**Espanso Editor Config & Feature List**

**Directory & Path Handling**

* Auto-detect Espanso config directory (`~/.config/espanso`, `%APPDATA%\espanso`)
* Custom config path override via GUI
* Parse `ESPANSO_CONFIG_DIR`, `ESPANSO_PACKAGE_DIR`, `ESPANSO_RUNTIME_DIR`
* Validate Espanso installation (`shutil.which`)
* Integration with `espanso path` and `espanso start`

**Configuration Management**

* YAML treeview for `match/` and `config/` directories
* Imports parsing with cycle detection
* `$CONFIG` variable resolution
* Recursive include/import support

**Match System**

* Trigger/replace editor with treeview
* Word boundary toggles (`word`, `left_word`, `right_word`)
* Case propagation (`propagate_case`, `uppercase_style`)
* Labels and search terms
* Per-match enable/disable, backend/delay overrides
* Cursor position markers ($|$)
* Markdown/HTML/rich text preview
* Image insertion (`image_path`)
* Nested match references (`type: match`, `params`)

**Variable System**

* Local `vars` and global `global_vars`
* Dependency ordering and drag-reorder
* Injection highlighting with fallback values
* Variable types:

  * `str`, `date`, `random`, `choice`, `clipboard`, `echo`, `shell`, `script`, `form`, `match`, `global`

**Forms**

* Template layout (`form` / `layout`)
* Field types: `text`, `choice`, `list`
* Multiline and default values
* Choice/list values with trimming
* Preview simulation dialog

**Regex Triggers**

* Pattern-based match (`regex`)
* Named groups with auto vars
* Regex validation and substitution preview
* Buffer size overrides

**App-Specific Configs**

* `<app>.yml` creation with priority merge
* Filter rules (`filter_exec`, `filter_title`, `filter_class`, `filter_os`)
* Active config detection (`espanso status`)
* Per-app overrides


**CLI Integration**

* Daemon control (start/stop/reload)
* Status/path popups (`espanso status/path`)
* Log viewer (`espanso log --follow`)
* Runtime toggle commands
* Match management (`list`, `exec`, `search`)
* Package management (`list`, `update`, `install`, `uninstall`)
