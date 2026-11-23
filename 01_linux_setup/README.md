# 01 — Linux setup: shell and Bash scripting (slide 18)

Statement: <https://courses.dallard.tech/linux/bash_exo/>

Environment: Ubuntu 26.04 under WSL (Windows), Bash.

---

## Key concepts

- **Shell vs terminal**: the *terminal* is the window program that displays text and sends
  my keystrokes (Windows Terminal, macOS Terminal). The *shell* is the program running inside it
  that interprets my commands and asks the kernel to execute them (Bash, Zsh, sh). One terminal
  can run different shells.
- **Environment variables**: named values (`NAME=value`) that every process inherits from its
  parent, and that configure programs without changing their code. Examples: `$HOME`, `$USER`, `$SHELL`,
  `$PATH` (the folders searched for executables). `export VAR=value` makes a variable
  visible to child processes. `env` lists them all.
- **Scripts**: text files containing a sequence of shell commands, run as one program. They
  automate repetitive tasks. The first line (shebang `#!/usr/bin/env bash`) says which
  interpreter runs the file, and the file must be executable (`chmod +x`).
- **Package managers**: tools that download, install, update and remove software *with its
  dependencies*, from trusted repositories: `apt` (Debian/Ubuntu), `yum`/`dnf` (Red Hat), `brew`
  (macOS), `pip` (Python packages only).

---

## Part 1: Improve your shell experience

### Step 1.1 — Which shell am I using?

```bash
getent passwd "$USER" | cut -d: -f7   # default (login) shell of my account → /bin/bash
echo "$SHELL"                         # SHELL environment variable → /bin/bash
ps -p $$ -o comm=                     # shell CURRENTLY running ($$ = its PID) → bash
```

`$SHELL` is the **login shell** written in `/etc/passwd`: it does not change if I start
`zsh` by hand from Bash. `ps -p $$` (or `echo $0`) shows the shell that is actually running.
On my machine all three say **Bash**.

### Step 1.2 — Install a shell framework: Oh My Bash

