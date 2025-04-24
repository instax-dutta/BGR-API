#!/bin/bash

# Exit on error
set -e

# 1. Create or activate a virtual environment
if [ -d "venv" ]; then
    echo "Activating existing virtual environment..."
    source venv/bin/activate
else
    echo "Creating new virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# 2. Upgrade pip (recommended)
pip install --upgrade pip

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Start the application with Gunicorn
gunicorn app:app --bind 0.0.0.0:10000
