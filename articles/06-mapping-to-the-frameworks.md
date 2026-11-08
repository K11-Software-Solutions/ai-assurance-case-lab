# 06. Mapping to NIST AI RMF, ISO/IEC 42001 and the EU AI Act

> **Series:** AI Assurance Case Lab · [Index](../README.md#articles) · Previous: [05](05-residual-risk-owners-and-expiry.md) · Next: [07. Testing the Case](07-testing-the-case.md)

Risk teams, auditors and regulators don't think in terms of "groundedness" or "pass^k". They think in terms of frameworks. Mapping each claim to the frameworks lets the same assurance case answer their questions, and shows where the evidence has gaps.

## Three frameworks, at the level they are useful

| Framework | What the case maps to |
|---|---|
| **NIST AI Risk Management Framework (AI RMF 1.0)** | its four functions (Govern, Map, Measure, Manage) and its characteristics of trustworthy AI: valid and reliable; safe; secure and resilient; accountable and transparent; explainable and interpretable; privacy-enhanced; fair with harmful bias managed |
| **ISO/IEC 42001** (AI management systems) | the clauses on planning (6), operation (8), performance evaluation (9) and improvement (10) |
| **EU AI Act**, requirements for high-risk systems | Articles 9 (risk management), 10 (data and data governance), 11 (technical documentation), 12 (record-keeping), 13 (transparency and information to deployers), 14 (human oversight) and 15 (accuracy, robustness and cybersecurity) |

Every claim records which of these it addresses. The coverage check requires every listed article, function and clause to be addressed by at least one claim, and every NIST characteristic to be either claimed or explicitly excluded with a justification.

These mappings are deliberately coarse: articles, functions, clauses and characteristics, not individual sub-requirements. They show **where evidence is relevant**. They are not a conformity assessment, a certification or legal advice. Whether a support assistant is a high-risk system under the EU AI Act at all is a legal question this lab does not answer; the mapping is useful either way, because those articles describe good practice for any AI system.

## What coverage looks like here

A sample from the rendered decision:

| Item | Claims |
|---|---|
| EU AI Act Art. 10, data | G8 |
| EU AI Act Art. 12, record-keeping | G5 |
| EU AI Act Art. 14, human oversight | G11 |
| EU AI Act Art. 15, accuracy, robustness, cybersecurity | G1, G2, G3, G4, G6, G7, G9, G10 |
| NIST: secure and resilient | G9, G10 |
| NIST: fair with harmful bias managed | excluded (see scope exclusions) |

Article 15 is addressed by eight claims, because most testing in this series is about accuracy, robustness and security. Article 14 rests on a single claim (G11) with comparatively weak evidence (a loop-stopping measurement and a documented escalation path). Mapping makes that imbalance visible.

## The coverage check found a real gap

When the case was first written, the coverage check failed:

```text
coverage: NIST characteristic 'explainable and interpretable' is neither claimed nor excluded with a justification
```

No claim argued that the system's outputs could be explained. For a support assistant, explaining an answer mostly means **citing the article it came from**, and the quality lab gates on exactly that (`citation_validity` 1.0). The fix was to extend G1 to cover citations and add that gate result as evidence (E25). Without the check, the gap would have gone unnoticed until a reviewer asked.

## Excluding, not ignoring

Fairness is the other characteristic not covered by evidence: no lab in the series measures it across customer groups. The case does not pretend otherwise. It **excludes** it, with a justification (the assistant makes no decisions about individuals) and a residual risk (R6) with an owner who must revisit it if that changes. The `no-scope-exclusion` negative control removes the exclusion and the case fails: silence about a characteristic is not allowed.

## Takeaways

- **Map claims to the frameworks your reviewers use**, at a level you can defend.
- **Require coverage**, and treat a gap as a finding.
- **Exclude explicitly, with a reason and an owner**, never by omission.
- **Mapping is not compliance.** It shows where evidence applies; the legal assessment is separate.
