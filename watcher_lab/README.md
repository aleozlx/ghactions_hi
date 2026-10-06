# Watcher process laboratory

Public, synthetic experiments for PR automation. No private screening records,
credentials, customer information, or production evidence belongs here. This lab
is isolated from production enrollment and does not establish GPU or multi-provider
validation. Existing experiments are left intact.

## Historical-fixture scope

The repository owner confirmed that these earlier experiments are stale and the
experimental-track work has already been deployed in FlashInfer. The replay below
is a historical test fixture, **not evidence of a current FlashInfer defect**.
New experiments should target current watcher recovery, reconciliation, evidence
freshness and lifecycle gaps.

## Experiment 1: green is not coverage

The read-only inspector checks a requested run against the PR's latest head and
explicit required job names, paginates jobs, and rechecks the head after inspection.
It never authorizes CI or merging. Passing jobs do not prove that the intended tests
executed; test collection, skips, architecture and scope require separate evidence.
The inspector also rereads the run after job pagination; changed attempts or
lifecycle metadata invalidate that observation. Full coverage receipts remain future work.

```sh
python3 -m unittest discover -s watcher_lab -v
python3 watcher_lab/inspect_run.py --pr 8 --run 33850994203 \
  --required-job 'Full Suite (mirrors H100: pytest tests/)'
python3 watcher_lab/inspect_run.py --pr 8 --run 33851061353 \
  --required-job 'Full Suite (mirrors H100: pytest tests/)'
```

Observed on 2026-10-05 at PR #8 head
`c88a04e31a62c97e95dd8643d2e7e4ef3c0cfcb0`:

- Run 33850994203 has a successful summary but lacks the required test job.
  The inspector rejects job completeness.
- Run 33851061353 has the named successful job. The inspector acknowledges job
  completion while retaining **unknown coverage** and **no merge authorization**.
- Four local regression cases cover skipped tests, stale head, unspecified job
  requirements, and the distinction between job success and coverage/merge proof.

## Next experiments

1. Structured test receipts with executed/skipped counts, scope, head, base and run
   attempt; deliberately exercise zero tests and a skipped relevant architecture.
2. A changed head during inspection and a rerun during pagination: invalidate the
   observation rather than combine receipts from different revisions/attempts.
3. Ambiguous CI submission followed by reconciliation: exactly one dispatch.
4. Durable waiting, worker restart, and explicit ownership handoff.
5. An isolated synthetic fix/validation/merge loop with verified outcome attribution.

These are lab scenarios, not a claim that production implements every gate.

## Landing projection transition corpus

`landing_scenarios.json` contains nine synthetic cases: ready, actual CI failure,
authorization-only failure, changed head/stale screening, safety hold, requested
changes, conflict, unknown CI and draft. The platform consumes the same fixture
shape in its ETA regression tests. This public copy is a reviewable experiment
specification, not a standalone projection implementation or a live CI experiment.
None of these cases supplies production duration samples or proves release inclusion.
