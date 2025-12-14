#!/bin/bash
# on-create.sh - Runs BEFORE VS Code server starts
# Sets up symlinks for VS Code server directories to persistent volume storage

set -e

echo "=== Setting up VS Code server symlinks ==="

# Function to handle migration and symlink creation
setup_vscode_symlink() {
    local edition="$1"  # "stable" or "insiders"
    local suffix=""
    [ "$edition" = "insiders" ] && suffix="-insiders"

    local dir="$HOME/.vscode-server${suffix}"
    local target="$HOME/.vscode/${edition}"

    # Ensure target directory exists in volume
    mkdir -p "$target"

    # Check if real directory exists (not a symlink)
    if [ -d "$dir" ] && [ ! -L "$dir" ]; then
        # Calculate size of orphaned data
        local size=$(du -sh "$dir" 2>/dev/null | cut -f1 || echo "unknown")

        echo ""
        echo "╔════════════════════════════════════════════════════════════════════╗"
        echo "║  WARNING: Orphaned VS Code server directory detected!              ║"
        echo "╠════════════════════════════════════════════════════════════════════╣"
        echo "║  Location: $dir"
        echo "║  Size: $size"
        echo "║                                                                    ║"
        echo "║  This data was written outside persistent storage and would be    ║"
        echo "║  lost on container rebuild. Migrating to persistent volume...     ║"
        echo "╚════════════════════════════════════════════════════════════════════╝"
        echo ""

        # Migrate contents to volume
        echo "Migrating $dir -> $target ..."
        cp -a "$dir"/. "$target"/ 2>/dev/null || true
        rm -rf "$dir"

        echo "Migration complete."
        echo ""
    fi

    # Remove any existing symlink or empty directory
    rm -rf "$dir" 2>/dev/null || true

    # Create symlink
    ln -sfn "$target" "$dir"
    echo "Symlinked: $dir -> $target"
}

# Set up both VS Code editions
setup_vscode_symlink "stable"
setup_vscode_symlink "insiders"

echo ""
echo "VS Code server symlinks configured."
