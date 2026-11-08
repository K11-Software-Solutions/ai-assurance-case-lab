# 04. Defeaters: Evidence Against Your Own Claim

> **Series:** AI Assurance Case Lab · [Index](../README.md#articles) · Previous: [03](03-evidence-you-can-trust.md) · Next: [05. Residual Risk](05-residual-risk-owners-and-expiry.md)

The most important part of an assurance case is what it says about its own weaknesses. A **defeater** is a piece of evidence or reasoning that, if left unanswered, would undermine a claim. Assurance-case practice (sometimes called *eliminative argumentation*) asks you to go looking for them, write them down, and say how each is dealt with.

## The defeaters in this case

Every lab in the series reported something that did not work. Those findings are not embarrassments to leave out of the release decision; they are its most useful content.

| Defeater | Against | Source | Resolution |
|---|---|---|---|
| D1: three known failing eval cases (a refund deadline, an unanswerable question answered, a paraphrase refused) | G1 answers are correct | quality lab eval report | accepted as R1 |
| D2: the model on its own complies with harmful requests | G2 model fit for purpose | model lab README | **rebutted** by E24 |
| D3: refund requests without the word "refund" are routed as status questions | G3 actions are the ones asked for | agent lab README | accepted as R2 |
| D4: a latency incident affecting 6% of requests is detected on onset day only 74% of the time | G5 incidents detected | monitoring lab experiments | accepted as R3 |
| D5: the judge agrees with the final labels more than two humans agree with each other, on 24 labels | G7 evaluators trustworthy | quality lab judge report | accepted as R4 |
| D6: about 40% of reworded eval leaks escape the contamination check | G8 data fit for use | data quality lab experiments | accepted as R5 |

Each defeater, like each evidence item, quotes its source line verbatim and is checked by the traceability check. A defeater is evidence too.

## Two ways to resolve a defeater

**Rebut it with other evidence.** D2 is real: the small model in the model lab does comply with harmful requests. But the claim is about the *system*, and in the system the model is never exposed on its own. The security lab's evidence (E24) shows that with all defence layers on, no jailbreak output reached a user in 1,440 attempts. The rebuttal names that evidence explicitly, and the defeaters check confirms it exists in the case. A rebuttal that points at nothing ("this is mitigated elsewhere") fails the check.

**Accept it as a residual risk.** D1, D3, D4, D5 and D6 are not rebutted: the weakness is real and still there. They are accepted, each through a residual risk with an owner, a rationale, monitoring and an expiry date (article 05). The case is honest that these problems ship.

There is no third option. A defeater left unresolved makes the case **NO-GO**: the `unresolved-defeater` negative control removes D2's rebuttal, and the gate fails.

## Finding defeaters

The defeaters here came from the labs' own "What the lab finds" sections and failing cases. For a real system, look in:

- **Known failures** in every eval report, and every test marked "expected to fail".
- **Limitations sections** of your own test documentation.
- **Negative findings from experiments**: detection rates below 100%, intervals that include unacceptable values.
- **Incidents and near misses** from production since the last release.
- **Disagreement**: evaluators that disagree with humans, reviewers who disagree with each other.

A case with no defeaters is not a strong case; it is one that has not looked.

## Takeaways

- **Write down the evidence against your claims.** It is the most valuable part of the case.
- **Resolve every defeater**: rebut it with named evidence, or accept it as a residual risk.
- **Rebuttals must point at real evidence** in the case.
- **No defeaters usually means no one looked.**
