#!/usr/bin/env bash
# env_install.sh - set up a Python / Jupyter development environment.
# Usage: ./env_install.sh            install what is missing
#        ./env_install.sh --dry-run  only show what would be done

# Strict mode (bonus): -e stop at the first failing command, -u an unset
# variable is an error (catches typos such as "$PAKAGE"), -o pipefail a pipeline
# fails if ANY command in it fails (not only the last one).
set -euo pipefail

# ---------------------------------------------------------------- settings
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then   # ${1:-} = "" if no argument (needed with -u)
    DRY_RUN=true
fi

# ANSI colour codes (bonus): green = success, yellow = warning, red = error.
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

# ---------------------------------------------------------------- functions
# Feature 1: pretty printing. $1 = message, $2 = optional level.
# printf instead of echo: echo handles "-e" and backslashes differently from
# one system to another, printf behaves the same everywhere.
pretty_print() {
    local message="$1"
    local level="${2:-info}"
    local color="$RESET"
    case "$level" in
        success) color="$GREEN" ;;
        warning) color="$YELLOW" ;;
        error)   color="$RED" ;;
    esac
    printf "\n%b%s%b\n\n" "$color" "$message" "$RESET"
}

# Run a command, or only display it in dry-run mode. "$@" keeps every
# argument intact (quoted), even if it contains spaces.
run() {
    if [[ "$DRY_RUN" == true ]]; then
        printf "[dry-run] %s\n" "$*"
    else
        "$@"
    fi
}

# Feature 2: operating system detection with the OSTYPE variable set by Bash.
# The patterns end with * because OSTYPE contains versions: "darwin23", "linux-gnu".
detect_os() {
    case "$OSTYPE" in
        linux*)  OS="linux" ;;
        darwin*) OS="macos" ;;
        *)
            pretty_print "Unsupported operating system: $OSTYPE" error
            exit 1
            ;;
    esac
    pretty_print "Detected operating system: $OS ($OSTYPE)"
}

# Install packages with the package manager of the detected OS.
# Written once, so the rest of the script never repeats the if/else on the OS.
APT_UPDATED=false
install_packages() {
    if [[ "$OS" == "linux" ]]; then
        # apt update only once per run: it is slow and the list does not change.
        if [[ "$APT_UPDATED" == false ]]; then
            run sudo apt update
            APT_UPDATED=true
        fi
        run sudo apt install -y "$@"
    else
        run brew install "$@"
    fi
}

# Feature 3: install python3 only if it is missing.
check_python() {
    # command -v prints the path of a command and fails if it does not exist.
    # It is the portable way to test "is this program installed?".
    if command -v python3 > /dev/null; then
        pretty_print "Python is installed: $(python3 --version)" success
    else
        pretty_print "python3 not found, installing it..." warning
        if [[ "$OS" == "linux" ]]; then
            install_packages python3
        else
            install_packages python
        fi
    fi
}

# Feature 4: verify pip. "python3 -m pip" uses the pip of THIS python3, so it
# avoids a pip3 command that belongs to another Python installation.
check_pip() {
    if python3 -m pip --version > /dev/null 2>&1; then
        pretty_print "pip is installed: $(python3 -m pip --version)" success
    elif [[ "$OS" == "linux" ]]; then
        # On Debian/Ubuntu, pip is a separate package.
        pretty_print "pip not found, installing python3-pip..." warning
        install_packages python3-pip
    else
        # Homebrew's Python always ships pip: if it is missing, the install is broken.
        pretty_print "pip not found: try 'brew reinstall python'" error
        exit 1
    fi
}

# Feature 5: install Jupyter Notebook (different command per OS).
install_jupyter() {
    if command -v jupyter > /dev/null; then
        pretty_print "Jupyter is already installed: $(jupyter --version | head -n 1)" success
        return
    fi
    pretty_print "Installing Jupyter..."
    if [[ "$OS" == "linux" ]]; then
        # The Ubuntu package, rather than "pip install": recent Ubuntu refuses pip
        # installs into the system Python (PEP 668, "externally-managed-environment").
        install_packages jupyter-notebook
    else
        install_packages jupyterlab
    fi
}

# Feature 6: Homebrew health check, on macOS only.
check_brew() {
    pretty_print "Running brew doctor..."
    # brew doctor returns an error code for simple warnings. "|| ..." keeps
    # strict mode from stopping the script for a warning.
    run brew doctor || pretty_print "brew doctor reported warnings (see above)" warning
}

# ---------------------------------------------------------------- main logic
main() {
    pretty_print "Starting environment setup..."
    # An "if" rather than "[[ ... ]] && ...": with set -e, a false test at the
    # end of a function would make the function itself fail.
    if [[ "$DRY_RUN" == true ]]; then
        pretty_print "Dry-run mode: nothing will be installed" warning
    fi
    detect_os
    check_python
    check_pip
    install_jupyter
    if [[ "$OS" == "macos" ]]; then
        check_brew
    fi
    pretty_print "Environment ready!" success
}

main "$@"