I use Bash, so I install **Oh My Bash** (Zsh users would install Oh My Zsh instead):

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
```

The installer backs up my `~/.bashrc` (`~/.bashrc.omb-backup-...`) and writes a new one that loads
the framework. To choose a theme, I edit `~/.bashrc`:

```bash
nano ~/.bashrc
# OSH_THEME="font"      → change the value, e.g. OSH_THEME="powerline"
source ~/.bashrc        # reload the configuration in the current shell
```

The prompt changes: it shows the theme, the current folder and the Git branch. That shows the framework is active.

**What's the purpose of the `source` command?**
`source file` (or `. file`) runs the commands of the file **inside the current shell**, instead
of starting a new shell process. So the variables, aliases and functions it defines stay
available in my session. That is why `source ~/.bashrc` applies a configuration change without
closing the terminal. Running `bash ~/.bashrc` would apply it in a child shell that ends immediately,
and nothing would change in my session.

### Step 1.3 — Enable the Git plugin

1. Open the configuration file: `nano ~/.bashrc` (Bash). Zsh users would open `~/.zshrc`.
2. Find the `plugins` section and add `git` to the list:

   ```bash
   plugins=(
     git
     bashmarks
   )
   ```

   (The `.bashrc` template of Oh My Bash may already list `git`. In that case, nothing to add.)

3. Save (`Ctrl+O`, `Enter`, `Ctrl+X`), then reload: `source ~/.bashrc`.

Verify the aliases (inside a Git repository):

```bash
gst          # = git status
gl           # = git pull
gp           # = git push
glo          # = git log --oneline --decorate
alias | grep "git status"    # shows which alias points to which command
```

`gst` displays exactly the same output as `git status`, so the plugin is loaded.

---

## Part 2: Check the Python installation

```bash
python --version     # → "command not found" on Ubuntu
python3 --version    # → Python 3.14.4
```

On recent Ubuntu, the `python` command does not exist: only `python3` is installed. Python 2
is no longer shipped, and `python` could point to it on older systems. That is why I always
type **`python3`** explicitly. (`sudo apt install python-is-python3` would create the `python` alias.)

Python 3 **is installed** (3.14.4), but `pip3 --version` answers "command not found": pip is a
separate package on Ubuntu (`python3-pip`). The script of Part 3 detects this and installs it.

---

## Part 3: Write the automation script

### Step 3.1 — Create the file and make it executable

```bash
touch env_install.sh
chmod +x env_install.sh   # x = execute permission. Without it: "Permission denied"
ls -l env_install.sh      # -rwxr-xr-x : the x bits are set
```

### Step 3.2 — Structure

The script follows the requested order: **shebang**, then **functions** at the top, then the **main
logic** in a `main` function called on the last line, with **conditional branches** depending on the
OS and on what is already installed. Putting the steps in `main` makes the whole workflow
readable in 10 lines, and each function does a single job.

### Step 3.3 — `env_install.sh`

| Feature | Where |
|---|---|
| 1. Pretty printing with `printf` and blank lines | `pretty_print` (with colours: bonus) |
| 2. OS detection with `$OSTYPE` | `detect_os` |
| 3. Install python3 if missing, otherwise show the version | `check_python` |
| 4. pip verification | `check_pip` (installs `python3-pip` on Ubuntu, where it is missing) |
| 5. Jupyter Notebook installation per OS | `install_jupyter` |
| 6. `brew doctor` on macOS | `check_brew` |
| Bonus: strict mode, colours, `--dry-run` option | top of the file, `run` |

```bash
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
```

### Step 3.4 — Best practices applied

- **Comments** explain *why* (e.g. why `printf` rather than `echo`, why `apt` rather than `pip` for Jupyter).
- **Error handling**: `set -euo pipefail` stops the script at the first error. Each missing tool
  gets a clear message, and an unsupported OS ends with an error message and exit code 1.
  `brew doctor || ...` handles a known non-zero exit code on purpose.
- **Quoted variables** everywhere (`"$OSTYPE"`, `"$@"`, `"$1"`): a value with spaces stays one
  argument instead of being split into several words.
- **Incremental testing**: each feature was run with `--dry-run` before the next one was added.

---

## Part 4: Execute and verify

### Step 4.1 — Run the script

```bash
./env_install.sh --dry-run   # first, see what it would do
./env_install.sh             # then the real run (sudo asks for the password)
```

Output of the dry run on my machine (Ubuntu/WSL, pip and Jupyter not installed yet):

```text
Starting environment setup...
Dry-run mode: nothing will be installed
Detected operating system: linux (linux-gnu)
Python is installed: Python 3.14.4
pip not found, installing python3-pip...
[dry-run] sudo apt update
[dry-run] sudo apt install -y python3-pip
Installing Jupyter...
[dry-run] sudo apt install -y jupyter-notebook
Environment ready!
```

### Step 4.2 — Verification checklist

| Check | Command | Expected |
|---|---|---|
| Shell prompt reflects the framework | open a new terminal | Oh My Bash theme prompt |
| Git aliases | `gst` in a repository | same output as `git status` |
| Python 3 | `python3 --version` | `Python 3.x` |
| pip | `python3 -m pip --version` | `pip X.Y from ... (python 3.x)` |
| Jupyter | `jupyter notebook` | the server starts and prints a `http://localhost:8888/...` URL |
| macOS only | `brew doctor` | `Your system is ready to brew.` |

## Bonus challenges

- **Done**: colours (`pretty_print` levels), strict mode (`set -euo pipefail`), a `--dry-run` argument.
- **Not done** (to keep the script short): log file, `--verbose`/`--quiet`, uninstall option.
  Ideas: `exec > >(tee -a install.log)` to log everything, and an `uninstall` branch that calls
  `sudo apt remove` on the same package list.
