---
name: git-rebase-main
description: Rebase current git branch onto main/master with latest updates from origin. Use when the user wants to update their feature branch with changes from main or master, sync their branch with the default branch, pull and rebase main/master, or keep their branch up to date with the latest upstream changes.
---

# Git Rebase Main

Fetch the latest default branch (main or master) from origin and rebase the current branch onto it.

## Usage

Run the bundled script from the user's repository directory:

```bash
bash <skill_path>/scripts/rebase_main.sh
```

Replace `<skill_path>` with the absolute path to this skill's directory.

## Behavior

- Auto-detects whether the repo uses `main` or `master` (checks local branches first, then remote)
- If already on the default branch, pulls latest with rebase instead
- Uses `git rebase --autostash` to automatically stash and restore any uncommitted changes (safe even if rebase fails)
- Fetches from `origin` only — does not modify the local main/master branch

## When Rebase Conflicts Occur

Inform the user of the conflict and provide these steps:

1. Resolve conflicts in the affected files
2. `git add <resolved-files>`
3. `git rebase --continue`

To abort: `git rebase --abort` (autostash will restore uncommitted changes automatically)
