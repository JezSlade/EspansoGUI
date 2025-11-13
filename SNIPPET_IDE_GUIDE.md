# Espanso Snippet IDE - User Guide

## Overview
The Espanso Snippet IDE provides an intuitive, word processor-like interface for creating and editing Espanso snippets with full variable support.

## Features

### 1. Snippet IDE View
Navigate to the **Snippet IDE** from the sidebar to access the full editor.

#### Left Panel - Snippet Editor
- **Trigger Field**: The text you'll type to trigger the snippet (e.g., `:email`)
- **Word Boundary**: Check this to only expand when trigger is a complete word
- **Propagate Case**: Check this to match the case of your trigger when expanding
- **Replacement Text**: The large text area where you write what the snippet will expand to

#### Replacement Text Tips:
- Use `{{variable_name}}` to insert variables
- Use `$|$` to mark where your cursor should land after expansion
- Multi-line text is fully supported
- Syntax highlighting shows variables in blue

### 2. Variable Builder

#### Adding Variables
1. Click **"+ Add Variable"** button
2. Enter a variable name (e.g., `mydate`, `username`)
3. Select a variable type from the grid
4. Fill in type-specific parameters
5. Click **Save Variable**

#### Variable Types

**📅 Date/Time**
- **Format**: strftime format string (e.g., `%Y-%m-%d`, `%I:%M %p`)
- **Offset**: Seconds to add/subtract (86400 = 1 day)
- Example: `{{today}}` with format `%Y-%m-%d`

**📋 Clipboard**
- Inserts the current clipboard content
- No parameters needed
- Example: `{{clipboard}}` for pasting

**🎲 Random Choice**
- **Choices**: Enter options (one per line)
- Randomly selects one option each time
- Example: `{{greeting}}` from ["Hi!", "Hello!", "Hey!"]

**💻 Shell Command**
- **Command**: Shell command to run
- Output is inserted into snippet
- Example: `{{ip}}` with cmd `curl -s ipinfo.io/ip`

**📜 Script**
- **Args**: Script path and arguments (one per line)
- First line is the executable/interpreter
- Example: `["python3", "%CONFIG%/scripts/greeting.py"]`

**💬 Echo (Prompt)**
- Prompts user for input when triggered
- No parameters needed
- Example: `{{name}}` will ask user to type their name

**🎯 User Choice**
- **Values**: Options to choose from (one per line)
- Shows a selection dialog when triggered
- Example: `{{priority}}` from ["High", "Medium", "Low"]

**📝 Form Input**
- Advanced: Creates a multi-field form
- **Fields**: Define form structure
- See Espanso docs for field syntax

**🔗 Match Reference**
- References another snippet
- **Trigger**: The trigger of the snippet to reference

#### Managing Variables
- **Insert**: Adds `{{variable_name}}` to your cursor position in the replacement text
- **Edit**: Modify variable configuration
- **Delete**: Remove variable from snippet

### 3. Snippet List Sidebar

#### Browsing Snippets
- All your snippets appear in the right sidebar
- **Search box**: Filter snippets by trigger or content
- Click any snippet to load it for editing
- Active snippet is highlighted in blue

### 4. Snippet Operations

#### Creating a New Snippet
1. Click **"New Snippet"** button (or start fresh)
2. Enter a trigger (e.g., `:sig`)
3. Enter replacement text (e.g., your email signature)
4. Add variables if needed
5. Click **"Save Snippet"**

#### Editing an Existing Snippet
1. Click the snippet in the sidebar
2. Modify trigger, replacement, or variables
3. Click **"Save Snippet"** to update

#### Deleting a Snippet
1. Load the snippet for editing
2. Click **"Delete"** button (red)
3. Confirm deletion
4. Snippet is removed and Espanso reloads

### 5. Common Workflows

#### Email Signature Snippet
```
Trigger: :sig
Replacement:
Best regards,
{{name}}
{{title}}
{{company}}

Variables:
- name (echo): prompts for your name
- title (echo): prompts for your title
- company (echo): prompts for company
```

#### Date Snippets
```
Trigger: :date
Replacement: {{mydate}}

Variables:
- mydate (date):
  - format: %m/%d/%Y
  - offset: 0
```

#### Meeting Notes Template
```
Trigger: :meeting
Replacement:
# Meeting Notes - {{date}}

**Attendees**: $|$

**Agenda**:
-

**Action Items**:
-

Variables:
- date (date):
  - format: %Y-%m-%d
  - offset: 0
```

#### Code Snippet with Shell
```
Trigger: :uuid
Replacement: {{uuid}}

Variables:
- uuid (shell):
  - cmd: uuidgen | tr '[:upper:]' '[:lower:]'
```

## Tips & Tricks

1. **Variable Ordering**: Variables are evaluated in the order they appear
2. **Cursor Positioning**: Use `$|$` to control where cursor lands after expansion
3. **Multi-line**: Press Enter in replacement text for multi-line snippets
4. **Search**: Use the search box to quickly find snippets by trigger or content
5. **Backup**: Every save creates an automatic backup in `~/.espanso_companion/editor_backups/`
6. **Live Testing**: Changes take effect immediately after clicking "Save Snippet"

## Keyboard Shortcuts (in replacement textarea)
- `Ctrl+A`: Select all
- `Ctrl+Z`: Undo
- `Ctrl+Y`: Redo
- `Tab`: Insert tab character
- `Ctrl+Enter`: Could be mapped to save (future enhancement)

## Troubleshooting

**Snippet not triggering after save?**
- Check Espanso service is running (Dashboard view)
- Verify trigger doesn't conflict with existing snippets
- Check "word" boundary setting if trigger has special characters

**Variable not working?**
- Verify variable name matches `{{name}}` in replacement text exactly
- Check parameter syntax for the variable type
- Review Espanso logs if shell/script variables fail

**Changes not saving?**
- Check for YAML syntax errors in toast notifications
- Ensure base.yml file is not read-only
- Verify Espanso config path in Dashboard

## Advanced Features

### Variable Dependencies
If one variable depends on another, list them in order:
```
Variables:
1. firstName (echo)
2. lastName (echo)
3. fullName (echo with default: "{{firstName}} {{lastName}}")
```

### Complex Forms
Use the Form variable type for multi-field input dialogs. See Espanso documentation for complete form syntax.

### Script Integration
Store scripts in `%CONFIG%/scripts/` directory:
- Windows: `C:\Users\<user>\.config\espanso\scripts\`
- Use `%CONFIG%` variable in script paths
- Make scripts executable on Unix systems

## Support
- Espanso Documentation: https://espanso.org/docs/
- Variable Reference: https://espanso.org/docs/matches/variables/
- This project: See README.md for support info
