#!/bin/bash
# Setup Node.js inside virtual environment for Tailwind CSS

echo "=== Setting up Node.js in Virtual Environment ==="
echo ""

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Error: Virtual environment not activated!"
    echo "Please activate your venv first:"
    echo "  source venv/bin/activate"
    exit 1
fi

echo "✓ Virtual environment detected: $VIRTUAL_ENV"
echo ""

# Step 1: Install nodeenv
echo "Step 1: Installing nodeenv..."
pip install nodeenv

if [ $? -ne 0 ]; then
    echo "❌ Failed to install nodeenv"
    exit 1
fi

echo "✓ nodeenv installed"
echo ""

# Step 2: Install Node.js LTS inside venv
echo "Step 2: Installing Node.js LTS in virtual environment..."
nodeenv -p --node=lts

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js"
    exit 1
fi

echo "✓ Node.js installed in venv"
echo ""

# Step 3: Verify installation
echo "Step 3: Verifying Node.js installation..."
which node
which npm
node --version
npm --version

echo ""
echo "✓ Node.js setup complete!"
echo ""

# Step 4: Install Tailwind dependencies
echo "Step 4: Installing Tailwind CSS dependencies..."
cd theme/static_src
npm install

echo ""
echo "✓ All dependencies installed!"
echo ""

# Step 5: Build CSS initially
echo "Step 5: Building initial CSS..."
npm run build

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Update config/settings/local.py with NPM path:"
echo "     NPM_BIN_PATH = '$VIRTUAL_ENV/bin/npm'"
echo ""
echo "  2. Start Tailwind development server:"
echo "     python manage.py tailwind start"
echo ""
echo "  3. Or start Django development server in another terminal:"
echo "     python manage.py runserver"
echo ""
