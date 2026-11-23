# 02 — Git workflow (slide 26)

Statement: <https://gist.github.com/bdallard/8bdbdd70f234f94823c0c2cde9515388>

Each part lists the commands I used and my answers to the questions.
Environment: Ubuntu under WSL, Bash.

---

## Part 1: Setup & config

```bash
sudo apt update && sudo apt install -y git   # 1. install Git (already present on Ubuntu/WSL)
git --version                                # 2. check the installed version, e.g. "git version 2.x.y"
git config --global user.name "Kamil Kabbaj" # 3. name stored in every commit I create
git config --global user.email "<my GitHub email>"
git config --global --list                   # check what is configured
```

`--global` writes to `~/.gitconfig`, so the identity applies to every repository on this machine.
Without `--global`, it only applies to the current repository (in `.git/config`).

## Part 2: Create your first repository

```bash
mkdir my-first-repo     # create the folder
cd my-first-repo        # navigate into it
git init                # create the hidden .git/ folder: the folder is now tracked by Git
touch readme.txt        # create an empty file
```

## Part 3: Your first commit

1. Current state of the repository: `git status`
2. Stage `readme.txt`: `git add readme.txt`
3. Commit with a message: `git commit -m "Add readme file"`
4. Commit history: `git log`

## Part 4: Make changes

```bash
echo "My first Git repository" >> readme.txt   # 1. add a line (>> appends, > would overwrite)
git status                                     # 2.
git add readme.txt                             # 3.
git commit -m "Add description line to readme"
git log --oneline                              # 4.
```

2. `git status` now reports `readme.txt` under **"Changes not staged for commit"** as *modified*:
   Git knows the file (it is in the last commit), sees that its content changed, but the change is
   not in the staging area yet, so it would not be part of the next commit.
4. I now have **2 commits** ("Add readme file" and "Add description line to readme").

## Part 5: Exploration

- `git diff`: shows, line by line, the differences between the working directory and the staging area,
  i.e. the changes that are **not staged yet** (`+` added lines, `-` removed lines).
  `git diff --staged` shows what is staged but not committed yet.
- `git log --oneline`: shows the history in compact form, one commit per line: the short hash
  (first 7 characters) and the first line of the message, most recent first.

## Part 6: Working with branches

```bash
git branch                    # 1. list local branches (* marks the current one)
git branch feature-script     # 2. create a branch (without switching to it)
git switch feature-script     # 3. switch to it (older equivalent: git checkout feature-script)
git switch -c dev             # 4. create AND switch in one command (older: git checkout -b dev)
git switch feature-script     # 5. go back to feature-script
git branch                    # 6. the * is in front of feature-script
git status                    #    first line: "On branch feature-script"
```

## Part 7: Create a Bash script on a branch

```bash
git branch                    # 1. check that * is on feature-script
nano install.sh               # 2-3. create the script (content: see install.sh in this folder)
chmod +x install.sh           # 4. make it executable
git add install.sh            # 5.
git commit -m "Add install script"
git log --oneline             # 6. history of this branch
```

The script ([`install.sh`](install.sh)) contains a shebang, the two messages, `apt update` to
refresh the package lists, and `apt install -y tree` to install a package.

6. `git log --oneline` on `feature-script` shows 3 commits: the 2 commits inherited from `main`
   (the branch started from there) plus "Add install script".

## Part 8: Merge branches

```bash
git switch main               # 1.
ls                            # 2.
git merge feature-script      # 3. bring the commits of feature-script into main
ls                            # 4.
git log --oneline             # 5.
git branch -d feature-script  # 6. delete the branch (safe: refused if it is not merged)
```

2. `install.sh` is **not present**: it was committed only on `feature-script`. When switching
   branches, Git rewrites the working directory to match the last commit of the target branch,
   and `main` has no commit containing that file.
4. `install.sh` now appears in the folder: the merge brought the commit into `main`.
5. The history of `main` now contains "Add install script". Since `main` had no new commit since
   the branch was created, Git made a **fast-forward** merge: it simply moved the `main` pointer
   forward to the last commit of `feature-script`. No merge commit was created and the history
   stays linear.
6. `git branch -d feature-script` (`-D` would force the deletion of an unmerged branch).
