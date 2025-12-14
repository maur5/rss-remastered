#!/bin/bash
set -e

echo "=== rss-remastered Dev Container Setup ==="

# uv is now installed via devcontainer feature
export PATH="$HOME/.local/bin:$PATH"

# Set up symlinks for persistent user data
# These point to the mounted ~/.persist volume which contains sensitive data
echo "Setting up persistent user data symlinks..."

# Handle .claude
if [ -d ~/.claude ] && [ ! -L ~/.claude ]; then
  cp -rn ~/.claude/* ~/.persist/claude/ 2>/dev/null || true
  rm -rf ~/.claude
fi
ln -sfn ~/.persist/claude ~/.claude

# Handle .config (may exist as directory from base image)
if [ -d ~/.config ] && [ ! -L ~/.config ]; then
  echo "Moving existing .config to persist volume..."
  find ~/.config -mindepth 1 -maxdepth 1 -exec cp -rn {} ~/.persist/config/ \; 2>/dev/null || true
  rm -rf ~/.config
fi
ln -sfn ~/.persist/config ~/.config

# Handle bash history
mkdir -p ~/.persist/bash
ln -sf ~/.persist/bash/.bash_history ~/.bash_history

# Install Playwright system dependencies
# Using Playwright's built-in dependency installer (knows exactly what's needed)
echo "Installing Playwright browser dependencies..."
sudo env PATH="$PATH" npx playwright install-deps

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Install Playwright browsers
echo "Installing Playwright browsers..."
npx playwright install chromium firefox webkit

# Initialize backend project if it doesn't exist
if [ ! -d "backend/.venv" ]; then
    echo "Initializing backend project..."
    cd backend

    # Install dependencies using uv
    uv sync

    echo "Backend initialized with dependencies"
    cd ..
else
    echo "Backend already initialized, skipping..."
fi

# Create data directory if it doesn't exist
mkdir -p data

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Environment:"
echo "  Python: $(python3 --version)"
echo "  uv: $(uv --version)"
echo "  Node: $(node --version)"
echo "  Playwright: $(npx playwright --version)"
echo ""
echo "Available commands:"
echo "  npm run test:e2e        - Run Playwright E2E tests"
echo "  npm run test:e2e:ui     - Run tests with Playwright UI"
echo "  cd backend && pytest    - Run backend tests"
echo "  docker compose up       - Start the application"
echo ""
