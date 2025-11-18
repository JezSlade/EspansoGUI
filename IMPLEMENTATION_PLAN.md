# Phase 13: UX Refinements & Power User Features

## Filtered Feature List (Removed Complex/Workaround Items)

**REMOVED** (require Espanso core changes or complex workarounds):
- ❌ Persistent/global variables (needs Espanso core support)
- ❌ Emoji picker/search (requires external library)
- ❌ Clipboard history (requires OS clipboard monitoring)
- ❌ Global hotkey registration (OS-specific, security concerns)
- ❌ Non-modal picklist (complex UI paradigm shift)

**KEEPING** (clean implementations, high UX value):
- ✅ Multi-select checkbox fix (z-index bug)
- ✅ Tooltips everywhere (simple HTML title attributes)
- ✅ Search box/menu for expansions (#119, 190 👍)
- ✅ Advanced form fields - radio, checkbox, dropdown (#151, 130 👍)
- ✅ Image/file injection enhancements (#85, 115 👍)
- ✅ Shell command param helpers (#240, 105 👍)
- ✅ Date math/calculation helpers (80 👍)

---

## Implementation Plan (Optimized)

### Part 1: Quick Fixes (30 min)
**File**: `espanso_companion.html`

#### 1.1 Multi-select Checkbox Z-Index Fix
**Issue**: Clicking checkboxes triggers parent card click
**Fix**: Add `position: relative; z-index: 10;` to checkbox container + stop propagation

```javascript
// Find checkbox click handlers (around line 1420-1440)
// Add event.stopPropagation() to prevent parent click
```

#### 1.2 Add Tooltips Everywhere
**Add `title` attributes to all buttons and inputs**:
- Snippet editor fields (trigger, replace, label, delay, backend, etc.)
- All toolbar buttons (Save, New, Delete, Export, etc.)
- Search filters
- Navigation buttons

---

### Part 2: Searchable Snippet Menu (2 hours)
**Files**: `espanso_companion.html`, `espansogui.py`

#### 2.1 Add "Quick Insert" View
- New sidebar button: "Quick Insert"
- Modal overlay with large search box
- Live-filtered snippet list with triggers + labels
- Click to copy trigger to clipboard
- Shows replacement preview on hover

**Backend**: Use existing `list_snippets()` - no changes needed

**Frontend**:
```html
<!-- Add to views section -->
<div class="view" id="quick-insert-view">
    <h2>Quick Insert Snippet</h2>
    <input type="text" id="quick-search" placeholder="Search snippets by name, trigger, or label...">
    <div id="quick-results"></div>
</div>
```

---

### Part 3: Advanced Form Fields (3 hours)
**Files**: `espanso_companion.html`, `espansogui.py`

#### 3.1 Extend Form Builder
Add 3 new field types to existing form builder:
- **Radio button group**: `type: radio`, `choices: [...]`
- **Checkbox**: `type: checkbox`, `default: true/false`
- **Dropdown/Select**: `type: select`, `choices: [...]`

**Backend**: Extend `create_form_snippet()` to support new types
**Frontend**: Add field type selector with conditional UI for each type

---

### Part 4: Image/File Injection Enhancements (1 hour)
**Files**: `espanso_companion.html`

#### 4.1 Image Preview
- Show thumbnail preview when image path is set
- Add "Test Image" button to verify path exists
- Support drag-drop image files (get path)

#### 4.2 File Picker Enhancement
- Add "Insert File Path" variable type
- Use existing `pick_path_dialog()` API
- Generate `{{file_path}}` variable with path

---

### Part 5: Shell Command Helpers (2 hours)
**Files**: `espanso_companion.html`

#### 5.1 Shell Variable Builder Enhancement
Add "Shell Parameter Template" button:
- Pre-fill common patterns: `{{input}}`, `{{clipboard}}`, `{{date}}`
- Error handling template: `|| echo "Error"`
- Timeout template: `timeout 5s command`

#### 5.2 Shell Command Tester
- Add "Test Shell Command" button in variable modal
- Runs command locally and shows output
- Warning if command takes >2s or returns error

---

### Part 6: Date Math Helpers (1.5 hours)
**Files**: `espanso_companion.html`

#### 6.1 Date Variable Enhancements
Add "Date Calculator" button in date variable editor:
- Dropdown: Today, Tomorrow, Yesterday, Custom offset
- Offset input: "+7 days", "-1 week", "+1 month"
- Preview: Shows calculated date
- Generates: `{{date_offset}}` variable with format + offset

**Example output**:
```yaml
- type: date
  params:
    format: "%Y-%m-%d"
    offset_days: 7  # +7 days from today
```

---

## File Changes Summary

### `espanso_companion.html` (estimated +250 LOC)
1. Multi-select checkbox z-index fix (5 lines)
2. Tooltips on 40+ elements (40 lines)
3. Quick Insert view + search (60 lines)
4. Advanced form field types (70 lines)
5. Image preview + drag-drop (40 lines)
6. Shell param templates (20 lines)
7. Date calculator widget (15 lines)

### `espansogui.py` (estimated +30 LOC)
1. Extend `create_form_snippet()` for new field types (20 lines)
2. Add `test_shell_command()` API for testing (10 lines)

---

## Implementation Order (Optimized)

**Session 1 (1 hour)**: Quick wins
1. Multi-select checkbox fix
2. Add tooltips everywhere
3. Test both fixes

**Session 2 (2 hours)**: Search & Discovery
1. Quick Insert view
2. Live search integration
3. Copy-to-clipboard functionality

**Session 3 (3 hours)**: Forms Enhancement
1. Radio button field type
2. Checkbox field type
3. Dropdown/select field type
4. Update form builder UI

**Session 4 (2 hours)**: Media & Commands
1. Image preview + drag-drop
2. Shell param templates
3. Shell command tester

**Session 5 (1.5 hours)**: Date Helpers
1. Date offset calculator
2. Preview widget
3. Integration testing

---

## Total Effort

- **Development**: ~10 hours
- **Testing**: ~2 hours
- **Documentation**: ~1 hour
- **Total**: ~13 hours

All features are GUI-only enhancements that work within Espanso's existing capabilities. No core Espanso changes required, no workarounds needed.

---

## Success Criteria

- ✅ Multi-select works without triggering parent clicks
- ✅ All interactive elements have helpful tooltips
- ✅ Users can search and insert snippets without memorizing triggers
- ✅ Form builder supports radio, checkbox, dropdown fields
- ✅ Image paths show previews and support drag-drop
- ✅ Shell commands have param templates and testing
- ✅ Date variables support offset calculations with preview

---

## Regression Prevention Strategy

### Pre-Implementation Safeguards

1. **Create Backup Before Starting**
   ```bash
   cp webview_ui/espanso_companion.html webview_ui/espanso_companion.html.backup.phase13
   cp espansogui.py espansogui.py.backup.phase13
   git add -A && git commit -m "Pre-Phase 13 backup"
   ```

2. **Read Current Code First**
   - Must use Read tool on any file before editing
   - Verify existing structure before adding new code
   - Check for naming conflicts before adding IDs/classes

3. **Incremental Testing Protocol**
   - Test after EACH session (not at the end)
   - Launch app: `python espansogui.py`
   - Verify existing features still work
   - Only proceed if no regressions detected

### Implementation Safeguards

#### Session 1: Quick Fixes
**Regression Risks**:
- Z-index changes could affect modal/dropdown layering
- Tooltips could block clickable elements

**Prevention**:
- Use highly specific CSS selectors (e.g., `.snippet-card .checkbox-container`)
- Add `pointer-events: none` to tooltip overlays
- Test multi-select in all views (Snippet Library, Variable Library)
- Verify modals still appear on top

**Rollback**: If issues, remove added CSS lines and `title` attributes

#### Session 2: Quick Insert View
**Regression Risks**:
- New view could conflict with existing navigation
- Search could interfere with existing search boxes

**Prevention**:
- Add as NEW view, don't modify existing Snippet Library
- Use unique ID: `#quick-insert-view` (verify not already used)
- Copy existing search pattern, don't modify `renderSnippetList()`
- New sidebar button at bottom, don't reorder existing buttons

**Rollback**: Remove sidebar button, remove view div, remove switchView case

#### Session 3: Form Enhancements
**Regression Risks**:
- Modifying form builder could break existing form snippets
- New field types could cause errors when loading old forms

**Prevention**:
- Extend `create_form_snippet()`, don't replace it
- Add new field types to existing switch/if-else, don't rewrite
- Test loading existing form snippets after changes
- Backward compatibility: old forms must still load

**Testing Checklist**:
```javascript
// Test existing form snippet still works:
1. Load existing form snippet from base.yml
2. Edit and save form snippet
3. Create new text/choice/list form (existing types)
4. Verify Espanso still triggers forms correctly
```

**Rollback**: Remove new case statements for radio/checkbox/select

#### Session 4: Media & Commands
**Regression Risks**:
- Image preview could break if path is invalid
- Shell tester could hang on long-running commands
- Drag-drop could interfere with existing drag operations

**Prevention**:
- Wrap image loading in try-catch, show placeholder on error
- Add 5-second timeout to shell tester
- Use `ondrop` only on specific elements, not globally
- Test existing image path field still works without preview

**Testing Checklist**:
1. Existing image path input still saves correctly
2. Snippets without image paths load normally
3. Shell variables without tester still function
4. No new errors in console when loading app

**Rollback**: Remove preview div, remove drag handlers, remove test button

#### Session 5: Date Helpers
**Regression Risks**:
- Date calculator could generate invalid date formats
- Offset could break existing date variables

**Prevention**:
- Add calculator as optional enhancement, don't modify date variable editor
- Existing date variables must work without offsets
- Validate offset before applying (reject invalid input)
- Preview shows result before saving

**Testing Checklist**:
1. Create date variable without offset (existing behavior)
2. Existing date variables load correctly
3. Invalid offsets show error, don't crash app
4. Date format preserved when adding offset

**Rollback**: Remove offset calculator UI, remove offset params from YAML generation

---

## Testing Protocol (MANDATORY)

### After Each Session

1. **Syntax Check**
   ```bash
   python -m py_compile espansogui.py
   ```

2. **Launch Test**
   ```bash
   python espansogui.py
   # Verify app window opens
   # Check for console errors
   ```

3. **Core Feature Smoke Test** (5 minutes)
   - ✅ Dashboard loads and shows status
   - ✅ Snippet Library displays snippets
   - ✅ Create new snippet (trigger, replace, save)
   - ✅ Edit existing snippet
   - ✅ Variable modal opens and closes
   - ✅ Search/filter works
   - ✅ Espanso restart works
   - ✅ No JavaScript errors in console

4. **New Feature Test** (2 minutes)
   - ✅ New feature works as expected
   - ✅ No visual glitches
   - ✅ No performance degradation

5. **Git Checkpoint**
   ```bash
   git add -A
   git commit -m "Session X complete: [feature name] - tests passing"
   ```

### Regression Detection

If ANY existing feature breaks:
1. **STOP immediately** - Do not continue to next session
2. Document the regression in console/logs
3. Rollback to last commit: `git reset --hard HEAD~1`
4. Re-analyze the change that caused regression
5. Apply safer fix

### Final Verification (End of Phase 13)

Run all 31 snippets from base.yml:
```bash
python espansogui.py
# Load app
# Navigate to each view
# Verify all panels scrollable
# Test each new feature
# Export test logs
```

---

## Risk Assessment (Updated)

**Low Risk Features** (safe to implement):
- ✅ Tooltips (additive, no logic changes)
- ✅ Quick Insert view (new view, isolated)
- ✅ Image preview (optional enhancement)

**Medium Risk Features** (need careful testing):
- ⚠️ Multi-select z-index fix (could affect other z-index elements)
- ⚠️ Form field extensions (touches existing builder)
- ⚠️ Shell command tester (subprocess execution)

**Mitigation for Medium Risk**:
- Use CSS cascade carefully (don't use `!important`)
- Extend switch statements, don't replace them
- Add timeout + error handling to shell tester
- Test on multiple snippet files, not just base.yml

---

## Rollback Plan

### Per-Session Rollback
```bash
# Undo last session
git reset --hard HEAD~1

# Or undo specific file
git checkout HEAD~1 -- webview_ui/espanso_companion.html
```

### Complete Phase 13 Rollback
```bash
# Restore pre-Phase 13 state
git checkout HEAD~5  # Assuming 5 sessions
# Or restore from backup
cp webview_ui/espanso_companion.html.backup.phase13 webview_ui/espanso_companion.html
cp espansogui.py.backup.phase13 espansogui.py
```

### Partial Rollback (Keep Some Features)
If only one feature causes issues:
1. Identify problematic code section
2. Comment out that section only
3. Keep other features functional
4. Re-test to confirm issue resolved

---

## Success Criteria (No Regression)

**All existing features must pass**:
- ✅ All 11 completed phases still functional
- ✅ All 31 test snippets load correctly
- ✅ No new console errors
- ✅ No performance degradation (load time <2s)
- ✅ All existing keyboard shortcuts work
- ✅ Theme toggle preserves state
- ✅ Pagination still works
- ✅ Backup/restore functional
- ✅ Package manager loads

**New features must work**:
- ✅ Each Phase 13 feature independently functional
- ✅ No conflicts between new features
- ✅ Clean user experience

**Documentation updated**:
- ✅ test-log.md has all test results
- ✅ session.md documents all changes
- ✅ Rollback steps documented if needed
