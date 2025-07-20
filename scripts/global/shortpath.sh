#!/bin/bash
# ------------------------------------------------------------------------------
# Script: shortpath.sh
# Purpose: Automatically jump into the root project directory (based on script location)
#          and launch a subshell with a shortened prompt (just project folder name).
#
# Usage (Linux/macOS/Git Bash):
#   ./scripts/global/shortpath.sh
#
# Behavior:
#   - Locates the project root by going two directories up from this script
#   - Enters the project folder
#   - Displays a short terminal prompt: (.venv) ai-resume-agent-on-kubernetes-with-argo>
#   - Works in Linux/macOS or Git Bash on Windows
#
# Notes:
#   - If you rename/move the script, update the relative ".." logic
#   - Not for CMD or PowerShell — they need their own versions
# ------------------------------------------------------------------------------

# Resolve the directory of this script, even if symlinked
SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || realpath "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

# Go two levels up: from scripts/global/ → project root
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Get project name (last part of path)
SHORTNAME="$(basename "$PROJECT_ROOT")"

# Move to project root
cd "$PROJECT_ROOT" || {
  echo "❌ Could not cd into $PROJECT_ROOT"
  exit 1
}

# Launch shell with custom prompt
echo "✅ Entered project: $SHORTNAME"
PS1="(.venv) $SHORTNAME> " bash --norc
