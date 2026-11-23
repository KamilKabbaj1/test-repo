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
