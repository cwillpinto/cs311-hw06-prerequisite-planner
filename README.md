# Homework 6 The Prerequisite Planner

Read **Homework 6 The Prerequisite Planner.pdf** or its Markdown copy. Both parts are 50 points, total 100; due November 18, 2026 at 11:59 PM Central (America/Chicago).

## Start

Starter repository: https://github.com/cwillpinto/cs311-hw06-prerequisite-planner

1. Select **Use this template → Create a new repository** and choose your own GitHub account. Clone your new repository, then open its folder in VS Code.
2. Check `python --version` (3.11+). Only the standard library is required. Run `python test_planner.py`. The untouched starter stops at its intended `NotImplementedError` TODO.
3. Complete the four numbered written questions using the handout's worked-example and slide guidance.
4. Implement `has_cycle` and `topological_sort` using recursive DFS. Rerun `python test_planner.py` after each phase; a later TODO can still stop an intermediate run.
5. Read every PASS/FAIL line. Once all 50 checks pass, enter your own USI username for the Success Token. Do not edit the verification suite.
6. Submit `HW6_Theory.pdf` or `HW6_Theory.md`, completed `prereq_planner.py` and the Success Token through Blackboard. Include the syllabus AI Usage note when applicable.

## Repository ownership

Push completed work to your own repository. Check `git remote -v` before pushing; `origin` must point to your account. Never push answers to the instructor starter.

If you prefer a direct clone, first create an empty repository under your account, then:

```sh
git clone https://github.com/cwillpinto/cs311-hw06-prerequisite-planner.git
cd cs311-hw06-prerequisite-planner
git remote rename origin upstream
git remote add origin <student-owned-repository-url>
git remote -v
git branch --show-current
git push -u origin main
```

Replace the placeholder with your own repository URL. Use your actual branch if it differs from `main`. A Blackboard starter ZIP is a fallback if GitHub is unavailable; extract the entire ZIP before running.

The token verifies only supplied checks. Method compliance and written reasoning are reviewed separately. The existing theory/source/token submission requirements are unchanged; no graded repository URL or commit item is added.

An arrow runs from a prerequisite to its dependent course. The graph is a teaching model, not an official degree audit. Review slides 54–62 and the practice trace on slide 61. The harness includes 20 seeded random-DAG trials and checks prerequisite constraints rather than requiring a unique order.
