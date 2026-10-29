#!/usr/bin/env bash
# Fetch and build Fast Downward (the external C++ baseline, D17) at a pinned release.
# Usage: scripts/setup_fast_downward.sh   -> third_party/downward (gitignored)
set -euo pipefail
TAG=release-24.06.1
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/third_party/downward"
if [ ! -d "$DEST" ]; then
  git clone --depth 1 --branch "$TAG" https://github.com/aibasel/downward.git "$DEST"
fi
cd "$DEST"
test "$(git describe --tags)" = "$TAG"
python3 build.py release -j 8
