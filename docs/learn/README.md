# Learning guide

This guide teaches everything the project uses, in the order you need it. It
assumes you can program in Python and know what a graph is. It assumes nothing
about planning, security, or neural networks.

Every chapter ends with **self-check questions**. If you can answer them out
loud without notes, you understand the chapter well enough for the viva and
for a reviewer. If you cannot, re-read and run the code the chapter points to.

## How the guide and the code fit together

We build the project in layers. Each layer gets a chapter written alongside
the code, and every worked example in a chapter is produced by code in this
repository, so the numbers are real and you can re-run them.

| Chapter | Topic | Code it explains | Status |
| --- | --- | --- | --- |
| [01](01-the-problem.md) | Attack graphs, CVEs, CVSS, the cost model | `src/ahg/task.py`, `src/ahg/examples.py` | written |
| [02](02-search.md) | State spaces, UCS, A*, weighted A*, GBFS | `src/ahg/search.py` | written |
| [03](03-heuristics.md) | Delete relaxation, hmax, hadd, hFF, LM-cut | `src/ahg/heuristics.py` | written |
| [04](04-learning.md) | Regression, MLPs, GNNs, WL features, learned heuristics | `src/ahg/models/` (next) | concepts written |
| [05](05-research-method.md) | Hypotheses, splits, metrics, statistics, the paper | `PREREG.md`, `eval.py` (later) | concepts written |
| 06 | Network and vulnerability generator | `topology.py`, `vulns.py`, `generate.py` | after the generator is built |
| 07 | Labels and training data | `labels.py`, `features.py` | after labels are built |
| [Glossary](glossary.md) | Every term in one place | | written |

## The whole project in one paragraph

A defender wants to know the cheapest way an attacker could break into the
most important machine on a network. We model that as a search problem: the
attacker's privileges are the state, exploits are actions with costs, and the
goal is a target privilege. A* search finds the cheapest attack, and how fast
it finds it depends on its *heuristic*, a guess of the remaining cost. Classical
heuristics are computed by formula. We train a neural network to make that
guess instead, and test whether it makes A* faster on networks it has never
seen (bigger ones, differently shaped ones, ones with different
vulnerabilities), and at what cost in solution quality.

## Running the code

```bash
uv sync                          # create .venv with the pinned Python and deps
uv run pytest -q                 # all correctness tests
uv run python scripts/toy_demo.py  # the worked example used in chapters 1-3
```

## Reading order

Read 01 to 03 in order before touching the code; they build on each other.
Chapter 04 can be read any time after 02. Chapter 05 is the one that turns a
coursework project into a paper; read it before any experiment is run.
