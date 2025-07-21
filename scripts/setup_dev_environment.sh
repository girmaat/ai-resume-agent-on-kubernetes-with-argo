#!/bin/bash

# ------------------------------------------------------------------------------
# Script: setup_dev_environment.sh
# Purpose: Prepare the development environment for a new developer (e.g., dev2)
# Platform: Linux only (tested on Ubuntu/Debian, RHEL, Arch)
#
# This script:
#   - Sets up .venv
#   - Installs required packages
#   - Prompts for .env OPENAI_API_KEY
#   - Runs test scripts after each key step
#
# Usage:
#   bash scripts/setup_dev_environment.sh
#
# Requirements:
#   - Must be run from the project root
#   - Have your OpenAI API key ready (will be required interactively)
# ------------------------------------------------------------------------------

set -e

echo "================================================================"
echo "Setting up AI Resume Assistant development environment (Linux)"
echo "================================================================"

# STEP 0: Ensure OpenAI key is ready
echo
echo "[Prerequisite] You will need your OpenAI API key (sk-...) to continue."
read -p "Do you have your OpenAI API key ready? (yes/no): " CONFIRM_KEY

if [[ "$CONFIRM_KEY" != "yes" ]]; then
    echo "Please obtain your API key and re-run the script when ready."
    exit 1
fi

# STEP 1: Check for Python 3
echo
echo "[Step 1] Checking for Python 3..."
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is not installed."

    echo "To install Python 3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv"
    echo "  RHEL/Fedora:   sudo dnf install python3"
    echo "  Arch Linux:    sudo pacman -S python"
    exit 1
fi
echo "python3 found: $(python3 --version)"

# STEP 2: Create .venv
echo
echo "[Step 2] Creating virtual environment..."
python3 -m venv .venv
echo "Virtual environment created at .venv"

# STEP 3: Activate .venv
echo
echo "[Step 3] Activating virtual environment..."
source .venv/bin/activate
echo "Virtual environment activated"

# STEP 4: Install dependencies
echo
echo "[Step 4] Installing Python dependencies from requirements.txt..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt
echo "Packages installed"

# Run test: requirements import
echo
echo "[Test] Verifying package imports..."
python tests/1.test_requirements_import.py

# STEP 5: Configure .env file
echo
echo "[Step 5] Creating .env file for OpenAI API key..."
ENV_FILE=".env"

if [ -f "$ENV_FILE" ]; then
    echo ".env already exists."
else
    read -p "Enter your OpenAI API key (starts with sk-): " OPENAI_KEY

    while [[ -z "$OPENAI_KEY" || "$OPENAI_KEY" != sk-* ]]; do
        echo "A valid OpenAI key (starting with sk-) is required."
        read -p "Enter your OpenAI API key (starts with sk-): " OPENAI_KEY
    done

    echo "OPENAI_API_KEY=$OPENAI_KEY" > .env
    echo ".env file created with OPENAI_API_KEY"
fi

# Run test: .env loading
echo
echo "[Test] Verifying .env loading and API key presence..."
python tests/2.test_env_loading.py

# STEP 6: Verify me/summary.txt and me/gi.pdf
echo
echo "[Step 6] Checking dummy resume and summary files..."
if [[ ! -f me/summary.txt || ! -f me/gi.pdf ]]; then
    echo "Required files not found in 'me/'"
    echo "Make sure 'me/summary.txt' and 'me/gi.pdf' exist before proceeding."
    exit 1
fi
echo "Dummy resume and summary found."

# Run test: resume loading
echo
echo "[Test] Verifying summary and PDF resume loading..."
python tests/4.test_resume_loading.py

# Final confirmation
echo
echo "================================================================"
echo "All setup steps and test scripts completed successfully."
echo "You can now begin development inside the .venv environment."
echo "================================================================"
