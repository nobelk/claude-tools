---
name: keybindings-help
description: >
  Use when the user wants to customize keyboard shortcuts, rebind keys, add chord bindings,
  or modify ~/.claude/keybindings.json. Examples: "rebind ctrl+s", "add a chord shortcut",
  "change the submit key", "customize keybindings".
---

# Keybindings Help

Help users customize Claude Code keyboard shortcuts by editing `~/.claude/keybindings.json`.

## Workflow

1. **Understand the request** — determine what the user wants to customize (rebind, unbind, add chord, etc.)
2. **Check existing config** — read `~/.claude/keybindings.json` if it exists
3. **Provide guidance or make edits** — explain the format or directly edit the file as requested
4. **Validate** — ensure the JSON is valid and warn about conflicts

## Configuration File

Keybindings are configured in `~/.claude/keybindings.json`. The user can run `/keybindings` in Claude Code to create or open this file.

### File Structure

```json
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

**Top-level fields:**
- `$schema` — Optional JSON Schema URL for editor autocompletion
- `$docs` — Optional documentation URL
- `bindings` — Array of binding blocks organized by context

## Key Syntax

### Modifiers

Use `+` to combine modifiers with keys:

| Modifier | Aliases |
|----------|---------|
| `ctrl` | `control` |
| `alt` | `opt`, `option` |
| `shift` | — |
| `meta` | `cmd`, `command` |

### Examples

```
ctrl+k          # Control + K
shift+tab       # Shift + Tab
meta+p          # Command/Meta + P
ctrl+shift+c    # Control + Shift + C
```

### Special Keys

`escape`/`esc`, `enter`/`return`, `tab`, `space`, `up`, `down`, `left`, `right`, `backspace`, `delete`

### Uppercase Letters

- Standalone uppercase implies Shift: `K` = `shift+k`
- With modifiers, uppercase does NOT imply Shift: `ctrl+K` = `ctrl+k`

## Chord Bindings

Chords are multi-key sequences separated by spaces. Press the first combo, release, then press the second:

```json
{
  "context": "Chat",
  "bindings": {
    "ctrl+k ctrl+s": "chat:stash"
  }
}
```

## Available Contexts

| Context | Purpose |
|---------|---------|
| `Global` | Applies everywhere in the app |
| `Chat` | Main chat input area |
| `Autocomplete` | Autocomplete menu is open |
| `Settings` | Settings menu |
| `Confirmation` | Permission and confirmation dialogs |
| `Tabs` | Tab navigation components |
| `Help` | Help menu is visible |
| `Transcript` | Transcript viewer |
| `HistorySearch` | History search mode (Ctrl+R) |
| `Task` | Background task is running |
| `ThemePicker` | Theme picker dialog |
| `Attachments` | Image/attachment bar navigation |
| `Footer` | Footer indicator navigation |
| `MessageSelector` | Rewind dialog message selection |
| `DiffDialog` | Diff viewer navigation |
| `ModelPicker` | Model picker effort level |
| `Select` | Generic select/list components |
| `Plugin` | Plugin dialog |

## Available Actions

### Global Context (app:*)

| Action | Default | Description |
|--------|---------|-------------|
| `app:interrupt` | Ctrl+C | Cancel current operation |
| `app:exit` | Ctrl+D | Exit Claude Code |
| `app:toggleTodos` | Ctrl+T | Toggle task list visibility |
| `app:toggleTranscript` | Ctrl+O | Toggle verbose transcript |

### Chat Context (chat:*)

| Action | Default | Description |
|--------|---------|-------------|
| `chat:submit` | Enter | Submit message |
| `chat:cancel` | Escape | Cancel current input |
| `chat:cycleMode` | Shift+Tab | Cycle permission modes |
| `chat:modelPicker` | Meta+P | Open model picker |
| `chat:thinkingToggle` | Meta+T | Toggle extended thinking |
| `chat:undo` | Ctrl+_ | Undo last action |
| `chat:externalEditor` | Ctrl+G | Open in external editor |
| `chat:stash` | Ctrl+S | Stash current prompt |
| `chat:imagePaste` | Ctrl+V | Paste image |

### History Actions (history:*)

| Action | Default | Description |
|--------|---------|-------------|
| `history:search` | Ctrl+R | Open history search |
| `history:previous` | Up | Previous history item |
| `history:next` | Down | Next history item |

### Autocomplete Context (autocomplete:*)

| Action | Default | Description |
|--------|---------|-------------|
| `autocomplete:accept` | Tab | Accept suggestion |
| `autocomplete:dismiss` | Escape | Dismiss menu |
| `autocomplete:previous` | Up | Previous suggestion |
| `autocomplete:next` | Down | Next suggestion |

### Confirmation Context (confirm:*)

| Action | Default | Description |
|--------|---------|-------------|
| `confirm:yes` | Y, Enter | Confirm action |
| `confirm:no` | N, Escape | Decline action |
| `confirm:previous` | Up | Previous option |
| `confirm:next` | Down | Next option |
| `confirm:nextField` | Tab | Next field |
| `confirm:cycleMode` | Shift+Tab | Cycle permission modes |
| `confirm:toggleExplanation` | Ctrl+E | Toggle permission explanation |

### Transcript Context (transcript:*)

| Action | Default | Description |
|--------|---------|-------------|
| `transcript:toggleShowAll` | Ctrl+E | Toggle show all content |
| `transcript:exit` | Ctrl+C, Escape | Exit transcript view |

### History Search Context (historySearch:*)

| Action | Default | Description |
|--------|---------|-------------|
| `historySearch:next` | Ctrl+R | Next match |
| `historySearch:accept` | Escape, Tab | Accept selection |
| `historySearch:cancel` | Ctrl+C | Cancel search |
| `historySearch:execute` | Enter | Execute selected command |

### Task Context (task:*)

| Action | Default | Description |
|--------|---------|-------------|
| `task:background` | Ctrl+B | Background current task |

### Tabs Context (tabs:*)

| Action | Default | Description |
|--------|---------|-------------|
| `tabs:next` | Tab, Right | Next tab |
| `tabs:previous` | Shift+Tab, Left | Previous tab |

### Attachments Context (attachments:*)

| Action | Default | Description |
|--------|---------|-------------|
| `attachments:next` | Right | Next attachment |
| `attachments:previous` | Left | Previous attachment |
| `attachments:remove` | Backspace, Delete | Remove selected |
| `attachments:exit` | Down, Escape | Exit attachment bar |

### Footer Context (footer:*)

| Action | Default | Description |
|--------|---------|-------------|
| `footer:next` | Right | Next footer item |
| `footer:previous` | Left | Previous footer item |
| `footer:openSelected` | Enter | Open selected item |
| `footer:clearSelection` | Escape | Clear selection |

### Message Selector Context (messageSelector:*)

| Action | Default | Description |
|--------|---------|-------------|
| `messageSelector:up` | Up, K | Move up |
| `messageSelector:down` | Down, J | Move down |
| `messageSelector:top` | Ctrl+Up, Shift+K | Jump to top |
| `messageSelector:bottom` | Ctrl+Down, Shift+J | Jump to bottom |
| `messageSelector:select` | Enter | Select message |

### Diff Context (diff:*)

| Action | Default | Description |
|--------|---------|-------------|
| `diff:dismiss` | Escape | Close diff viewer |
| `diff:previousSource` | Left | Previous diff source |
| `diff:nextSource` | Right | Next diff source |
| `diff:previousFile` | Up | Previous file |
| `diff:nextFile` | Down | Next file |
| `diff:viewDetails` | Enter | View diff details |

### Model Picker Context (modelPicker:*)

| Action | Default | Description |
|--------|---------|-------------|
| `modelPicker:decreaseEffort` | Left | Decrease effort level |
| `modelPicker:increaseEffort` | Right | Increase effort level |

### Select Context (select:*)

| Action | Default | Description |
|--------|---------|-------------|
| `select:next` | Down, J, Ctrl+N | Next option |
| `select:previous` | Up, K, Ctrl+P | Previous option |
| `select:accept` | Enter | Accept selection |
| `select:cancel` | Escape | Cancel selection |

### Plugin Context (plugin:*)

| Action | Default | Description |
|--------|---------|-------------|
| `plugin:toggle` | Space | Toggle plugin selection |
| `plugin:install` | I | Install selected plugins |

### Settings Context (settings:*)

| Action | Default | Description |
|--------|---------|-------------|
| `settings:search` | / | Enter search mode |
| `settings:retry` | R | Retry loading usage data |

### Help Context (help:*)

| Action | Default | Description |
|--------|---------|-------------|
| `help:dismiss` | Escape | Close help menu |

### Theme Picker Context (theme:*)

| Action | Default | Description |
|--------|---------|-------------|
| `theme:toggleSyntaxHighlighting` | Ctrl+T | Toggle syntax highlighting |

## Unbinding Shortcuts

Set an action to `null` to unbind a default shortcut:

```json
{
  "context": "Chat",
  "bindings": {
    "ctrl+s": null
  }
}
```

## Reserved Shortcuts

These shortcuts cannot be rebound:
- `Ctrl+C` — Hardcoded interrupt/cancel
- `Ctrl+D` — Hardcoded exit

## Terminal Multiplexer Conflicts

Be aware of these potential conflicts:

| Shortcut | Conflict |
|----------|----------|
| `Ctrl+B` | tmux prefix (press twice to send) |
| `Ctrl+A` | GNU screen prefix |
| `Ctrl+Z` | Unix process suspend (SIGTSTP) |

## Vim Mode Interaction

When vim mode is enabled (`/vim`):
- **Vim mode** handles text input level (cursor movement, modes, motions)
- **Keybindings** handle component level actions (toggle todos, submit, etc.)
- Escape in vim mode switches INSERT to NORMAL mode (does NOT trigger `chat:cancel`)
- Most Ctrl+key shortcuts pass through vim mode to the keybinding system

## Common Customizations

### Change Submit Key to Ctrl+Enter

```json
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "enter": null,
        "ctrl+enter": "chat:submit"
      }
    }
  ]
}
```

### Add VS Code-Style Chord for External Editor

```json
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+k ctrl+e": "chat:externalEditor"
      }
    }
  ]
}
```

### Rebind Model Picker to Ctrl+M

```json
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+m": "chat:modelPicker"
      }
    }
  ]
}
```

## Validation

Claude Code validates keybindings and warns about:
- Parse errors (invalid JSON or structure)
- Invalid context names
- Reserved shortcut conflicts
- Terminal multiplexer conflicts
- Duplicate bindings in the same context

Run `/doctor` to see any keybinding warnings.

## Notes

- Changes to `keybindings.json` are automatically detected and applied without restarting Claude Code
- Use the JSON schema for autocompletion in your editor
- When helping users, always read their existing config first to avoid overwriting customizations
