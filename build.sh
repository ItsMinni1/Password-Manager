#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Build the executable using PyInstaller
# --onefile: Create a single executable file
# --windowed: Do not open a console window (GUI only)
# --add-data: Include static files and templates
pyinstaller --name "PasswordManager" \
            --onefile \
            --windowed \
            --add-data "templates:templates" \
            --add-data "static:static" \
            app.py

echo "Build complete! You can find your executable in the 'dist' folder."
