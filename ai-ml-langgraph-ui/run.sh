#!/bin/bash

# AI/ML LangGraph UI - Quick Start Script

echo "🚀 AI/ML LangGraph UI - Quick Start"
echo "=================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed successfully"
else
    echo "✅ Dependencies already installed"
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "🔧 Creating environment configuration..."
    cp .env.example .env.local
    echo "✅ Created .env.local from template"
    echo "💡 You can edit .env.local to add your API keys"
fi

# Build the application
echo "🔨 Building application..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi

echo "✅ Build completed successfully"

# Start the development server
echo ""
echo "🎉 Starting AI/ML LangGraph UI..."
echo "=================================="
echo ""
echo "📱 Application will be available at: http://localhost:3000"
echo "🛠  Features available:"
echo "   • NLP Task Creation (Sentiment, Classification, Extraction, etc.)"
echo "   • Real-time Results Display"
echo "   • Performance Metrics Dashboard"
echo "   • ShadCN UI Components"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start development server
npm run dev