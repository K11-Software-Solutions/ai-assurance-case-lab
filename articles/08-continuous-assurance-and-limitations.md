# 08. Continuous Assurance, the Series, and Limitations

> **Series:** AI Assurance Case Lab · [Index](../README.md#articles) · Previous: [07](07-testing-the-case.md)

## Continuous assurance in CI

An assurance case written once, in a document, is out of date by the next release. Here the case is code and data, so CI keeps it honest on every push:

| CI job | What it checks |
|---|---|
| tests | the checks themselves, on hand-made cases; the committed JSON matches its source; the committed release decision is current |
| evidence integrity | every snapshot matches its pinned commit and hash (`python -m assurance.snapshot --check`) |
| assurance case | all nine checks pass and a decision is reached; thirteen broken cases must each be NO-GO for the right reason |

Because evidence has dates and risks have expiry dates, the case **fails by itself as time passes**: 90 days after collection, evidence goes stale; on its expiry date, a risk acceptance lapses. A release decision that silently remains "GO" forever is not continuous assurance.

## Updating the case for a new release

1. Re-run the labs (or your real test suites) against the new version and publish their results.
2. Pin the new releases in [`evidence/sources.json`](../evidence/sources.json) and run `python -m assurance.snapshot`.
3. Update the evidence items: quotes, numbers, system version, dates. Add the new defeaters you found.
4. Review the residual risks: renew, fix or retire each.
5. Run `python -m evals.run_case --publish` and review the diff of [`docs/release-decision.md`](../docs/release-decision.md) like code.

## What the series covered

| Lab | Claim it supports here |
|---|---|
| Becoming an AI Quality Engineer | G1 answers, G7 evaluators |
| LLM Model Testing Lab | G2 model |
| Agent Testing Lab | G3 actions, G11 escalation |
| AI Production Monitoring Lab | G5 production |
| Multi-Agent Testing Lab | G3, G4 refund flow, G11 |
| AI Performance and Cost Lab | G6 performance and cost |
| AI Evaluation Science Lab | G7 evaluators |
| AI Data Quality Lab | G8 data |
| AI Security Testing Lab | G2 (rebuttal), G9 security |
| MCP Testing Lab | G10 tool supply chain |

## Limitations

- **The evidence is from teaching labs.** Most use simulated models, agents and services. The case is a template for the structure and the checks; the numbers are not evidence about any real system.
- **One system, assembled for the argument.** The ten labs test different fictional products; the case treats them as components of one assistant. A real case has evidence produced against the real, integrated system.
- **Coarse framework mappings.** Articles, functions, clauses and characteristics, not sub-requirements, and no legal assessment.
- **Documented findings for two labs.** The model and agent labs publish no machine-readable results, so their evidence is prose. The right fix is upstream.
- **Mechanical checks.** The checks confirm the case is complete, traceable, current and internally consistent. They cannot confirm that an argument is *convincing*; that still needs a knowledgeable human reviewer.
- **Independence by method name.** Two methods from the same lab, sharing the same data, may share the same blind spot. Real cases need a reviewer's judgement about independence.

## Takeaways

- **Keep the case in CI**, so it fails when evidence goes stale or acceptances expire.
- **Update the case with every release** and review the decision's diff.
- **Checks make a case complete and honest; people judge whether it is convincing.**
