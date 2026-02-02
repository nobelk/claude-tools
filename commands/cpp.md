# Commit and Push to Main
# Usage: Stage, commit, and push all changes to origin main

## Pre-flight Checks
Execute these checks in parallel before proceeding:
1. Run `git status` to identify all changed and untracked files
2. Run `git diff` to review unstaged changes
3. Run `git diff --staged` to review any already staged changes
4. Run `git log -3 --oneline` to see recent commit message style

## Validation
- Verify there are actual changes to commit (abort if working tree is clean)
- Check for any untracked files that should be ignored (node_modules, .env, etc.)
- Ensure no sensitive files are being committed (.env, credentials, API keys)

## Execution Steps

### Step 1: Stage Changes
```bash
git add .
```

### Step 2: Generate Commit Message
Based on the staged changes, generate a descriptive commit message that:
- Starts with a type prefix: feat|fix|docs|style|refactor|test|chore
- Uses imperative mood ("Add feature" not "Added feature")
- Summarizes the change in under 72 characters
- Optionally includes a body explaining the "why"

### Step 3: Create Commit
```bash
git commit -m "<type>: <description>

<optional body explaining why>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 4: Push to Remote
```bash
git push origin main
```

### Step 5: Verify
Run `git status` to confirm the push was successful and working tree is clean.

## Error Handling
- If push fails due to remote changes, run `git pull --rebase origin main` first
- If conflicts occur, report them and stop execution
- If pre-commit hooks fail, report the failure and do not proceed

## Output
Report:
- Number of files changed
- Insertions/deletions summary
- Commit hash
- Push status (success/failure)
