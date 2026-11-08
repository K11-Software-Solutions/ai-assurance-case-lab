# 02. Claims, Arguments and Evidence

> **Series:** AI Assurance Case Lab · [Index](../README.md#articles) · Previous: [01](01-test-results-are-not-an-assurance-case.md) · Next: [03. Evidence You Can Trust](03-evidence-you-can-trust.md)

Assurance cases are usually written in one of two closely related notations: **Claims, Arguments, Evidence** (CAE) and the **Goal Structuring Notation** (GSN). Both say the same thing: a top claim, broken down by an argument into sub-claims, each eventually resting on evidence. This lab uses that structure, written as JSON so it can be checked by code.

## The top claim and the strategy

> **G0:** Orbitly Support Assistant 2.3.0 is acceptably safe, effective and controllable for release to customers.
>
> *Strategy:* argue over each quality attribute, with evidence from the lab that tests it; accept stated residual risks.

Two **context** statements frame it: what the system does, and the fact that all evidence comes from teaching labs, so the case is a template. Context is part of the argument: a claim is only true *in* a context.

## Eleven sub-claims

| Claim | Says | Critical | Evidence from |
|---|---|---|---|
| G1 | Answers are correct, grounded, and cite their source | yes | Becoming an AI Quality Engineer |
| G2 | The model is fit for purpose and does not leak training secrets | no | LLM Model Testing Lab, AI Security Testing Lab |
| G3 | Actions taken are the ones the customer asked for | yes | Agent Testing Lab, Multi-Agent Testing Lab |
| G4 | The refund flow never pays twice; failures are attributable | yes | Multi-Agent Testing Lab |
| G5 | Production is recorded; incidents are detected and fed back | no | AI Production Monitoring Lab |
| G6 | Performance and cost stay within limits under expected load | no | AI Performance and Cost Lab |
| G7 | The automated evaluators are trustworthy | yes | Becoming an AI Quality Engineer, AI Evaluation Science Lab |
| G8 | Eval data, training data and the knowledge base are fit | yes | AI Data Quality Lab |
| G9 | Attackers cannot leak data, misuse tools or run up costs | yes | AI Security Testing Lab |
| G10 | Third-party MCP tools cannot hijack the assistant | yes | MCP Testing Lab |
| G11 | When it cannot finish safely, it stops and hands over to a person | no | Multi-Agent Testing Lab, Agent Testing Lab |

**Critical** claims are those where being wrong causes serious harm: money, data, security, or the evidence itself being untrustworthy. The case's checks hold them to a higher standard (article 07).

G7 is easy to forget and essential: several other claims rest on automated evaluators (an LLM judge, a groundedness metric). If the evaluators are wrong, those claims are wrong with them. An assurance case for an AI system must argue for its measuring instruments, not just its measurements.

## Evidence items

Each of the 25 evidence items records:

| Field | Example |
|---|---|
| claim | G9 |
| lab and file | ai-security-testing-lab, `experiments/results/summary.md` |
| quote | `\| all layers (recommended) \| 0.0 \| none \| 0.0 \|` |
| kind | measurement (or gate, or documented finding) |
| method | static attack suite, 20 repeats |
| numbers | 0 successes in 1,440 attempts |
| system version and date | 2.3.0, 2026-11-07 |
| evaluator dependency | (for E1: relies on E3, the judge validation) |

The **kind** matters. A *measurement* or *gate* result is a number produced by code. A *documented finding* is a sentence in a README, such as "Evaluations on world state caught it." Documented findings are real evidence, but weaker: they can't be re-checked without re-running the lab. Two of the labs (model and agent) commit no machine-readable results, so their evidence is documented findings, and the case says so.

## Reading the case

The rendered decision ([`docs/release-decision.md`](../docs/release-decision.md)) shows every claim with its evidence (each quote linked to the exact line's file at the pinned commit), its defeaters and how they were resolved, the residual risk register and the framework coverage table. That document, not the test logs, is what a release board or an auditor reads.
