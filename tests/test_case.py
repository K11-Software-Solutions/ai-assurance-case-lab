"""The committed case, each check on hand-made cases, the snapshot integrity check and the negative controls."""
import copy
import json

import pytest
from datetime import date

from assurance import checks as C
from assurance.snapshot import check as snapshot_check, sha256
from evals import run_case as gate

CASE = C.load(gate.CASE)


def test_snapshots_match_pinned_commits_and_hashes():
    assert snapshot_check() == []


def test_line_endings_do_not_change_a_hash():
    assert sha256(b"a\r\nb\n") == sha256(b"a\nb\n")


ASSESSED = date.fromisoformat(CASE["assessment_date"])


def test_committed_case_passes_every_check_and_reaches_a_decision():
    results = C.run_all(CASE, when=ASSESSED)
    assert all(v == [] for v in results.values()), results
    assert C.decision(results, CASE) == "GO WITH ACCEPTED RISKS"


def test_committed_json_matches_its_source():
    import runpy
    import tempfile
    from pathlib import Path
    src = (gate.ROOT / "case" / "build_case.py").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "build_case.py"
        p.write_text(src, encoding="utf-8")
        runpy.run_path(str(p), run_name="__main__")
        assert json.loads((Path(d) / "assurance_case.json").read_text(encoding="utf-8")) == CASE


def test_every_quote_is_verbatim_in_its_snapshot():
    assert C.traceability(CASE) == []
    broken = copy.deepcopy(CASE)
    broken["evidence"][0]["quote"] = "| correctness | 0.999 |"
    assert any("E1 quote not found" in p for p in C.traceability(broken))


def test_strength_uses_the_rule_of_three():
    c = copy.deepcopy(CASE)
    next(x for x in c["claims"] if x["id"] == "G9")["required_bound"] = 0.003
    assert C.strength(c) == []                         # 3/1440 = 0.21% <= 0.3%
    next(x for x in c["claims"] if x["id"] == "G9")["required_bound"] = 0.002
    assert C.strength(c)                               # 0.21% > 0.2%


def test_documented_findings_alone_cannot_carry_a_critical_claim():
    c = copy.deepcopy(CASE)
    c["evidence"] = [e for e in c["evidence"] if e["claim"] != "G3" or e["kind"] == "documented-finding"]
    assert any("only on documented findings" in p for p in C.independence(c))


def test_a_rebuttal_must_point_at_evidence_in_the_case():
    c = copy.deepcopy(CASE)
    next(d for d in c["defeaters"] if d["id"] == "D2")["resolution"] = {"type": "rebutted", "by": ["E99"]}
    assert C.defeaters(c)


def test_no_residual_risks_and_no_accepted_defeaters_means_a_clean_go():
    c = copy.deepcopy(CASE)
    c["residual_risks"], c["defeaters"] = [], []
    c["scope_exclusions"] = [{"characteristic": "fair with harmful bias managed", "justification": "out of scope"}]
    assert C.decision(C.run_all(c, when=ASSESSED), c) == "GO"


def test_the_case_fails_by_itself_when_time_passes():
    later = date(2027, 2, 6)                            # evidence is 91 days old and every acceptance has expired
    results = C.run_all(CASE, when=later)
    assert results["freshness"] and results["residual_risks"]
    assert C.decision(results, CASE) == "NO-GO"


@pytest.mark.parametrize("variant", sorted(gate.VARIANTS))
def test_negative_controls(monkeypatch, tmp_path, variant):
    monkeypatch.setenv("CASE_VARIANT", variant)
    assert gate.main(["--out", str(tmp_path)]) == 1
    report = json.loads((tmp_path / "release_decision.json").read_text(encoding="utf-8"))
    assert report["decision"] == "NO-GO"
    assert report["checks"][gate.EXPECTED[variant]], f"{variant} should fail the {gate.EXPECTED[variant]} check"


def test_committed_release_decision_is_current(tmp_path, monkeypatch):
    monkeypatch.delenv("CASE_VARIANT", raising=False)
    gate.main(["--out", str(tmp_path)])
    published = (gate.ROOT / "docs" / "release-decision.md").read_text(encoding="utf-8")
    assert (tmp_path / "release_decision.md").read_text(encoding="utf-8") == published
