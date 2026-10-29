#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree is not clean. Commit or stash before syncing." >&2
  git status --short >&2
  exit 1
fi

git fetch upstream
git checkout dev
git merge --ff-only upstream/dev
git checkout our-release
git merge dev

echo
echo "Sync complete. If conflicts were reported, resolve them with FORK.md open."
echo "Then push:"
echo "  git push -u origin our-release"
