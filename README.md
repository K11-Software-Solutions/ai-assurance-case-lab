# AI Assurance Case Lab

[![CI quality gates](https://github.com/K11-Software-Solutions/ai-assurance-case-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/K11-Software-Solutions/ai-assurance-case-lab/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE) [![Articles: CC BY 4.0](https://img.shields.io/badge/Articles-CC%20BY%204.0-lightgrey.svg)](articles/LICENSE.md)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![No dependencies](https://img.shields.io/badge/runtime%20deps-none-success)

**The capstone of the series: turn the evidence from ten AI testing labs into one reviewable argument that a system is fit to release. Claims, arguments and evidence pinned to archived releases; defeaters and residual risks with owners and expiry dates; mappings to NIST AI RMF, ISO/IEC 42001 and the EU AI Act; and nine checks that test the argument itself.**

The capstone of a series for quality engineers moving into AI:

| Lab | Question it answers |
|---|---|
| [Becoming an AI Quality Engineer](https://github.com/K11-Software-Solutions/becoming-ai-quality-engineer) | Is the RAG **application** good enough to ship? |
| [LLM Model Testing Lab](https://github.com/K11-Software-Solutions/llm-model-testing-lab) | Is the **model** good enough? |
| [Agent Testing Lab](https://github.com/K11-Software-Solutions/agent-testing-lab) | Is the **agent** safe to let act? |
| [AI Production Monitoring Lab](https://github.com/K11-Software-Solutions/ai-production-monitoring-lab) | Is it **still** good, for the users we actually have, right now? |
| [Multi-Agent Testing Lab](https://github.com/K11-Software-Solutions/multi-agent-testing-lab) | When **agents work together**, does the team do the right thing, and who broke it when it doesn't? |
| [AI Performance and Cost Lab](https://github.com/K11-Software-Solutions/ai-performance-cost-lab) | Is it **fast enough under load**, and what does each **good answer** cost? |
| [AI Evaluation Science Lab](https://github.com/K11-Software-Solutions/ai-evaluation-science-lab) | Can we **trust the evaluator**, and how sure are we? |
| [AI Data Quality Lab](https://github.com/K11-Software-Solutions/ai-data-quality-lab) | Is the **data** behind it all fit to learn from, test with and retrieve? |
| [AI Security Testing Lab](https://github.com/K11-Software-Solutions/ai-security-testing-lab) | Can an **attacker** make it misbehave, and how sure are we that they can't? |
| [MCP Testing Lab](https://github.com/K11-Software-Solutions/mcp-testing-lab) | Can we trust the **tools our agents plug into**? |
| **AI Assurance Case Lab** (this repo, capstone) | Can we **sign it off**, on what evidence, and what risk are we accepting? |

## The decision

**[Release decision: Orbitly Support Assistant 2.3.0: GO WITH ACCEPTED RISKS](docs/release-decision.md)**

12 claims, 25 evidence items, 6 defeaters (evidence against the claims: 1 rebutted, 5 accepted) and 6 residual risks, each with an owner, monitoring and an expiry date. Every evidence item quotes, word for word, a result file from one of the ten labs' v1.0.0 releases, pinned by commit and Zenodo DOI.

This is a **worked template**: the evidence comes from teaching labs with mostly simulated components, so the case shows how to argue, not that any real system is safe.

## Articles

| # | Article |
|---|---|
| 01 | [Why Test Results Are Not an Assurance Case](articles/01-test-results-are-not-an-assurance-case.md) |
| 02 | [Claims, Arguments and Evidence](articles/02-claims-arguments-and-evidence.md) |
| 03 | [Evidence You Can Trust: Pinning, Quoting and Freshness](articles/03-evidence-you-can-trust.md) |
| 04 | [Defeaters: Evidence Against Your Own Claim](articles/04-defeaters-evidence-against-your-own-claim.md) |
| 05 | [Residual Risk: Owners, Monitoring and Expiry](articles/05-residual-risk-owners-and-expiry.md) |
| 06 | [Mapping to NIST AI RMF, ISO/IEC 42001 and the EU AI Act](articles/06-mapping-to-the-frameworks.md) |
| 07 | [Testing the Case: Thirteen Ways an Argument Fails](articles/07-testing-the-case.md) |
| 08 | [Continuous Assurance, the Series, and Limitations](articles/08-continuous-assurance-and-limitations.md) |

## Quick start

Requirements: Python 3.11+. No runtime dependencies; no network needed except to refresh evidence.

```bash
git clone https://github.com/K11-Software-Solutions/ai-assurance-case-lab.git
cd ai-assurance-case-lab
python -m venv .venv
source .venv/bin/activate              # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

```bash
pytest                                                   # 24 tests
python -m assurance.snapshot --check                     # evidence matches its pinned commits and hashes
python -m evals.run_case                                 # nine checks and the release decision
CASE_VARIANT=stale-evidence python -m evals.run_case     # a broken case: must be NO-GO
python -m assurance.snapshot                             # refresh evidence from GitHub (network)
```

## Repository layout

```text
case/
  build_case.py            the case, written as readable Python (claims, evidence, defeaters, risks)
  assurance_case.json      the checked artefact, generated from build_case.py
evidence/
  sources.json             each lab's repository, v1.0.0 commit and Zenodo DOI, and the files used
  snapshots/               those files, fetched at the pinned commits
  manifest.json            SHA-256 of every snapshot
assurance/
  snapshot.py              fetch and verify evidence snapshots
  checks.py                nine checks on the case and the release decision
evals/
  run_case.py              the gate, the rendered decision and thirteen broken variants
docs/
  release-decision.md      the committed release decision
tests/                     24 tests
articles/                  the eight articles
.github/workflows/ci.yml   tests -> evidence integrity -> case gate + 13 broken cases that must be NO-GO
```

## What the lab shows

- **The checks found a gap in this case on its first run:** no claim covered explainability. The fix was evidence the quality lab already had (every answer must cite its source).
- **Every lab's own negative findings became defeaters**, and each is either rebutted by named evidence or accepted as a residual risk with an owner and an expiry date.
- **The strength of zero-failure evidence is a calculation:** 0 successes in 1,440 attacks supports a claim of "below 0.5%", but not "below 0.1%".
- **Evidence about an AI system includes evidence about its evaluators:** scores from an automated grader count only if the grader's validation is in the case.
- **Silence is not allowed:** a trustworthiness characteristic with no evidence (fairness) must be excluded explicitly, with a reason and an owner, or the case fails.

## CI quality gates

Every push runs three jobs: **tests**; **evidence integrity** (every snapshot matches its pinned commit and hash); and the **assurance case** gate (nine checks and a decision), with thirteen broken versions of the case that must each be NO-GO, for the right reason. Because evidence and risk acceptances carry dates, the case fails by itself when evidence goes stale or an acceptance expires.

## Limitations

Evidence from teaching labs with simulated components; one system assembled for the argument; coarse framework mappings with no legal assessment; prose-only evidence from two labs; checks that confirm completeness and traceability but not persuasiveness. [Article 08](articles/08-continuous-assurance-and-limitations.md#limitations) covers each.

## About

Created by **Kavita Jadhav**, founder of [K11 Software Solutions](https://github.com/K11-Software-Solutions), Senior SDET and AI Quality Engineer working on LLM evaluation, red teaming and agentic QA systems.

**Licences:** code under the [MIT License](LICENSE); the written material in [`articles/`](articles/LICENSE.md) and [`docs/`](docs/) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (share and adapt with credit). Evidence snapshots are copies of files from the source labs, under their own licences.

Orbitly and its support assistant are fictional. Framework mappings show where evidence is relevant; they are not a legal, regulatory or certification assessment.

## Citing

Use GitHub's **Cite this repository** button (from [`CITATION.cff`](CITATION.cff)). Each tagged release is archived on Zenodo with its own DOI; cite the version you used, or the concept DOI for the project as a whole. The DOI badge will appear here after the first release.
