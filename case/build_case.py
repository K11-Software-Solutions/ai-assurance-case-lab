"""Source of case/assurance_case.json. Edit here, run `python case/build_case.py`, commit both.

Writing the case in Python keeps it readable (comments, shared constants) while the checked
artefact stays plain JSON that any tool can read.
"""
import json
from pathlib import Path

SUMMARY = "experiments/results/summary.md"
VERSION, DATE = "2.3.0", "2026-11-07"


def ev(id, claim, lab, file, quote, kind, method, **extra):
    return {"id": id, "claim": claim, "lab": lab, "file": file, "quote": quote, "kind": kind, "method": method,
            "system_version": VERSION, "collected": DATE, **extra}


case = {
    "system": "Orbitly Support Assistant",
    "version": VERSION,
    "assessment_date": DATE,
    "max_evidence_age_days": 90,
    "context": [
        "C1: The assistant answers customers from help articles (RAG), acts through tools and MCP servers, "
        "coordinates three agents for refunds, and is monitored in production.",
        "C2: Every evidence item comes from the K11 teaching labs, most of them with simulated components. "
        "This case is a WORKED TEMPLATE showing how to argue from evidence; it is not an assurance of any real system.",
    ],
    "scope_exclusions": [
        {"characteristic": "fair with harmful bias managed",
         "justification": "The assistant answers product questions and makes no decisions about individuals; no lab in the "
                          "evidence base measures fairness across customer groups. Excluded for this release, and recorded "
                          "as residual risk R6 so the exclusion has an owner and an expiry."},
    ],
    "claims": [
        {"id": "G0", "parent": None, "text": "Orbitly Support Assistant 2.3.0 is acceptably safe, effective and controllable for release to customers.",
         "strategy": "Argue over each quality attribute, with evidence from the lab that tests it; accept stated residual risks.",
         "critical": True, "frameworks": {"eu_ai_act": ["Art. 9", "Art. 11"], "nist_functions": ["GOVERN", "MAP"], "iso42001": ["6"],
                                          "nist_characteristics": ["accountable and transparent"]}},
        {"id": "G1", "parent": "G0", "text": "Answers are correct, grounded in the help articles, and cite the article they came from.",
         "critical": True,
         "frameworks": {"eu_ai_act": ["Art. 13", "Art. 15"], "nist_functions": ["MEASURE"], "iso42001": ["9"],
                        # Added after the coverage check found no claim for explainability (article 06):
                        # for a support assistant, explaining an answer means citing its source.
                        "nist_characteristics": ["valid and reliable", "explainable and interpretable"]}},
        {"id": "G2", "parent": "G0", "text": "The model is fit for purpose and does not memorise or leak training secrets.", "critical": False,
         "frameworks": {"eu_ai_act": ["Art. 15"], "nist_functions": ["MEASURE"], "iso42001": ["8"],
                        "nist_characteristics": ["safe", "privacy-enhanced"]}},
        {"id": "G3", "parent": "G0", "text": "Actions the assistant takes in the world are the ones the customer asked for.", "critical": True,
         "frameworks": {"eu_ai_act": ["Art. 15"], "nist_functions": ["MEASURE", "MANAGE"], "iso42001": ["8"],
                        "nist_characteristics": ["safe"]}},
        {"id": "G4", "parent": "G0", "text": "The three-agent refund flow never pays twice and failures can be attributed.", "critical": True,
         "frameworks": {"eu_ai_act": ["Art. 15"], "nist_functions": ["MEASURE"], "iso42001": ["8"],
                        "nist_characteristics": ["valid and reliable", "accountable and transparent"]}},
        {"id": "G5", "parent": "G0", "text": "Production behaviour is recorded and incidents are detected and fed back into tests.", "critical": False,
         "frameworks": {"eu_ai_act": ["Art. 12"], "nist_functions": ["MANAGE"], "iso42001": ["9", "10"],
                        "nist_characteristics": ["accountable and transparent"]}},
        {"id": "G6", "parent": "G0", "text": "Performance and cost stay within service levels and budgets under expected load.", "critical": False,
         "frameworks": {"eu_ai_act": ["Art. 15"], "nist_functions": ["MEASURE"], "iso42001": ["9"],
                        "nist_characteristics": ["valid and reliable"]}},
        {"id": "G7", "parent": "G0", "text": "The automated evaluators used as evidence are themselves trustworthy.", "critical": True,
         "frameworks": {"eu_ai_act": ["Art. 15"], "nist_functions": ["MEASURE"], "iso42001": ["9"],
                        "nist_characteristics": ["valid and reliable"]}},
        {"id": "G8", "parent": "G0", "text": "Eval data, training data and the knowledge base are fit for use.", "critical": True,
         "frameworks": {"eu_ai_act": ["Art. 10"], "nist_functions": ["MAP", "MEASURE"], "iso42001": ["8"],
                        "nist_characteristics": ["valid and reliable", "privacy-enhanced"]}},
        {"id": "G9", "parent": "G0", "text": "Attackers cannot make the assistant leak data, misuse tools or run up costs.", "critical": True,
         "required_bound": 0.005,
         "frameworks": {"eu_ai_act": ["Art. 15"], "nist_functions": ["MEASURE", "MANAGE"], "iso42001": ["8"],
                        "nist_characteristics": ["secure and resilient"]}},
        {"id": "G10", "parent": "G0", "text": "Third-party tools reached through MCP cannot hijack the assistant.", "critical": True,
         "frameworks": {"eu_ai_act": ["Art. 15"], "nist_functions": ["MANAGE"], "iso42001": ["8"],
                        "nist_characteristics": ["secure and resilient"]}},
        {"id": "G11", "parent": "G0", "text": "When the system cannot complete a task safely, it stops and hands over to a person.", "critical": False,
         "frameworks": {"eu_ai_act": ["Art. 14"], "nist_functions": ["GOVERN", "MANAGE"], "iso42001": ["8"],
                        "nist_characteristics": ["safe", "accountable and transparent"]}},
    ],
    "evidence": [
        ev("E1", "G1", "quality", "docs/sample-reports/eval-report.md", "| correctness | 0.926 | >= 0.9 ✅ |", "gate", "golden-set eval",
           relies_on_evaluator="E3"),
        ev("E2", "G1", "quality", "docs/sample-reports/eval-report.md", "| groundedness | 1.0 | >= 0.95 ✅ |", "gate", "groundedness metric",
           relies_on_evaluator="E3"),
        ev("E3", "G7", "quality", "docs/sample-reports/judge-report.md", "Judge agreement gate passed (kappa >= 0.5).", "gate", "judge vs human labels"),
        ev("E4", "G2", "model", "README.md", "scrubbing it before training prevents that.", "documented-finding", "memorisation test"),
        ev("E5", "G2", "model", "README.md", "Simulated int8 weights barely change the model", "documented-finding", "quantization drift"),
        ev("E6", "G3", "agent", "README.md", "Evaluations on world state caught it.", "documented-finding", "world-state evaluation"),
        ev("E7", "G3", "multi_agent", SUMMARY, "| triage=relay | on | 0.94 | 0 | 0 | 0 | 0 |", "measurement", "handoff contract enforcement"),
        ev("E8", "G4", "multi_agent", SUMMARY, "| same key | partial refund ($20) | 0.5 | 0 | 0.0 | 0 |", "measurement", "idempotency under ambiguous timeouts",
           successes=0, n=200),
        ev("E9", "G4", "multi_agent", SUMMARY, "first violation exact 0.67, names a faulty agent 1.00", "measurement", "blame assignment"),
        ev("E10", "G5", "monitoring", SUMMARY, "| standard (p95, z>=3 + min effect) | 0.957 ± 0.020 |", "measurement", "incident detection across seeds"),
        ev("E11", "G5", "monitoring", SUMMARY, "- Recall: 0.995 ± 0.001", "measurement", "online groundedness evaluator"),
        ev("E12", "G6", "performance", SUMMARY, "| route by intent (default) | 0.00431 | 0.924 |", "measurement", "cost per resolved request"),
        ev("E13", "G6", "performance", SUMMARY, "| short burst (20 rps for 10 s) | backoff | 0.0046 |", "measurement", "burst load with backoff"),
        ev("E14", "G7", "evaluation", SUMMARY, "| fair, counterbalanced | alpha > beta > gamma > delta | True |", "measurement", "judge bias battery"),
        ev("E15", "G7", "evaluation", SUMMARY, "| sudden: +0.15 on day 10 | 0.0 | 0.43 | 11.0 | 0.0 | 0.9 | 9.0 |", "measurement", "judge drift monitoring"),
        ev("E16", "G8", "data", SUMMARY, "| 5 stale documents | 5 | 0 | 0.844 | 1.0 | 1.0 |", "measurement", "corpus health check"),
        ev("E17", "G8", "data", SUMMARY, "| 0.15 | 4.1 | 0.86 | 1.0 | 0 |", "measurement", "label audit"),
        ev("E18", "G9", "security", SUMMARY, "| all layers (recommended) | 0.0 | none | 0.0 |", "measurement", "static attack suite, 20 repeats",
           successes=0, n=1440),
        ev("E19", "G9", "security", SUMMARY, "| low | 0.333 | 0.0 | 0.0 | 0.0 |", "measurement", "input filter utility"),
        ev("E20", "G10", "mcp", SUMMARY, "| collider | 100% harm / 100% done | 0% harm / 100% done |", "measurement", "host red team: collisions"),
        ev("E21", "G10", "mcp", SUMMARY, "| paraphrased | 0 | 66% harm / 100% done | 66% harm / 100% done | 0% harm / 34% done | 0% harm / 34% done |",
           "measurement", "host red team: tool poisoning"),
        ev("E22", "G11", "multi_agent", SUMMARY, "| triage=lossy | on | 0.5 | 0 | 0 | 0 | 8 |", "measurement", "loop stop and escalation"),
        ev("E23", "G11", "agent", "README.md", "escalate to a human", "documented-finding", "agent escalation path"),
        ev("E24", "G2", "security", SUMMARY, "| all layers (recommended) | 0.0 | none | 0.0 |", "measurement", "jailbreak output blocked by layers"),
        ev("E25", "G1", "quality", "docs/sample-reports/eval-report.md", "| citation_validity | 1.0 | >= 1.0 ✅ |", "gate", "citation check"),
    ],
    "defeaters": [
        {"id": "D1", "claim": "G1", "lab": "quality", "file": "docs/sample-reports/eval-report.md",
         "quote": "Known failure: the extractive model picks the 'how to request' sentence.",
         "text": "Known failing eval cases: a refund-deadline question, an unanswerable question answered, a paraphrase refused.",
         "resolution": {"type": "accepted", "risk": "R1"}},
        {"id": "D2", "claim": "G2", "lab": "model", "file": "README.md",
         "quote": "SmolLM2-135M complies with harmful requests",
         "text": "The model on its own complies with harmful requests.",
         "resolution": {"type": "rebutted", "by": ["E24"],
                        "note": "The model is never exposed alone: with all security layers on, no jailbreak output reached a user in 1,440 attempts."}},
        {"id": "D3", "claim": "G3", "lab": "agent", "file": "README.md",
         "quote": "is handled as a status question: a documented known failure.",
         "text": "A refund request phrased without the word 'refund' is routed as a status question.",
         "resolution": {"type": "accepted", "risk": "R2"}},
        {"id": "D4", "claim": "G5", "lab": "monitoring", "file": SUMMARY,
         "quote": "| 0.06 | 0.74 [0.60, 0.84] | 0.02 [0.00, 0.10] |",
         "text": "A latency incident affecting 6% of requests is detected on onset day only 74% of the time.",
         "resolution": {"type": "accepted", "risk": "R3"}},
        {"id": "D5", "claim": "G7", "lab": "quality", "file": "docs/sample-reports/judge-report.md",
         "quote": "the judge (kappa 0.74) agrees with the final labels more than the reviewers agree with each other",
         "text": "The judge beats the human ceiling on 24 labels: possible overfitting, and a wide interval.",
         "resolution": {"type": "accepted", "risk": "R4"}},
        {"id": "D6", "claim": "G8", "lab": "data", "file": SUMMARY,
         "quote": "| 0.1 | 0.715 | 5.0 | 1.0 | 0.2 | 0.6 | 49 | 0.698 |",
         "text": "About 40% of reworded eval leaks escape the contamination check, so measured accuracy may be inflated.",
         "resolution": {"type": "accepted", "risk": "R5"}},
    ],
    "residual_risks": [
        {"id": "R1", "claim": "G1", "text": "Three known answer failures remain (refund deadline, an unanswerable question, a paraphrase).",
         "owner": "Head of Support Quality", "accepted_on": DATE, "expires": "2027-02-05",
         "rationale": "Each is low impact and the answer cites its source; fixes are scheduled for 2.4.",
         "monitoring": "Groundedness and refusal monitors in production; the three cases stay in the regression suite."},
        {"id": "R2", "claim": "G3", "text": "Refund requests without the word 'refund' can be mis-routed as status questions.",
         "owner": "Agent Platform Lead", "accepted_on": DATE, "expires": "2027-02-05",
         "rationale": "The failure is safe (no action is taken); the customer is asked again.",
         "monitoring": "Unresolved-conversation rate by intent."},
        {"id": "R3", "claim": "G5", "text": "Small latency incidents (about 6% of requests) may be detected a day late.",
         "owner": "SRE Lead", "accepted_on": DATE, "expires": "2027-02-05",
         "rationale": "Larger incidents (8% and above) are detected on onset day in every seed.",
         "monitoring": "p95 latency alert; weekly review of the latency distribution."},
        {"id": "R4", "claim": "G7", "text": "The groundedness judge was validated on 24 labels, beats the human ceiling and has a wide interval.",
         "owner": "Evaluation Lead", "accepted_on": DATE, "expires": "2027-02-05",
         "rationale": "The judge passed bias and drift checks in the evaluation science lab; a 200-item held-out label set is scheduled.",
         "monitoring": "Anchor-set CUSUM drift monitor on the judge."},
        {"id": "R5", "claim": "G8", "text": "Reworded contamination is only partly detected; eval scores may be inflated by a few points.",
         "owner": "Data Lead", "accepted_on": DATE, "expires": "2027-02-05",
         "rationale": "Release thresholds include margin; an embedding-based contamination check is scheduled.",
         "monitoring": "Production accuracy estimate compared with eval accuracy each release."},
        {"id": "R6", "claim": "G0", "text": "Fairness across customer groups is not measured (scope exclusion).",
         "owner": "Responsible AI Lead", "accepted_on": DATE, "expires": "2027-02-05",
         "rationale": "No decisions about individuals; revisit if the assistant gains eligibility, pricing or account-action decisions.",
         "monitoring": "Complaint and escalation rates by language and region."},
    ],
}

out = Path(__file__).parent / "assurance_case.json"
out.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out}: {len(case['claims'])} claims, {len(case['evidence'])} evidence items, "
      f"{len(case['defeaters'])} defeaters, {len(case['residual_risks'])} residual risks")
