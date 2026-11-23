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

## Part 9: Push to GitHub

1-2. On github.com: **New repository** → name `my-first-repo` → do **not** tick "Add a README"
     (otherwise the remote has a commit that my local repo does not have, and the first push is rejected).

```bash
git remote add origin https://github.com/KamilKabbaj1/my-first-repo.git   # 3. link local → GitHub
git remote -v                                                             #    check the link
git push -u origin main                                                   # 4. send the commits
```

`origin` is just the conventional name of the remote. `-u` (upstream) remembers that local `main`
tracks `origin/main`, so the next times a plain `git push` / `git pull` is enough.

5. After refreshing the GitHub page, I see the files (`readme.txt`, `install.sh`), the number of commits,
   and the history with the same messages and hashes as `git log` locally.

## Part 10: Delete and clone

```bash
cd ..                                                         # 1. leave the project folder
rm -rf my-first-repo                                          # 2. delete the local folder (and its .git/)
git clone https://github.com/KamilKabbaj1/my-first-repo.git   # 3. download it again from GitHub
cd my-first-repo && ls && git log --oneline                   # 4. files and full history are back
```

`git clone` gives back the whole history, not only the files, and the remote `origin` is already configured.

## Part 11: Full workflow practice

Repository: **<https://github.com/KamilKabbaj1/bash-installer>**

```bash
# 1-2. clean up the previous exercise
cd ~ && rm -rf my-first-repo          # local folder
# on github.com: my-first-repo → Settings → Danger Zone → Delete this repository

# 3-4. new project
mkdir bash-installer && cd bash-installer
git init -b main                      # -b main: name the first branch "main"

# 5-6. README on main
nano README.md
git add README.md
git commit -m "Add README describing the project"

# 7-9. the script lives on a feature branch
git switch -c feature-install
cp ~/test-repo/02_git_workflow/install.sh .
chmod +x install.sh
git add install.sh
git commit -m "Add install script"

# 10-12. merge and clean up
git switch main
git merge feature-install             # fast-forward, like in part 8
git branch -d feature-install

# 13-14. on github.com: create "bash-installer" WITHOUT README, then:
git remote add origin https://github.com/KamilKabbaj1/bash-installer.git
git push -u origin main
```

Result (`git log --oneline --graph --all`): two commits on `main`, "Add README describing the project"
then "Add install script", and no other branch left.

---

## Reflection questions

1. **Why is version control useful?**
   It keeps the full history of a project: I can see who changed what, when and why, go back to
   any previous version if something breaks, work on several things in parallel with branches,
   and collaborate without overwriting each other's work. With a remote (GitHub) it is also a backup.

2. **What is the difference between staging and committing?**
   Staging (`git add`) chooses *which changes* go into the next snapshot. It is a preparation area
   where I can compose the commit file by file. Committing (`git commit`) actually *records* that
   snapshot in the history, permanently, with a message, an author and a date.
   So I can modify 5 files but commit only the 2 that belong to the same logical change.

3. **When should you make a commit?**
   Each time a small, coherent and working unit of work is finished: one feature, one bug fix,
   one refactoring. "Commit small, commit often": if something breaks, a small commit tells me
   exactly which change caused it, and it is easy to revert.

4. **What is the difference between `git init` and `git clone`?**
   `git init` creates a *new, empty* repository in the current folder (no history, no remote).
   `git clone <url>` copies an *existing* remote repository: files, full history, branches,
   and it configures the remote `origin` automatically.

5. **Why should you write good commit messages?**
   The history is documentation: `git log --oneline` must tell what happened without opening
   each commit. A clear message ("Fix null pointer in login handler") helps teammates, reviewers
   and my future self find when and why a change was made. "updates" or "fixed some bugs" say nothing.

6. **What is the purpose of using branches?**
   A branch is an independent line of development: I can build a feature or try an idea without
   breaking the stable code on `main`, several people can work on different features at the same
   time, and the work is merged only when it is ready (and can be thrown away if it is not).

7. **When would you create a new branch instead of working on main?**
   As soon as the work is more than a trivial change: a new feature (`feature-login`), a bug fix
   (`fix-...`), an experiment, or any work that will take several commits or must be reviewed.
   `main` should always contain production-ready code, so unfinished work never goes there directly.
