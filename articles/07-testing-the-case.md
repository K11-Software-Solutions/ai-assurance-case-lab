# 07. Testing the Case: Thirteen Ways an Argument Fails

> **Series:** AI Assurance Case Lab · [Index](../README.md#articles) · Previous: [06](06-mapping-to-the-frameworks.md) · Next: [08. Continuous Assurance](08-continuous-assurance-and-limitations.md)

Every lab in this series tested a system and then tested the tests. An assurance case is an artefact too, and it can be wrong in specific, checkable ways. [`assurance/checks.py`](../assurance/checks.py) runs nine checks on it; [`evals/run_case.py`](../evals/run_case.py) proves each with broken versions of the case that must fail.

## Nine checks

| Check | Fails when |
|---|---|
| **structure** | more than one top claim, a missing parent, or a claim with no evidence (undeveloped) |
| **traceability** | a quote is not in its snapshot, a snapshot doesn't match its hash, or a source isn't pinned to a commit and DOI |
| **freshness** | evidence is about another system version, or older than 90 days |
| **independence** | a critical claim rests on fewer than two methods, or only on documented findings |
| **strength** | zero-failure evidence can't support the claim's required bound (rule of three: 0 in *n* supports about 3/*n*) |
| **evaluators** | evidence produced by an automated evaluator doesn't name the evidence that validated that evaluator |
| **defeaters** | a defeater is neither rebutted by named evidence nor accepted as a residual risk |
| **residual risks** | a risk lacks an owner, rationale or monitoring, or its acceptance has expired |
| **coverage** | a framework item is unaddressed, or a NIST characteristic is neither claimed nor excluded |

## Thirteen negative controls

| Variant | What it breaks | Caught by |
|---|---|---|
| `missing-evidence` | removes the evidence for G6 | structure |
| `broken-trace` | changes "0.0" to "0.01" in a quote | traceability |
| `tampered-snapshot` | a snapshot no longer matches its hash | traceability |
| `stale-evidence` | E10 is about version 2.2.0 | freshness |
| `old-evidence` | E12 was collected 190 days ago | freshness |
| `weak-bound` | G9 requires 0.1%; 0 in 1,440 only supports 0.21% | strength |
| `single-method` | G7 left with only the judge-vs-labels check | independence |
| `prose-only` | G3 left with only a documented finding | independence |
| `unvalidated-evaluator` | E1's evaluator validation link removed | evaluators |
| `unresolved-defeater` | D2's rebuttal removed | defeaters |
| `expired-risk` | R3's acceptance expired | residual risks |
| `coverage-gap` | Article 14 unmapped | coverage |
| `no-scope-exclusion` | the fairness exclusion removed | coverage |

Each must turn the decision into NO-GO, **and fail the right check**. The tests assert both: a control that failed for the wrong reason would prove nothing about the check it was meant to test.

## Three checks worth a closer look

**Strength.** G9 claims that attacks succeed rarely, and states how rarely: below 0.5%. The evidence is 0 successes in 1,440 attempts, and by the rule of three that supports "below about 0.21%", so the claim holds. Tighten the claim to 0.1% (`weak-bound`) and the same evidence no longer supports it: you need about 3,000 clean attempts. The check turns "we tested a lot" into a calculation.

**Evaluators.** E1 (correctness 0.926) and E2 (groundedness 1.0) are produced by an automated grader. They name E3, the judge's validation against human labels, as the evidence that the grader can be trusted. Remove the link (`unvalidated-evaluator`) and E1 stops counting: a score is only as good as the instrument that produced it.

**Independence.** Critical claims need at least two different methods. G7 (evaluators are trustworthy) rests on three: agreement with human labels, a bias battery and drift monitoring. Remove two (`single-method`) and it fails. Two methods are not two sources of truth, but they are much less likely to share the same blind spot.

## Takeaways

- **An assurance case can be tested like code.** Write checks for the ways arguments fail.
- **Prove every check with a broken case that must fail, for the right reason.**
- **Make strength a calculation** and evaluator trust a link, not an assumption.
