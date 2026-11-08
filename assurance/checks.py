"""Checks on the assurance case itself. Each returns a list of problems; an empty list passes.

structure       one root; every parent exists; every claim other than the root has evidence
traceability    every evidence quote and defeater quote appears verbatim in its pinned snapshot,
                and every snapshot matches its recorded hash
freshness       evidence is about the system version under assessment, and recent enough
independence    critical claims rest on at least two different methods, and not only on
                documented findings (prose) as opposed to measurements or gates
strength        zero-failure evidence supports the claim's required bound (rule of three: 3/n)
evaluators      evidence produced by an automated evaluator names evidence that the evaluator
                was validated, and that validation is itself in the case
defeaters       every defeater is rebutted by evidence in the case or accepted as a residual risk
residual risks  every risk has an owner, a rationale, monitoring, and has not expired
coverage        EU AI Act Articles 9-15, the four NIST AI RMF functions, ISO/IEC 42001 clauses
                6, 8, 9 and 10, and every NIST trustworthiness characteristic are covered by a
                claim, or (characteristics only) excluded with a justification
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from assurance.snapshot import check as snapshot_check, snapshot_path, sources

EU_AI_ACT = ("Art. 9", "Art. 10", "Art. 11", "Art. 12", "Art. 13", "Art. 14", "Art. 15")
NIST_FUNCTIONS = ("GOVERN", "MAP", "MEASURE", "MANAGE")
ISO_42001 = ("6", "8", "9", "10")
NIST_CHARACTERISTICS = ("valid and reliable", "safe", "secure and resilient", "accountable and transparent",
                        "explainable and interpretable", "privacy-enhanced", "fair with harmful bias managed")
STRONG_KINDS = ("measurement", "gate")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _snapshot_text(case: dict, lab: str, file: str, overrides: dict) -> str | None:
    key = f"{lab}:{file}"
    if key in overrides:
        return overrides[key]
    src = sources().get(lab)
    if src is None or file not in src["files"]:
        return None
    p = snapshot_path(src["repo"], file)
    return p.read_text(encoding="utf-8") if p.is_file() else None


def structure(case: dict) -> list[str]:
    ids = {c["id"] for c in case["claims"]}
    roots = [c for c in case["claims"] if c["parent"] is None]
    out = [] if len(roots) == 1 else [f"structure: {len(roots)} root claims (need exactly one)"]
    out += [f"structure: {c['id']} has unknown parent {c['parent']}" for c in case["claims"]
            if c["parent"] is not None and c["parent"] not in ids]
    evidenced = {e["claim"] for e in case["evidence"]}
    parents = {c["parent"] for c in case["claims"]}
    out += [f"structure: {c['id']} has no evidence (undeveloped claim)" for c in case["claims"]
            if c["id"] not in parents and c["id"] not in evidenced]
    out += [f"structure: evidence {e['id']} supports unknown claim {e['claim']}" for e in case["evidence"] if e["claim"] not in ids]
    return out


def traceability(case: dict, overrides: dict | None = None) -> list[str]:
    overrides = overrides or {}
    out = [] if overrides.get("_skip_hash") else [f"traceability: {p}" for p in snapshot_check()]
    if "_tamper" in overrides:
        out.append(f"traceability: snapshot of {overrides['_tamper']} does not match its recorded hash (edited after fetching?)")
    for item in case["evidence"] + case["defeaters"]:
        text = _snapshot_text(case, item["lab"], item["file"], overrides)
        if text is None:
            out.append(f"traceability: {item['id']} cites {item['lab']}/{item['file']}, which is not a pinned snapshot")
        elif _norm(item["quote"]) not in _norm(text):
            out.append(f"traceability: {item['id']} quote not found in {sources()[item['lab']]['repo']}/{item['file']}")
    for lab, s in sources().items():
        if not re.fullmatch(r"[0-9a-f]{40}", s["commit"]) or not s.get("doi"):
            out.append(f"traceability: source '{lab}' is not pinned to a full commit and a DOI")
    return out


def as_of(case: dict, when: date | None = None) -> date:
    """The date the case is judged on: today, or the assessment date if that is later. Using today's
    date is what makes the case fail BY ITSELF when evidence goes stale or an acceptance expires."""
    return when or max(date.fromisoformat(case["assessment_date"]), date.today())


def freshness(case: dict, when: date | None = None) -> list[str]:
    today = as_of(case, when)
    out = []
    for e in case["evidence"]:
        if e["system_version"] != case["version"]:
            out.append(f"freshness: {e['id']} is evidence about version {e['system_version']}, not {case['version']}")
        age = (today - date.fromisoformat(e["collected"])).days
        if age > case["max_evidence_age_days"]:
            out.append(f"freshness: {e['id']} is {age} days old (limit {case['max_evidence_age_days']})")
    return out


def independence(case: dict) -> list[str]:
    out = []
    for c in case["claims"]:
        if not c.get("critical") or c["parent"] is None:
            continue
        items = [e for e in case["evidence"] if e["claim"] == c["id"]]
        if len({e["method"] for e in items}) < 2:
            out.append(f"independence: critical claim {c['id']} rests on {len({e['method'] for e in items})} method(s); needs 2")
        if items and not any(e["kind"] in STRONG_KINDS for e in items):
            out.append(f"independence: critical claim {c['id']} rests only on documented findings, no measurement")
    return out


def strength(case: dict) -> list[str]:
    out = []
    claims = {c["id"]: c for c in case["claims"]}
    for e in case["evidence"]:
        bound = claims.get(e["claim"], {}).get("required_bound")
        if bound is not None and e.get("successes") == 0 and e.get("n"):
            if 3 / e["n"] > bound:
                out.append(f"strength: {e['id']}: 0 failures in {e['n']} supports a rate below {3 / e['n']:.2%} "
                           f"(rule of three), but {e['claim']} requires {bound:.2%}")
    return out


def evaluators(case: dict) -> list[str]:
    ids = {e["id"]: e for e in case["evidence"]}
    out = []
    for e in case["evidence"]:
        ref = e.get("relies_on_evaluator", "absent")
        if ref == "absent":
            continue
        if ref is None or ref not in ids:
            out.append(f"evaluators: {e['id']} relies on an automated evaluator with no validation evidence in the case")
        elif ids[ref]["kind"] not in STRONG_KINDS:
            out.append(f"evaluators: {e['id']}'s evaluator validation {ref} is not a measurement or gate")
    return out


def defeaters(case: dict) -> list[str]:
    ev_ids = {e["id"] for e in case["evidence"]}
    risk_ids = {r["id"] for r in case["residual_risks"]}
    out = []
    for d in case["defeaters"]:
        r = d.get("resolution") or {}
        if r.get("type") == "rebutted" and r.get("by") and all(b in ev_ids for b in r["by"]):
            continue
        if r.get("type") == "accepted" and r.get("risk") in risk_ids:
            continue
        out.append(f"defeaters: {d['id']} ({d['text']}) is neither rebutted by evidence nor accepted as a residual risk")
    return out


def residual_risks(case: dict, when: date | None = None) -> list[str]:
    today = as_of(case, when)
    claims = {c["id"] for c in case["claims"]}
    out = []
    for r in case["residual_risks"]:
        for field in ("owner", "rationale", "monitoring"):
            if not r.get(field):
                out.append(f"residual risks: {r['id']} has no {field}")
        if date.fromisoformat(r["expires"]) <= today:
            out.append(f"residual risks: {r['id']} acceptance expired on {r['expires']}")
        if r["claim"] not in claims:
            out.append(f"residual risks: {r['id']} refers to unknown claim {r['claim']}")
    return out


def coverage(case: dict) -> list[str]:
    seen = {k: set() for k in ("eu_ai_act", "nist_functions", "iso42001", "nist_characteristics")}
    for c in case["claims"]:
        for k in seen:
            seen[k] |= set(c.get("frameworks", {}).get(k, []))
    excluded = {x["characteristic"] for x in case.get("scope_exclusions", []) if x.get("justification")}
    out = [f"coverage: EU AI Act {a} is not addressed by any claim" for a in EU_AI_ACT if a not in seen["eu_ai_act"]]
    out += [f"coverage: NIST AI RMF {f} is not addressed by any claim" for f in NIST_FUNCTIONS if f not in seen["nist_functions"]]
    out += [f"coverage: ISO/IEC 42001 clause {c} is not addressed by any claim" for c in ISO_42001 if c not in seen["iso42001"]]
    out += [f"coverage: NIST characteristic '{ch}' is neither claimed nor excluded with a justification"
            for ch in NIST_CHARACTERISTICS if ch not in seen["nist_characteristics"] and ch not in excluded]
    return out


ALL = {"structure": structure, "traceability": traceability, "freshness": freshness, "independence": independence,
       "strength": strength, "evaluators": evaluators, "defeaters": defeaters, "residual_risks": residual_risks,
       "coverage": coverage}


def run_all(case: dict, overrides: dict | None = None, when: date | None = None) -> dict[str, list[str]]:
    out = {}
    for name, fn in ALL.items():
        if name == "traceability":
            out[name] = fn(case, overrides)
        elif name in ("freshness", "residual_risks"):
            out[name] = fn(case, when)
        else:
            out[name] = fn(case)
    return out


def decision(results: dict[str, list[str]], case: dict) -> str:
    if any(results.values()):
        return "NO-GO"
    accepted = [d for d in case["defeaters"] if (d.get("resolution") or {}).get("type") == "accepted"]
    return "GO WITH ACCEPTED RISKS" if accepted or case["residual_risks"] else "GO"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
