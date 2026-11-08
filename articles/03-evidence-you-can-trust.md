# 03. Evidence You Can Trust: Pinning, Quoting and Freshness

> **Series:** AI Assurance Case Lab · [Index](../README.md#articles) · Previous: [02](02-claims-arguments-and-evidence.md) · Next: [04. Defeaters](04-defeaters-evidence-against-your-own-claim.md)

An assurance case is only as good as its weakest evidence link. "Security testing passed (see CI)" is a link to a moving target: the CI of which commit, which run, which configuration? This lab makes every link checkable.

## Pin the source

[`evidence/sources.json`](../evidence/sources.json) names, for each of the ten labs, the repository, the **v1.0.0 release**, the **full commit hash** of that release, and its **Zenodo version DOI**:

```json
"security": {"repo": "ai-security-testing-lab", "version": "v1.0.0",
             "commit": "d815003dc2fce9dfcf1b02c01a0e56681f8e23b2",
             "doi": "10.5281/zenodo.24039872",
             "files": ["experiments/results/summary.md"]}
```

The DOI points at an archived copy that cannot change. The commit points at the same content in the repository. A branch name would point at whatever was pushed last.

## Snapshot it

`python -m assurance.snapshot` downloads each evidence file from GitHub **at the pinned commit** into [`evidence/snapshots/`](../evidence/snapshots), and records its SHA-256 in [`evidence/manifest.json`](../evidence/manifest.json). The case is then checked against the snapshots, offline and deterministically. `python -m assurance.snapshot --check` (run in CI) fails if a snapshot is missing, came from a different commit, or **does not match its recorded hash**: a snapshot edited by hand to make a number look better is caught. Line endings are normalised before hashing, so checking out on Windows or Linux gives the same hash.

## Quote it

Every evidence item quotes, **verbatim**, the line of the snapshot it relies on:

```text
E18  quote: "| all layers (recommended) | 0.0 | none | 0.0 |"
     file:  ai-security-testing-lab@d815003/experiments/results/summary.md
```

The traceability check confirms each quote appears in its snapshot. Change the 0.0 to 0.01 in the case, or in the snapshot, and the case fails. A number in an assurance case that cannot be found in its source is a claim, not evidence.

Quoting also makes reviews fast: the reviewer sees the exact line, and the rendered decision links straight to the file at the pinned commit.

## Check that it is about this system, and recent

Each evidence item states the **system version** it is about and the **date** it was collected. The freshness check requires the version to match the version under assessment, and the evidence to be at most 90 days old. Evidence about 2.2.0 supports claims about 2.2.0. That rule sounds pedantic until a release ships on last quarter's red-team report.

## Grade it

Not all evidence is equal, and the case records the difference:

| Kind | What it is | Example |
|---|---|---|
| gate | a pass/fail result from CI with a stated threshold | `\| correctness \| 0.926 \| >= 0.9 ✅ \|` |
| measurement | a number from an experiment, ideally with an interval or sample size | 0 successes in 1,440 attempts |
| documented finding | a sentence describing a result | "Evaluations on world state caught it." |

Critical claims may not rest **only** on documented findings (article 07). Where a lab publishes only prose, the honest fix is upstream: make the lab commit its results in a machine-readable form, as six of the ten labs already do.

## Takeaways

- **Pin evidence to a commit and an archived DOI**, never a branch.
- **Snapshot and hash it**, so it can be checked offline and cannot be quietly edited.
- **Quote the exact line**, and check the quote is really there.
- **Evidence has a version and a date.** Check both.
- **Grade evidence by kind**, and hold critical claims to the stronger kinds.
