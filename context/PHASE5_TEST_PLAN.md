# Phase 5 Integration Test Plan

**Date**: 2025-11-15
**Phase**: 5 - Enhanced Snippet Features
**Status**: Implementation complete, awaiting user verification

---

## Pre-Test Setup

1. **Application Status**: ✅ Running (31 snippets loaded)
2. **Config Path**: `C:\Users\jez.slade\AppData\Roaming\espanso`
3. **Match Path**: `C:\Users\jez.slade\AppData\Roaming\espanso\match`

---

## Test 1: Create Snippet with ALL New Fields

**Objective**: Verify all Phase 5 fields save and load correctly

**Steps**:
1. Open Snippet IDE view
2. Click "New Snippet"
3. Fill in ALL fields:
   - **Trigger**: `:testphase5`
   - **Label**: `Phase 5 Test Snippet`
   - **Enabled**: ✅ Checked
   - **Backend**: Select "Clipboard" from dropdown
   - **Delay**: Enter `100` (should increment by 10ms when using arrows)
   - **Replacement**: `This is a Phase 5 test with delay`
   - **Image Path**: Click "Browse..." button and select any image file
4. Click "Save Snippet"
5. Verify toast shows success message
6. Click on the snippet in the list to reload it
7. **Verify**: All fields retain their values exactly as entered

**Expected Results**:
- ✅ All fields persist correctly
- ✅ Browse button opens file dialog
- ✅ Backend dropdown shows "Clipboard"
- ✅ Delay shows 100
- ✅ Label displays in snippet card

---

## Test 2: Backend Field Validation

**Objective**: Verify backend field only accepts "Inject" or "Clipboard"

**Steps**:
1. Create new snippet with trigger `:testbackend`
2. Select "Clipboard" from Backend dropdown
3. Save snippet
4. Open base.yml in YAML Editor
5. **Verify**: `backend: Clipboard` appears in YAML (capitalized)
6. Change backend to "Inject" in GUI
7. Save and verify YAML shows `backend: Inject`
8. Change backend to "Auto" (empty value)
9. **Verify**: Backend field is removed from YAML

**Expected Results**:
- ✅ Only "Inject" or "Clipboard" saved to YAML
- ✅ Capitalization normalized correctly
- ✅ Empty/Auto removes backend field

---

## Test 3: Enabled/Disabled Toggle

**Objective**: Verify snippets can be disabled and won't trigger in Espanso

**Steps**:
1. Create snippet with trigger `:testdisabled`
2. Uncheck "Enabled" checkbox
3. Save snippet
4. Open base.yml in YAML Editor
5. **Verify**: `enabled: false` appears in the match
6. Restart Espanso via Dashboard
7. Type `:testdisabled` in a text editor
8. **Verify**: Snippet does NOT expand (disabled works)
9. Re-enable the snippet in GUI
10. Restart Espanso
11. Type `:testdisabled` again
12. **Verify**: Snippet now expands

**Expected Results**:
- ✅ Disabled snippets have `enabled: false` in YAML
- ✅ Disabled snippets do not trigger in Espanso
- ✅ Re-enabling snippets makes them work again

---

## Test 4: Delay Field Polish

**Objective**: Verify delay input has step increment and tooltip

**Steps**:
1. Edit any snippet
2. Click in the "Delay (ms)" field
3. Hover over field
4. **Verify**: Tooltip appears: "Add delay before expansion (useful for slow applications)"
5. Use up/down arrow keys
6. **Verify**: Value increments/decrements by 10ms steps
7. Enter value `250` manually
8. Save snippet
9. Open YAML Editor
10. **Verify**: `delay: 250` appears in match

**Expected Results**:
- ✅ Tooltip shows helpful text
- ✅ Arrow keys increment by 10
- ✅ Manual values save correctly

---

## Test 5: Image Path Browse Button

**Objective**: Verify Browse button opens file dialog and saves path

**Steps**:
1. Create new snippet with trigger `:testimgpath`
2. Click "Browse..." button next to Image Path field
3. **Verify**: File dialog opens
4. Select an image file (PNG, JPG, etc.)
5. **Verify**: File path populates in Image Path field
6. Save snippet
7. Open YAML Editor
8. **Verify**: `image_path: <selected path>` appears in match
9. Edit snippet again
10. **Verify**: Image path loads correctly from YAML

**Expected Results**:
- ✅ Browse button opens native file dialog
- ✅ Selected path populates input field
- ✅ Path saves to YAML correctly
- ✅ Path loads when editing snippet

---

## Test 6: Advanced Search and Filtering

**Objective**: Verify all filter controls work correctly

**Steps**:
1. Go to Snippet Library view
2. Type search term in search box
3. **Verify**: Snippets filter by trigger, label, or content
4. Check "Enabled only" filter
5. **Verify**: Disabled snippets are hidden
6. Enter text in "Label" filter
7. **Verify**: Only snippets with matching labels show
8. Select a file from "File" dropdown
9. **Verify**: Only snippets from that file show
10. Check "Has variables" filter
11. **Verify**: Only snippets with variables show
12. Check "Has forms" filter
13. **Verify**: Only snippets with forms show
14. Click "Clear Filters"
15. **Verify**: All filters reset, full list returns

