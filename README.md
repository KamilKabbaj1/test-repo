# OOP & Design Patterns in Python — Exercises

Exercises for the course **"Object Oriented Programming & Design pattern in Python"**
(Benjamin Dallard, CentraleSupélec, 2nd year). One folder per exercise.

## Exercises

| Folder | Slide | Statement | Content |
|---|---|---|---|
| `01_linux_setup/` | 18 | [bash_exo](https://courses.dallard.tech/linux/bash_exo/) | ⏳ Pending: exercise statement not available yet |
| [`02_git_workflow/`](02_git_workflow/) | 26 | [Git mini exo](https://gist.github.com/bdallard/8bdbdd70f234f94823c0c2cde9515388) | Commands and answers for parts 1–11, reflection questions, `install.sh`. Part 11 repo: [bash-installer](https://github.com/KamilKabbaj1/bash-installer) |
| [`03_oop_basics/`](03_oop_basics/) | 67 | [OOP problems](https://gist.github.com/bdallard/b2f2c910e3a9b564a30c86991c97b4fc) | `operator_overloading.py`, `inheritance.py` + pytest tests |
| [`04_uml/`](04_uml/) | 68 | [UML practice](https://gist.github.com/bdallard/2d2407c4de4c182afca6d3ec7235e9eb) | Mermaid diagrams (Hospital + ABCD Records), Python implementation + tests |
| `05_design_patterns/` | 84 | [creational](https://courses.dallard.tech/sys_design/creational_pattern/) · [structural](https://courses.dallard.tech/sys_design/structural_pattern/) · [behavioral](https://courses.dallard.tech/sys_design/behavioral_pattern/) | ⏳ Pending: exercise statement not available yet |

## Running the tests

Tests use [pytest](https://docs.pytest.org/en/stable/) (slide 90) inside a virtual environment:

```bash
python3 -m venv .venv                       # create the venv (once)
source .venv/bin/activate                   # activate it
pip install -r requirements-dev.txt         # install pytest
pytest -v                                   # run every test of every exercise
pytest 03_oop_basics -v                     # or only one exercise
```

`pytest.ini` adds the exercise folders to the import path, because a folder name starting
with a digit (`03_oop_basics`) cannot be imported as a Python package.
