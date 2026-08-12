---
name: pass-criteria
description: Decide whether a resume draft is done - a six-gate check across score, page fit, accuracy, readability, diminishing returns, and ordering - or name exactly which pass should run next. Use to test whether compaction should stop, or when asked if the resume is as good as it gets.
---

# Pass criteria

The stop test for the Stage 3 loop. Either "done, finalize it" or "not
done, and here is the single next pass" — never a vague "could keep
tightening".

## Why it is not just the score

On this repo's first application the score reached its ceiling at
iteration 12 and stayed there through iteration 26. A score-only gate
would have stopped 14 passes early and shipped a draft that was over one
page, had two factual overclaims still in it, carried three
fact-stacked bullets, and was ordered worst-first in one section. The
score measures rubric coverage. It does not measure whether a human can
read the thing.

## The six gates

All must pass. Report each explicitly with its evidence — never assert a
gate from memory or from a prior pass's claim.

**1. Score floor.** Current score >= the Stage 2 baseline ceiling in
`2-initial-drafts/<slug>.md`. Verify with a fresh `raw-score`, not the
last log entry's assertion. (A lower ceiling is legitimate only when an
accuracy correction reduced it — check the log for that note before
treating a shortfall as a regression.)

**2. Page fit.** `page-fit-check` reports the target page count. Also
report remaining whitespace: a page with room left is a *pass* with an
opportunity attached, and the user may want to spend it.

**3. Accuracy clean.** No open flags from `accuracy-checkpoint`, and no
skills-line entry the user has not knowingly accepted as
draft-unproven. If the checkpoint has not run since the last content
change, this gate **fails** — it is not assumed-pass.

**4. Readability clean.** `skim-readability` reports no *unaccepted*
failing bullets. A flagged bullet the user has knowingly kept — because
its keywords carry a scored verdict, or they simply prefer it — counts as
accepted and does not block the gate; record that it was a deliberate
call. Unreviewed failures do block it. (The reference resume sits at 1
accepted failure of 17; a run reporting many more usually means the
checks were applied too literally — see that skill's calibration note.)

**5. Diminishing returns confirmed.** Satisfied by **either** of:

- A `compactor` pass was actually *attempted* since the last content
  change and either dropped the score or produced no meaningful
  reduction. Attempted, not assumed — this is what distinguishes "we
  stopped finding cuts" from "we stopped looking."
- **The page is already full of content the user wants** (gate 2 reports
  the target page count with negligible whitespace left, reached by
  adding material back rather than by cutting). Compaction is a means to
  page fit, not an end. Once the page is exactly full, freed space would
  only be refilled from `experience.md` — so a compactor pass has nothing
  to buy and demanding one is busywork.

The second route is the normal ending for a draft that overflowed, was
compacted to fit, and then had material added back until the page was
exactly full. Say which route satisfied the gate; do not run a pass just
to tick the box.

**6. Ordering current.** `reorder` has run against the **present**
bullet set. If any bullet was added, removed, or reworded since the last
reorder, this gate fails — ordering goes stale silently.

## Output

```
## Pass criteria: <PASS - ready to finalize | FAIL - N gates open>

| Gate | Status | Evidence |
|------|--------|----------|
| 1 Score floor        | PASS/FAIL | X/10 vs ceiling X/10 (raw-score, this pass) |
| 2 Page fit           | PASS/FAIL | PAGES=N, ~N bullets of room left |
| 3 Accuracy clean     | PASS/FAIL | last checkpoint: <when>, open flags: N |
| 4 Readability clean  | PASS/FAIL | N of M bullets failing |
| 5 Diminishing returns| PASS/FAIL | last compactor attempt: <result> |
| 6 Ordering current   | PASS/FAIL | last reorder: <when> vs last content change |

**Next pass:** <the single specific skill and target, or "none — finalize">
```

## Do not over-apply

Gates 1-6 measure whether the draft is *sound*. They do not measure
whether the user is *satisfied*. A user choosing to spend a pass on
breadth signal, a preferred phrasing, or a skill the rubric does not
credit is exercising judgment this skill has no standing to override.
When all six gates pass, say so and hand the decision over — do not argue
against a taste call, and do not treat one as a failed gate.
