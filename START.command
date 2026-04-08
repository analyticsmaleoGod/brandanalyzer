#!/bin/bash

# ╔══════════════════════════════════════════╗
# ║  Brand Analyzer — Double-click to run!   ║
# ╚══════════════════════════════════════════╝

# Go to the script's directory
cd "$(dirname "$0")"

echo ""
echo "📊 Brand Analyzer — Starting up..."
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "   Download from: https://www.python.org/downloads/"
    echo ""
    echo "Press any key to close..."
    read -n 1
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install dependencies if needed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo ""
    echo "📦 First time setup — installing dependencies..."
    echo "   (this only happens once, may take 1-2 minutes)"
    echo ""
    pip3 install -r requirements.txt --quiet
    echo ""
    echo "✅ Dependencies installed!"
fi

echo ""
echo "🚀 Launching Brand Analyzer..."
echo "   Opening in your browser..."
echo ""
echo "   To stop: close this window or press Ctrl+C"
echo ""

# Run the app
python3 -m streamlit run app.py --server.headless=false
