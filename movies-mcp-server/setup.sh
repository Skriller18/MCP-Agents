#!/bin/bash

# Movies MCP Server Setup Script

set -e

echo "🎬 Movies MCP Server Setup"
echo "=========================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "❌ Error: Python 3.10 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"
echo ""

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "✅ uv is installed"
    USE_UV=true
else
    echo "⚠️  uv not found, will use pip instead"
    USE_UV=false
fi

echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📦 Installing dependencies..."
echo ""

if [ "$USE_UV" = true ]; then
    # Using uv
    echo "Creating virtual environment with uv..."
    uv venv
    
    echo "Installing dependencies with uv..."
    source .venv/bin/activate
    uv pip install -e .
else
    # Using pip
    echo "Creating virtual environment with venv..."
    python3 -m venv .venv
    
    echo "Installing dependencies with pip..."
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -e .
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add the movies server to your mcp.json file (see CONFIGURATION.md)"
echo "2. Restart Cursor completely"
echo "3. Start asking for movies! (e.g., 'Get me some action movies')"
echo ""
echo "📚 For detailed configuration instructions, see:"
echo "   - CONFIGURATION.md (quick config reference)"
echo "   - ../MOVIES_MCP.md (full documentation)"
echo ""

