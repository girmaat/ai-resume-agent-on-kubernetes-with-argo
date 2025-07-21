# ------------------------------------------------------------------------------
# File: scripts/global/setup_debugger.py
# Purpose: Automatically generate .vscode/launch.json for Python debugging
#          with .env support. Reusable across any Python project.
#
# How to Run:
#   python scripts/global/setup_debugger.py
#
# Expected Output:
#   .vscode/launch.json is created (if missing), ready for Cursor/VSCode debug.
# ------------------------------------------------------------------------------

import os
import json

def main():
    # Determine the project root relative to this script
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    vscode_dir = os.path.join(project_root, ".vscode")
    launch_path = os.path.join(vscode_dir, "launch.json")

    # Create .vscode directory if it doesn't exist
    if not os.path.exists(vscode_dir):
        os.makedirs(vscode_dir)

    # Default launch config using the open file as the program
    default_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Debug Single Script",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "envFile": "${workspaceFolder}/.env",
                "console": "integratedTerminal"
            }
        ]
    }

    if os.path.exists(launch_path):
        print(f"launch.json already exists at {launch_path}. No changes made.")
    else:
        with open(launch_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
        print(f"Debugger config written to {launch_path}")

if __name__ == "__main__":
    main()
