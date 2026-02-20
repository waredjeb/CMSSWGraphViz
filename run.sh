#!/bin/bash
# Quick start script for CMSSW Graph Visualization

set -e

echo "============================================================"
echo "CMSSW Module Dependency Graph Visualization"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python -c "import pydot; import networkx" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install -q -r preprocess/requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi
echo ""

# Check if bundle exists
if [ ! -f "data/bundle.json" ]; then
    echo "Bundle not found. Generating from input files..."
    echo ""
    python preprocess/build_bundle.py
    echo ""
fi

# Start server
echo ""
echo "Starting web server..."
echo "============================================================"
echo ""
python server.py
