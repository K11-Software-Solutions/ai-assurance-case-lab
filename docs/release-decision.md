# Release decision: Orbitly Support Assistant 2.3.0

**Decision: GO WITH ACCEPTED RISKS**

Assessed 2026-11-07. Evidence pinned to the v1.0.0 release commit and DOI of each source lab.

> C1: The assistant answers customers from help articles (RAG), acts through tools and MCP servers, coordinates three agents for refunds, and is monitored in production.
> C2: Every evidence item comes from the K11 teaching labs, most of them with simulated components. This case is a WORKED TEMPLATE showing how to argue from evidence; it is not an assurance of any real system.

## Checks on the case

| Check | Result |
|---|---|
| structure | pass |
| traceability | pass |
| freshness | pass |
| independence | pass |
| strength | pass |
| evaluators | pass |
| defeaters | pass |
| residual_risks | pass |
| coverage | pass |

## Claims and evidence

### G0 (critical): Orbitly Support Assistant 2.3.0 is acceptably safe, effective and controllable for release to customers.

*Strategy:* Argue over each quality attribute, with evidence from the lab that tests it; accept stated residual risks.


### G1 (critical): Answers are correct, grounded in the help articles, and cite the article they came from.

Evidence (gate):

- **E1** golden-set eval (gate): `| correctness | 0.926 | >= 0.9 ✅ |`, [becoming-ai-quality-engineer@0e2e0e4/docs/sample-reports/eval-report.md](https://github.com/K11-Software-Solutions/becoming-ai-quality-engineer/blob/0e2e0e49c1bc7af99668fb4682ef9798478fb7bf/docs/sample-reports/eval-report.md)
- **E2** groundedness metric (gate): `| groundedness | 1.0 | >= 0.95 ✅ |`, [becoming-ai-quality-engineer@0e2e0e4/docs/sample-reports/eval-report.md](https://github.com/K11-Software-Solutions/becoming-ai-quality-engineer/blob/0e2e0e49c1bc7af99668fb4682ef9798478fb7bf/docs/sample-reports/eval-report.md)
- **E25** citation check (gate): `| citation_validity | 1.0 | >= 1.0 ✅ |`, [becoming-ai-quality-engineer@0e2e0e4/docs/sample-reports/eval-report.md](https://github.com/K11-Software-Solutions/becoming-ai-quality-engineer/blob/0e2e0e49c1bc7af99668fb4682ef9798478fb7bf/docs/sample-reports/eval-report.md)
- *Defeater D1:* Known failing eval cases: a refund-deadline question, an unanswerable question answered, a paraphrase refused. (`Known failure: the extractive model picks the 'how to request' sentence.`, [becoming-ai-quality-engineer@0e2e0e4/docs/sample-reports/eval-report.md](https://github.com/K11-Software-Solutions/becoming-ai-quality-engineer/blob/0e2e0e49c1bc7af99668fb4682ef9798478fb7bf/docs/sample-reports/eval-report.md)); accepted as residual risk R1

### G2: The model is fit for purpose and does not memorise or leak training secrets.

Evidence (documented-finding, measurement):

- **E4** memorisation test (documented-finding): `scrubbing it before training prevents that.`, [llm-model-testing-lab@36b32a6/README.md](https://github.com/K11-Software-Solutions/llm-model-testing-lab/blob/36b32a6bd624cfd9ed8f9ed66f59ff447fdf843f/README.md)
- **E5** quantization drift (documented-finding): `Simulated int8 weights barely change the model`, [llm-model-testing-lab@36b32a6/README.md](https://github.com/K11-Software-Solutions/llm-model-testing-lab/blob/36b32a6bd624cfd9ed8f9ed66f59ff447fdf843f/README.md)
- **E24** jailbreak output blocked by layers (measurement): `| all layers (recommended) | 0.0 | none | 0.0 |`, [ai-security-testing-lab@d815003/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-security-testing-lab/blob/d815003dc2fce9dfcf1b02c01a0e56681f8e23b2/experiments/results/summary.md)
- *Defeater D2:* The model on its own complies with harmful requests. (`SmolLM2-135M complies with harmful requests`, [llm-model-testing-lab@36b32a6/README.md](https://github.com/K11-Software-Solutions/llm-model-testing-lab/blob/36b32a6bd624cfd9ed8f9ed66f59ff447fdf843f/README.md)); rebutted by E24: The model is never exposed alone: with all security layers on, no jailbreak output reached a user in 1,440 attempts.

### G3 (critical): Actions the assistant takes in the world are the ones the customer asked for.

Evidence (documented-finding, measurement):

- **E6** world-state evaluation (documented-finding): `Evaluations on world state caught it.`, [agent-testing-lab@851355c/README.md](https://github.com/K11-Software-Solutions/agent-testing-lab/blob/851355c675279f8bccb363ba60d5fa2f067632e9/README.md)
- **E7** handoff contract enforcement (measurement): `| triage=relay | on | 0.94 | 0 | 0 | 0 | 0 |`, [multi-agent-testing-lab@6a17a3d/experiments/results/summary.md](https://github.com/K11-Software-Solutions/multi-agent-testing-lab/blob/6a17a3dd037916e86827a9437cc7c80cc297fb5b/experiments/results/summary.md)
- *Defeater D3:* A refund request phrased without the word 'refund' is routed as a status question. (`is handled as a status question: a documented known failure.`, [agent-testing-lab@851355c/README.md](https://github.com/K11-Software-Solutions/agent-testing-lab/blob/851355c675279f8bccb363ba60d5fa2f067632e9/README.md)); accepted as residual risk R2

### G4 (critical): The three-agent refund flow never pays twice and failures can be attributed.

Evidence (measurement):

- **E8** idempotency under ambiguous timeouts (measurement; 0 failures in 200): `| same key | partial refund ($20) | 0.5 | 0 | 0.0 | 0 |`, [multi-agent-testing-lab@6a17a3d/experiments/results/summary.md](https://github.com/K11-Software-Solutions/multi-agent-testing-lab/blob/6a17a3dd037916e86827a9437cc7c80cc297fb5b/experiments/results/summary.md)
- **E9** blame assignment (measurement): `first violation exact 0.67, names a faulty agent 1.00`, [multi-agent-testing-lab@6a17a3d/experiments/results/summary.md](https://github.com/K11-Software-Solutions/multi-agent-testing-lab/blob/6a17a3dd037916e86827a9437cc7c80cc297fb5b/experiments/results/summary.md)

### G5: Production behaviour is recorded and incidents are detected and fed back into tests.

Evidence (measurement):

- **E10** incident detection across seeds (measurement): `| standard (p95, z>=3 + min effect) | 0.957 ± 0.020 |`, [ai-production-monitoring-lab@15be57c/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-production-monitoring-lab/blob/15be57cc1b36d46f79fb238ebcc75be465b4f5bc/experiments/results/summary.md)
- **E11** online groundedness evaluator (measurement): `- Recall: 0.995 ± 0.001`, [ai-production-monitoring-lab@15be57c/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-production-monitoring-lab/blob/15be57cc1b36d46f79fb238ebcc75be465b4f5bc/experiments/results/summary.md)
- *Defeater D4:* A latency incident affecting 6% of requests is detected on onset day only 74% of the time. (`| 0.06 | 0.74 [0.60, 0.84] | 0.02 [0.00, 0.10] |`, [ai-production-monitoring-lab@15be57c/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-production-monitoring-lab/blob/15be57cc1b36d46f79fb238ebcc75be465b4f5bc/experiments/results/summary.md)); accepted as residual risk R3

### G6: Performance and cost stay within service levels and budgets under expected load.

Evidence (measurement):

- **E12** cost per resolved request (measurement): `| route by intent (default) | 0.00431 | 0.924 |`, [ai-performance-cost-lab@0ff821a/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-performance-cost-lab/blob/0ff821a41fabca934d7d2555fe5e06ccf00bbd89/experiments/results/summary.md)
- **E13** burst load with backoff (measurement): `| short burst (20 rps for 10 s) | backoff | 0.0046 |`, [ai-performance-cost-lab@0ff821a/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-performance-cost-lab/blob/0ff821a41fabca934d7d2555fe5e06ccf00bbd89/experiments/results/summary.md)

### G7 (critical): The automated evaluators used as evidence are themselves trustworthy.

Evidence (gate, measurement):

- **E3** judge vs human labels (gate): `Judge agreement gate passed (kappa >= 0.5).`, [becoming-ai-quality-engineer@0e2e0e4/docs/sample-reports/judge-report.md](https://github.com/K11-Software-Solutions/becoming-ai-quality-engineer/blob/0e2e0e49c1bc7af99668fb4682ef9798478fb7bf/docs/sample-reports/judge-report.md)
- **E14** judge bias battery (measurement): `| fair, counterbalanced | alpha > beta > gamma > delta | True |`, [ai-evaluation-science-lab@a83bdd8/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-evaluation-science-lab/blob/a83bdd83c8cdf09cd6185afd52c772f8650aec41/experiments/results/summary.md)
- **E15** judge drift monitoring (measurement): `| sudden: +0.15 on day 10 | 0.0 | 0.43 | 11.0 | 0.0 | 0.9 | 9.0 |`, [ai-evaluation-science-lab@a83bdd8/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-evaluation-science-lab/blob/a83bdd83c8cdf09cd6185afd52c772f8650aec41/experiments/results/summary.md)
- *Defeater D5:* The judge beats the human ceiling on 24 labels: possible overfitting, and a wide interval. (`the judge (kappa 0.74) agrees with the final labels more than the reviewers agree with each other`, [becoming-ai-quality-engineer@0e2e0e4/docs/sample-reports/judge-report.md](https://github.com/K11-Software-Solutions/becoming-ai-quality-engineer/blob/0e2e0e49c1bc7af99668fb4682ef9798478fb7bf/docs/sample-reports/judge-report.md)); accepted as residual risk R4

### G8 (critical): Eval data, training data and the knowledge base are fit for use.

Evidence (measurement):

- **E16** corpus health check (measurement): `| 5 stale documents | 5 | 0 | 0.844 | 1.0 | 1.0 |`, [ai-data-quality-lab@b53f47b/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-data-quality-lab/blob/b53f47b5d77bf2c93cec217091c60aabe8f8e579/experiments/results/summary.md)
- **E17** label audit (measurement): `| 0.15 | 4.1 | 0.86 | 1.0 | 0 |`, [ai-data-quality-lab@b53f47b/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-data-quality-lab/blob/b53f47b5d77bf2c93cec217091c60aabe8f8e579/experiments/results/summary.md)
- *Defeater D6:* About 40% of reworded eval leaks escape the contamination check, so measured accuracy may be inflated. (`| 0.1 | 0.715 | 5.0 | 1.0 | 0.2 | 0.6 | 49 | 0.698 |`, [ai-data-quality-lab@b53f47b/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-data-quality-lab/blob/b53f47b5d77bf2c93cec217091c60aabe8f8e579/experiments/results/summary.md)); accepted as residual risk R5

### G9 (critical): Attackers cannot make the assistant leak data, misuse tools or run up costs.

Evidence (measurement):

- **E18** static attack suite, 20 repeats (measurement; 0 failures in 1440): `| all layers (recommended) | 0.0 | none | 0.0 |`, [ai-security-testing-lab@d815003/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-security-testing-lab/blob/d815003dc2fce9dfcf1b02c01a0e56681f8e23b2/experiments/results/summary.md)
- **E19** input filter utility (measurement): `| low | 0.333 | 0.0 | 0.0 | 0.0 |`, [ai-security-testing-lab@d815003/experiments/results/summary.md](https://github.com/K11-Software-Solutions/ai-security-testing-lab/blob/d815003dc2fce9dfcf1b02c01a0e56681f8e23b2/experiments/results/summary.md)

### G10 (critical): Third-party tools reached through MCP cannot hijack the assistant.

Evidence (measurement):

- **E20** host red team: collisions (measurement): `| collider | 100% harm / 100% done | 0% harm / 100% done |`, [mcp-testing-lab@1a54ed4/experiments/results/summary.md](https://github.com/K11-Software-Solutions/mcp-testing-lab/blob/1a54ed45d54824d8b24989a869e352a4dbdf6c49/experiments/results/summary.md)
- **E21** host red team: tool poisoning (measurement): `| paraphrased | 0 | 66% harm / 100% done | 66% harm / 100% done | 0% harm / 34% done | 0% harm / 34% done |`, [mcp-testing-lab@1a54ed4/experiments/results/summary.md](https://github.com/K11-Software-Solutions/mcp-testing-lab/blob/1a54ed45d54824d8b24989a869e352a4dbdf6c49/experiments/results/summary.md)

### G11: When the system cannot complete a task safely, it stops and hands over to a person.

Evidence (documented-finding, measurement):

- **E22** loop stop and escalation (measurement): `| triage=lossy | on | 0.5 | 0 | 0 | 0 | 8 |`, [multi-agent-testing-lab@6a17a3d/experiments/results/summary.md](https://github.com/K11-Software-Solutions/multi-agent-testing-lab/blob/6a17a3dd037916e86827a9437cc7c80cc297fb5b/experiments/results/summary.md)
- **E23** agent escalation path (documented-finding): `escalate to a human`, [agent-testing-lab@851355c/README.md](https://github.com/K11-Software-Solutions/agent-testing-lab/blob/851355c675279f8bccb363ba60d5fa2f067632e9/README.md)

## Residual risk register

| Risk | Claim | Owner | Expires | Rationale | Monitoring |
|---|---|---|---|---|---|
| R1: Three known answer failures remain (refund deadline, an unanswerable question, a paraphrase). | G1 | Head of Support Quality | 2027-02-05 | Each is low impact and the answer cites its source; fixes are scheduled for 2.4. | Groundedness and refusal monitors in production; the three cases stay in the regression suite. |
| R2: Refund requests without the word 'refund' can be mis-routed as status questions. | G3 | Agent Platform Lead | 2027-02-05 | The failure is safe (no action is taken); the customer is asked again. | Unresolved-conversation rate by intent. |
| R3: Small latency incidents (about 6% of requests) may be detected a day late. | G5 | SRE Lead | 2027-02-05 | Larger incidents (8% and above) are detected on onset day in every seed. | p95 latency alert; weekly review of the latency distribution. |
| R4: The groundedness judge was validated on 24 labels, beats the human ceiling and has a wide interval. | G7 | Evaluation Lead | 2027-02-05 | The judge passed bias and drift checks in the evaluation science lab; a 200-item held-out label set is scheduled. | Anchor-set CUSUM drift monitor on the judge. |
| R5: Reworded contamination is only partly detected; eval scores may be inflated by a few points. | G8 | Data Lead | 2027-02-05 | Release thresholds include margin; an embedding-based contamination check is scheduled. | Production accuracy estimate compared with eval accuracy each release. |
| R6: Fairness across customer groups is not measured (scope exclusion). | G0 | Responsible AI Lead | 2027-02-05 | No decisions about individuals; revisit if the assistant gains eligibility, pricing or account-action decisions. | Complaint and escalation rates by language and region. |

## Framework coverage

| Framework | Item | Claims |
|---|---|---|
| EU AI Act | Art. 9 | G0 |
| EU AI Act | Art. 10 | G8 |
| EU AI Act | Art. 11 | G0 |
| EU AI Act | Art. 12 | G5 |
| EU AI Act | Art. 13 | G1 |
| EU AI Act | Art. 14 | G11 |
| EU AI Act | Art. 15 | G1, G2, G3, G4, G6, G7, G9, G10 |
| NIST AI RMF | GOVERN | G0, G11 |
| NIST AI RMF | MAP | G0, G8 |
| NIST AI RMF | MEASURE | G1, G2, G3, G4, G6, G7, G8, G9 |
| NIST AI RMF | MANAGE | G3, G5, G9, G10, G11 |
| ISO/IEC 42001 clause | 6 | G0 |
| ISO/IEC 42001 clause | 8 | G2, G3, G4, G8, G9, G10, G11 |
| ISO/IEC 42001 clause | 9 | G1, G5, G6, G7 |
| ISO/IEC 42001 clause | 10 | G5 |
| NIST characteristic | valid and reliable | G1, G4, G6, G7, G8 |
| NIST characteristic | safe | G2, G3, G11 |
| NIST characteristic | secure and resilient | G9, G10 |
| NIST characteristic | accountable and transparent | G0, G4, G5, G11 |
| NIST characteristic | explainable and interpretable | G1 |
| NIST characteristic | privacy-enhanced | G2, G8 |
| NIST characteristic | fair with harmful bias managed | excluded: see scope exclusions |

Scope exclusions:

- **fair with harmful bias managed**: The assistant answers product questions and makes no decisions about individuals; no lab in the evidence base measures fairness across customer groups. Excluded for this release, and recorded as residual risk R6 so the exclusion has an owner and an expiry.

Framework mappings are at the level of articles, functions, clauses and characteristics. They show where evidence is relevant; they are not a legal or certification assessment.
