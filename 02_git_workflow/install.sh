#!/usr/bin/env bash
# install.sh - small installation script (Git workflow exercise, part 7).
#
# Shebang: "/usr/bin/env bash" finds bash wherever it is installed in the PATH,
# which is more portable than hard-coding "/bin/bash".

# Stop at the first failing command: there is no point in printing
# "Installation complete!" if the update or the install failed.
set -e

echo "Starting installation..."

# Refresh the list of available packages, so apt installs the latest version.
sudo apt update

# Install a package of my choice: "tree" displays folders as a tree.
# -y answers "yes" automatically, so the script runs without user interaction.
sudo apt install -y tree

echo "Installation complete!"
