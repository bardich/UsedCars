#!/bin/bash

# Django Used Cars Marketplace - Virtual Environment Setup Script

set -e

echo "========================================="
echo "  AutoMaroc - Environment Setup"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"

# Create virtual environment
VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment already exists at ./$VENV_DIR${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf "$VENV_DIR"
        echo "Creating new virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi
else
    echo "Creating virtual environment at ./$VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing requirements from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "Installing Tailwind CSS dependencies..."
cd theme/static_src
if [ -f "package.json" ]; then
    if command -v npm &> /dev/null; then
        npm install
    else
        echo -e "${YELLOW}Warning: npm not found. Tailwind CSS dependencies not installed.${NC}"
        echo "Please install Node.js and npm, then run 'npm install' in theme/static_src/"
    fi
else
    echo -e "${YELLOW}Warning: package.json not found in theme/static_src/${NC}"
fi
cd ../..

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the development server:"
echo "  python manage.py runserver"
echo ""
echo "To start Tailwind CSS in watch mode:"
echo "  python manage.py tailwind start"
echo ""
echo "To set up the database (PostgreSQL must be running):"
echo "  python manage.py migrate"
echo ""