**Expected Results**:
- ✅ Search box filters instantly
- ✅ All checkbox filters work correctly
- ✅ File dropdown filters by source file
- ✅ Clear Filters resets everything
- ✅ Multiple filters can combine (AND logic)

---

## Test 7: Snippet Library Label Display

**Objective**: Verify labels and disabled badges display correctly

**Steps**:
1. Create snippet with label "Important Snippet"
2. View in Snippet Library
3. **Verify**: Label displays above or near trigger
4. Create another snippet and disable it
5. View in Snippet Library
6. **Verify**: Disabled badge or styling indicates disabled state
7. **Verify**: Snippet card has reduced opacity or visual indicator

**Expected Results**:
- ✅ Labels display in snippet cards
- ✅ Disabled snippets have visual indicator
- ✅ Layout looks clean and readable

---

## Test 8: Regression Test - Existing Snippets

**Objective**: Verify existing snippets without new fields still work

**Steps**:
1. Find an existing snippet (created before Phase 5)
2. Edit it in Snippet IDE
3. Change ONLY the replacement text
4. Save snippet
5. **Verify**: No new fields added to YAML
6. **Verify**: Snippet still works in Espanso
7. Open YAML Editor
8. **Verify**: Match structure unchanged except replacement

**Expected Results**:
- ✅ Old snippets don't get new fields added automatically
- ✅ Editing old snippets doesn't break them
- ✅ YAML remains clean and minimal

---

## Test 9: YAML Validation

**Objective**: Verify all YAML output is valid and Espanso-compatible

**Steps**:
1. Create multiple snippets using all new fields
2. Open YAML Editor (base.yml)
3. Copy entire content
4. Paste into online YAML validator (yamllint.com)
5. **Verify**: No YAML syntax errors
6. **Verify**: All fields use correct types:
   - `label`: string
   - `enabled`: boolean (false)
   - `backend`: string (Inject/Clipboard)
   - `delay`: integer
   - `image_path`: string
7. Restart Espanso via CLI: `espanso restart`
8. Check for errors in Espanso log
9. **Verify**: No errors or warnings

**Expected Results**:
- ✅ YAML is syntactically valid
- ✅ Field types are correct
- ✅ Espanso accepts the YAML without errors

---

## Test 10: Backup System

**Objective**: Verify timestamped backups created on save

**Steps**:
1. Note the current time
2. Create and save a new snippet
3. Navigate to `~/.espanso_companion/editor_backups/`
4. **Verify**: New backup file exists with timestamp ≈ current time
5. Open backup file
6. **Verify**: Contains the saved snippet data
7. Edit and save again
8. **Verify**: Second backup created with newer timestamp

**Expected Results**:
- ✅ Backup created on every save
- ✅ Timestamped filenames
- ✅ Backup contains correct YAML content
- ✅ Multiple backups accumulate (not overwriting)

---

## Success Criteria Summary

Phase 5 is considered **COMPLETE** when:

- [x] All 12 implementation steps verified in code
- [ ] All 10 integration tests pass
- [ ] No regressions in existing functionality
- [ ] YAML output is valid and Espanso-compatible
- [ ] Backups created consistently
- [ ] User confirms all features work in live environment

---

## Test Results Log

**Tester**: _______________
**Date**: _______________

| Test | Status | Notes |
|------|--------|-------|
| Test 1: All Fields | ⬜ Pass / ⬜ Fail | |
| Test 2: Backend Validation | ⬜ Pass / ⬜ Fail | |
| Test 3: Enabled Toggle | ⬜ Pass / ⬜ Fail | |
| Test 4: Delay Polish | ⬜ Pass / ⬜ Fail | |
| Test 5: Image Browse | ⬜ Pass / ⬜ Fail | |
| Test 6: Search/Filter | ⬜ Pass / ⬜ Fail | |
| Test 7: Label Display | ⬜ Pass / ⬜ Fail | |
| Test 8: Regression | ⬜ Pass / ⬜ Fail | |
| Test 9: YAML Validation | ⬜ Pass / ⬜ Fail | |
| Test 10: Backups | ⬜ Pass / ⬜ Fail | |

**Overall Result**: ⬜ PASS / ⬜ FAIL

---

## Notes

- Application is currently running in background (Bash ID: 0b240d)
- 31 snippets loaded from existing configuration
- All code changes complete and ready for testing
- Per CLAUDE.md workflow: Do not mark Phase 5 complete until user confirms live testing

/*
CHANGELOG
2025-11-15 Codex
- Created comprehensive Phase 5 test plan with 10 integration tests
- Detailed step-by-step verification procedures for all new features
- Included success criteria and test results log template
*/
