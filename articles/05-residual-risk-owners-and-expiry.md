# 05. Residual Risk: Owners, Monitoring and Expiry

> **Series:** AI Assurance Case Lab · [Index](../README.md#articles) · Previous: [04](04-defeaters-evidence-against-your-own-claim.md) · Next: [06. Mapping to the Frameworks](06-mapping-to-the-frameworks.md)

No AI system ships without known weaknesses. The question is whether those weaknesses are **accepted on purpose**, by someone with the authority to accept them, with a reason, a way of watching them and a date when the acceptance must be reviewed. A residual risk register makes that explicit.

## The register

| Risk | Owner | Rationale | Monitoring | Expires |
|---|---|---|---|---|
| R1: three known answer failures remain | Head of Support Quality | low impact, answers cite their source; fixes scheduled | groundedness and refusal monitors; the cases stay in the regression suite | 2027-02-05 |
| R2: refund requests without "refund" can be mis-routed | Agent Platform Lead | the failure is safe: no action is taken, the customer is asked again | unresolved-conversation rate by intent | 2027-02-05 |
| R3: small latency incidents may be detected a day late | SRE Lead | incidents of 8% and above are detected on onset day in every seed | p95 latency alert; weekly review | 2027-02-05 |
| R4: the judge was validated on 24 labels and beats the human ceiling | Evaluation Lead | passed bias and drift checks; a 200-item held-out set is scheduled | anchor-set drift monitor | 2027-02-05 |
| R5: reworded contamination is only partly detected | Data Lead | thresholds include margin; an embedding-based check is scheduled | production accuracy compared with eval accuracy | 2027-02-05 |
| R6: fairness across customer groups is not measured | Responsible AI Lead | no decisions about individuals; revisit if that changes | complaint and escalation rates by language and region | 2027-02-05 |

Owners are **roles**, not names: the case should survive people changing jobs.

## Four rules the checks enforce

1. **Every risk has an owner, a rationale and monitoring.** An accepted risk without an owner is not accepted; it is ignored. Without monitoring, nobody will know when the risk has grown.
2. **Every acceptance expires.** Each risk here expires 90 days after acceptance. On that date the case fails (the `expired-risk` negative control sets R3's expiry in the past) until the owner reviews it: renew with a new date and reason, or fix the problem. Acceptances that never expire become permanent by default.
3. **Every risk is tied to a claim**, so a reviewer can see which part of the argument it weakens.
4. **Every accepted defeater points at a risk** (article 04), and every scope exclusion has one too. R6 exists because the case *excludes* fairness from scope; the exclusion is a decision, and decisions need owners.

## How the decision uses the register

The decision has three outcomes:

| Decision | When |
|---|---|
| **GO** | every check passes and nothing is accepted |
| **GO WITH ACCEPTED RISKS** | every check passes, and the register is not empty |
| **NO-GO** | any check fails, including an expired or incomplete risk |

This case's decision is **GO WITH ACCEPTED RISKS**. That is the normal outcome for a real system, and the honest one. A clean GO should make a reviewer more suspicious, not less.

## Takeaways

- **Accept residual risks on purpose**: an owner, a reason, monitoring and an expiry.
- **Make acceptances expire**, so they are reviewed rather than forgotten.
- **Scope exclusions are decisions.** Give them owners too.
- **"GO with accepted risks" is the normal, honest outcome.**
