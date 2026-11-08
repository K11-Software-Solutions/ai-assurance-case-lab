"""Check the assurance case and write the release decision.

Usage (from the repo root):

    python -m evals.run_case                              # the committed case: must reach a decision
    CASE_VARIANT=stale-evidence python -m evals.run_case  # a broken case: must FAIL (NO-GO)

Writes evals/results/release_decision.md and .json. The committed copy of the decision lives
in docs/release-decision.md, regenerated with --publish.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from pathlib import Path

from assurance.checks import (EU_AI_ACT, ISO_42001, NIST_CHARACTERISTICS, NIST_FUNCTIONS, decision, load, run_all)
from assurance.snapshot import sources

ROOT = Path(__file__).resolve().parent.parent
CASE = ROOT / "case" / "assurance_case.json"
HERE = Path(__file__).parent


def _ev(case, eid):
    return next(e for e in case["evidence"] if e["id"] == eid)


def _set(case, kind, iid, **changes):
    next(x for x in case[kind] if x["id"] == iid).update(changes)


VARIANTS = {
    "missing-evidence": lambda c: c.update(evidence=[e for e in c["evidence"] if e["claim"] != "G6"]),
    "broken-trace": lambda c: _ev(c, "E18").update(quote="| all layers (recommended) | 0.01 | none | 0.0 |"),
    "tampered-snapshot": None,      # handled through overrides
    "stale-evidence": lambda c: _ev(c, "E10").update(system_version="2.2.0"),
    "old-evidence": lambda c: _ev(c, "E12").update(collected="2026-05-01"),
    "weak-bound": lambda c: _set(c, "claims", "G9", required_bound=0.001),
    "single-method": lambda c: c.update(evidence=[e for e in c["evidence"] if e["id"] not in ("E14", "E15")]),
    "prose-only": lambda c: c.update(evidence=[e for e in c["evidence"] if e["id"] != "E7"]),
    "unvalidated-evaluator": lambda c: _ev(c, "E1").update(relies_on_evaluator=None),
    "unresolved-defeater": lambda c: _set(c, "defeaters", "D2", resolution=None),
    "expired-risk": lambda c: _set(c, "residual_risks", "R3", expires="2026-11-01"),
    "coverage-gap": lambda c: next(x for x in c["claims"] if x["id"] == "G11")["frameworks"].update(eu_ai_act=[]),
    "no-scope-exclusion": lambda c: c.update(scope_exclusions=[]),
}
EXPECTED = {"missing-evidence": "structure", "broken-trace": "traceability", "tampered-snapshot": "traceability",
            "stale-evidence": "freshness", "old-evidence": "freshness", "weak-bound": "strength",
            "single-method": "independence", "prose-only": "independence", "unvalidated-evaluator": "evaluators",
            "unresolved-defeater": "defeaters", "expired-risk": "residual_risks", "coverage-gap": "coverage",
            "no-scope-exclusion": "coverage"}


def build(variant: str) -> tuple[dict, dict]:
    case = load(CASE)
    overrides = {}
    if variant == "tampered-snapshot":
        overrides["_tamper"] = "ai-security-testing-lab/experiments/results/summary.md"
    elif variant:
        case = copy.deepcopy(case)
        VARIANTS[variant](case)
    return case, overrides


def link(lab: str, file: str) -> str:
    s = sources()[lab]
    return f"[{s['repo']}@{s['commit'][:7]}/{file}](https://github.com/K11-Software-Solutions/{s['repo']}/blob/{s['commit']}/{file})"


def report(case: dict, results: dict, verdict: str, variant: str) -> str:
    claims = case["claims"]
    L = [f"# Release decision: {case['system']} {case['version']}", "",
         f"**Decision: {verdict}**" + (f"  (variant `{variant}`)" if variant else ""), "",
         f"Assessed {case['assessment_date']}. Evidence pinned to the v1.0.0 release commit and DOI of each source lab.", ""]
    L += [f"> {c}" for c in case["context"]] + [""]
    L += ["## Checks on the case", "", "| Check | Result |", "|---|---|"]
    L += [f"| {k} | {'pass' if not v else '**' + str(len(v)) + ' problem(s)**'} |" for k, v in results.items()]
    problems = [p for v in results.values() for p in v]
    if problems:
        L += ["", "Problems:", ""] + [f"- {p}" for p in problems]
    L += ["", "## Claims and evidence", ""]
    for c in claims:
        items = [e for e in case["evidence"] if e["claim"] == c["id"]]
        kinds = sorted({e["kind"] for e in items})
        tag = " (critical)" if c.get("critical") else ""
        L += [f"### {c['id']}{tag}: {c['text']}", ""]
        if c.get("strategy"):
            L += [f"*Strategy:* {c['strategy']}", ""]
        if items:
            L += [f"Evidence ({', '.join(kinds)}):", ""]
            for e in items:
                extra = f"; 0 failures in {e['n']}" if e.get("successes") == 0 and e.get("n") else ""
                L.append(f"- **{e['id']}** {e['method']} ({e['kind']}{extra}): `{e['quote']}`, {link(e['lab'], e['file'])}")
        for d in [d for d in case["defeaters"] if d["claim"] == c["id"]]:
            r = d.get("resolution") or {}
            how = (f"rebutted by {', '.join(r['by'])}: {r.get('note', '')}" if r.get("type") == "rebutted"
                   else f"accepted as residual risk {r.get('risk')}" if r.get("type") == "accepted" else "**unresolved**")
            L.append(f"- *Defeater {d['id']}:* {d['text']} (`{d['quote']}`, {link(d['lab'], d['file'])}); {how}")
        L.append("")
    L += ["## Residual risk register", "", "| Risk | Claim | Owner | Expires | Rationale | Monitoring |", "|---|---|---|---|---|---|"]
    L += [f"| {r['id']}: {r['text']} | {r['claim']} | {r['owner']} | {r['expires']} | {r['rationale']} | {r['monitoring']} |"
          for r in case["residual_risks"]]
    L += ["", "## Framework coverage", "", "| Framework | Item | Claims |", "|---|---|---|"]
    for fw, items, key in (("EU AI Act", EU_AI_ACT, "eu_ai_act"), ("NIST AI RMF", NIST_FUNCTIONS, "nist_functions"),
                           ("ISO/IEC 42001 clause", ISO_42001, "iso42001"), ("NIST characteristic", NIST_CHARACTERISTICS, "nist_characteristics")):
        for it in items:
            by = [c["id"] for c in claims if it in c.get("frameworks", {}).get(key, [])]
            excl = [x for x in case.get("scope_exclusions", []) if x["characteristic"] == it]
            L.append(f"| {fw} | {it} | {', '.join(by) if by else ('excluded: see scope exclusions' if excl else '**none**')} |")
    if case.get("scope_exclusions"):
        L += ["", "Scope exclusions:", ""] + [f"- **{x['characteristic']}**: {x['justification']}" for x in case["scope_exclusions"]]
    L += ["", "Framework mappings are at the level of articles, functions, clauses and characteristics. They show where "
          "evidence is relevant; they are not a legal or certification assessment.", ""]
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=HERE / "results")
    parser.add_argument("--publish", action="store_true", help="also write docs/release-decision.md")
    args = parser.parse_args(argv)
    variant = os.environ.get("CASE_VARIANT", "")
    if variant and variant not in VARIANTS:
        raise SystemExit(f"unknown CASE_VARIANT '{variant}'; choose from {', '.join(VARIANTS)}")
    case, overrides = build(variant)
    results = run_all(case, overrides)
    verdict = decision(results, case)
    text = report(case, results, verdict, variant)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "release_decision.md").write_text(text, encoding="utf-8")
    (args.out / "release_decision.json").write_text(json.dumps({"variant": variant, "decision": verdict, "checks": results},
                                                              indent=2), encoding="utf-8")
    if args.publish:
        (ROOT / "docs").mkdir(exist_ok=True)
        (ROOT / "docs" / "release-decision.md").write_text(text, encoding="utf-8")
    print(text)
    if verdict == "NO-GO":
        print("Assurance case FAILED: NO-GO", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
