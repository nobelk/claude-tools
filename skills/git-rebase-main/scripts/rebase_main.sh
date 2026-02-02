#!/bin/bash
# Rebase current branch onto main/master with latest updates
set -euo pipefail

# Ensure we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Get current branch name
CURRENT_BRANCH=$(git branch --show-current)
if [ -z "$CURRENT_BRANCH" ]; then
    echo "Error: Not on a branch (detached HEAD state)"
    exit 1
fi

# Detect default branch (main or master) by checking local then remote refs
DEFAULT_BRANCH=""
for ref in refs/heads/main refs/heads/master refs/remotes/origin/main refs/remotes/origin/master; do
    if git show-ref --verify --quiet "$ref"; then
        DEFAULT_BRANCH="${ref##*/}"
        break
    fi
done

if [ -z "$DEFAULT_BRANCH" ]; then
    echo "Error: Could not find a main or master branch (checked local and origin)"
    exit 1
fi

echo "Current branch: $CURRENT_BRANCH"
echo "Default branch: $DEFAULT_BRANCH"

# If already on the default branch, just pull latest
if [ "$CURRENT_BRANCH" = "$DEFAULT_BRANCH" ]; then
    echo "Already on $DEFAULT_BRANCH, pulling latest..."
    git pull --rebase origin "$DEFAULT_BRANCH"
    echo "✓ $DEFAULT_BRANCH is up to date"
    exit 0
fi

# Fetch latest default branch from origin
echo "Fetching latest from origin/$DEFAULT_BRANCH..."
git fetch origin "$DEFAULT_BRANCH"

# Rebase onto origin's default branch
# --autostash automatically stashes and restores uncommitted changes,
# including on failure, avoiding the pitfalls of manual stash management.
echo "Rebasing $CURRENT_BRANCH onto origin/$DEFAULT_BRANCH..."
if git rebase --autostash "origin/$DEFAULT_BRANCH"; then
    echo "✓ Successfully rebased $CURRENT_BRANCH onto $DEFAULT_BRANCH"
else
    echo ""
    echo "⚠ Rebase paused due to conflicts. To resolve:"
    echo "  1. Fix conflicts in the affected files"
    echo "  2. Stage them: git add <resolved-files>"
    echo "  3. Continue:   git rebase --continue"
    echo ""
    echo "  To abort and return to the previous state: git rebase --abort"
    exit 1
fi

echo "✓ Done! $CURRENT_BRANCH now includes all updates from $DEFAULT_BRANCH"
