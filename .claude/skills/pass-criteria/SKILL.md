---
name: pass-criteria
description: Decide whether a resume draft is done - a nine-gate check across the three gating evaluations (raw-score, ats-score, hr-simulation), page fit, accuracy, readability, diminishing returns, ordering, and bold-emphasis density - or name exactly which pass should run next. Use to test whether compaction should stop, or when asked if the resume is as good as it gets.
---

# Pass criteria

The stop test for the Stage 3 loop. Either "done, finalize it" or "not
done, and here is the single next pass" — never a vague "could keep
tightening".

Nine gates as of the `ats-score`/`hr-simulation` skills' addition to
the pipeline — update this count if a future skill adds another gate,
so the header line and the actual gate list never drift apart.

## Three evals, one gate each — none is optional

Gates 1-3 are three independent, differently-blind evaluations of the
same draft: `raw-score` (does the content earn rubric credit),
`ats-score` (can a parser see that content at all), and
`hr-simulation` (does a human reader's gut reaction favor it). A draft
can pass any two of these and still fail the third — a resume can
score well on the rubric and parse cleanly while still reading as
generic to a human, or read compellingly while quietly failing to
parse. **All three must independently clear their threshold before
this skill can report PASS; none substitutes for another, and a high
score on one does not offset a fail on another.**

## Sanity-check assumption-based findings before failing a gate on them

`raw-score`, `ats-score`, and `hr-simulation` are blind by design — none
of them can check a finding against anything outside the JD/draft text.
That's correct for literal claims (a keyword either appears or it
doesn't) but it means some verdicts are really **assumptions about the
outside world** wearing a score's clothing — "this reads senior for a
growth-seat JD" depends on what the company's actual Senior bar is, not
on anything in the two texts themselves.

Before treating a gate-1/2/3 shortfall as final, check whether any of
the findings behind it match `sanity-check`'s trigger taxonomy
(seniority/level claims, culture/expectation assumptions, standardness
assumptions, hedge language on a threshold-moving verdict). If one
does, run `sanity-check` on it and use its output:

- **CONFIRMED or INCONCLUSIVE** — the gate's original PASS/FAIL stands.
  Inconclusive research is not grounds to soften a finding.
- **REVISED or OVERTURNED** — report both numbers side by side and use
  the grounded one for the gate's PASS/FAIL call, per `sanity-check`'s
  own rule against silently replacing a number.

This is not a way to argue a gate into passing — see that skill's
guardrails. A finding with no assumption in it (a literal Gap, a
literal structural PDF fail) never triggers this and never gets a
second look for being inconvenient.

## Why it is not just the score

On this repo's first application the score reached its ceiling at
iteration 12 and stayed there through iteration 26. A score-only gate
would have stopped 14 passes early and shipped a draft that was over one
page, had two factual overclaims still in it, carried three
fact-stacked bullets, and was ordered worst-first in one section. The
score measures rubric coverage. It does not measure whether a human can
read the thing.

## The nine gates

All must pass. Report each explicitly with its evidence — never assert a
gate from memory or from a prior pass's claim.

**1. Score floor (raw-score).** Current score >= the Stage 2 baseline
ceiling in `2-initial-drafts/<slug>.md`. Verify with a fresh
`raw-score` — spawned as a fresh subagent per that skill's procedure,
not the last log entry's assertion and not a score reasoned about
inline. (A lower ceiling is legitimate only when an accuracy correction
reduced it — check the log for that note before treating a shortfall as
a regression.) If the shortfall traces to a component like Seniority &
Scope that rests on a world-assumption rather than literal text, run
`sanity-check` on it before failing the gate — see that section above.

**2. ATS score.** Run `ats-score` fresh (also a subagent call — see
that skill). Passes at score >= 8.5/10 **and** zero critical fails in
its structural-parseability checks. A critical fail (broken column
order, info-bearing image, header/footer content, non-extractable
text) blocks this gate regardless of the numeric score — see that
skill's threshold note for why it isn't averaged away.

**3. HR simulation.** Run `hr-simulation` fresh (also a subagent call,
and the most context-isolated of the three — it must not be told the
rubric, the current score, or anything else about this pipeline).
Passes at Verdict = Advance **and** Confidence >= 7/10. A Maybe, a
Reject, or a low-confidence Advance all fail this gate. If the concerns
list names a specific, fixable issue, that becomes the next pass (see
that skill's routing note); route by what the concern actually names,
not reflexively back to `compactor`. If a concern is itself a
world-assumption (a seniority read, a "this company usually wants X"
guess), run `sanity-check` on it before treating it as the next pass's
target — grounding it may change what the actual next pass should be,
or dissolve it entirely.

**4. Page fit.** `page-fit-check` reports the target page count. Also
report remaining whitespace: a page with room left is a *pass* with an
opportunity attached, and the user may want to spend it.

**5. Accuracy clean.** No open flags from `accuracy-checkpoint`, and no
skills-line entry the user has not knowingly accepted as
draft-unproven. If the checkpoint has not run since the last content
change, this gate **fails** — it is not assumed-pass.

**6. Readability clean.** `skim-readability` reports no *unaccepted*
failing bullets. A flagged bullet the user has knowingly kept — because
its keywords carry a scored verdict, or they simply prefer it — counts as
accepted and does not block the gate; record that it was a deliberate
call. Unreviewed failures do block it. (The reference resume sits at 1
accepted failure of 17; a run reporting many more usually means the
checks were applied too literally — see that skill's calibration note.)

**7. Diminishing returns confirmed.** Satisfied by **either** of:

- A `compactor` pass was actually *attempted* since the last content
  change and either dropped the score or produced no meaningful
  reduction. Attempted, not assumed — this is what distinguishes "we
  stopped finding cuts" from "we stopped looking."
- **The page is already full of content the user wants** (gate 4 reports
  the target page count with negligible whitespace left, reached by
  adding material back rather than by cutting). Compaction is a means to
  page fit, not an end. Once the page is exactly full, freed space would
  only be refilled from `experience.md` — so a compactor pass has nothing
  to buy and demanding one is busywork.

The second route is the normal ending for a draft that overflowed, was
compacted to fit, and then had material added back until the page was
exactly full. Say which route satisfied the gate; do not run a pass just
to tick the box.

**8. Ordering current.** `reorder` has run against the **present**
bullet set. If any bullet was added, removed, or reworded since the last
reorder, this gate fails — ordering goes stale silently.

**9. Bold density current.** `bold` has run against the **present**
bullet set and reported density under the ~15% ceiling from
`research-notes/resume-bold-emphasis.md`. If any bullet was added,
removed, or reworded since the last bold pass — or `bold` has never run
— this gate fails. Emphasis goes stale exactly like ordering does: a
bullet added after the last bold pass is unbolded by omission, not by
a deliberate "this bullet doesn't earn it" call, and a reader has no way
to tell the difference.

## Output

```
## Pass criteria: <PASS - ready to finalize | FAIL - N gates open>

| Gate | Status | Evidence |
|------|--------|----------|
| 1 Score floor (raw-score)   | PASS/FAIL | X/10 vs ceiling X/10 (fresh subagent) |
| 2 ATS score                 | PASS/FAIL | X.X/10, critical fails: N (fresh subagent) |
| 3 HR simulation             | PASS/FAIL | Verdict: <Advance/Maybe/Reject>, confidence X/10 (fresh subagent) |
| 4 Page fit                  | PASS/FAIL | PAGES=N, ~N bullets of room left |
| 5 Accuracy clean            | PASS/FAIL | last checkpoint: <when>, open flags: N |
| 6 Readability clean         | PASS/FAIL | N of M bullets failing |
| 7 Diminishing returns       | PASS/FAIL | last compactor attempt: <result> |
| 8 Ordering current          | PASS/FAIL | last reorder: <when> vs last content change |
| 9 Bold density               | PASS/FAIL | last bold: <when> vs last content change, density N% |

**Sanity checks run:** <none triggered> / <trigger -> verdict, one line each; "none" is expected most passes>

**Next pass:** <the single specific skill and target, or "none — finalize">
```

## Persist the verdict — every run, PASS or FAIL

`finalize` no longer trusts a verdict spoken in conversation: a
`PreToolUse` hook (`.claude/hooks/check-finalize-gate.ps1`) hard-blocks
any write to `4-final-drafts/<slug>.md` unless
`.claude/pipeline-state/<slug>.json` records a PASS whose hash matches
the *current* draft body in `3-compact-drafts/<slug>.md`. This skill is
the only place that's allowed to write that file, and it must do so at
the end of **every** run — a FAIL gets recorded too, both because it
overwrites a stale PASS from an earlier, now-invalidated draft, and
because the hook's block message reads directly from it (a recorded
FAIL produces a more useful denial than a missing file does).

Run this after producing the table above, filling in the actual
per-gate results and overall verdict:

```powershell
& .claude/hooks/record-pass-criteria-state.ps1 `
  -Slug "<slug>" -Verdict "PASS" `
  -GatesJson '{"1_score_floor":"PASS","2_ats_score":"PASS","3_hr_simulation":"PASS","4_page_fit":"PASS","5_accuracy":"PASS","6_readability":"PASS","7_diminishing_returns":"PASS","8_ordering":"PASS","9_bold_density":"PASS"}'
```

Call it with `&` (the call operator), not a nested `powershell -File`
invocation — the latter has been observed to mangle the `-GatesJson`
argument's quoting when run from within an already-running PowerShell
session.

The script hashes `3-compact-drafts/<slug>.md`'s draft body (everything
after the `<!-- draft-below -->` sentinel — see `compactor`) the same
way the hook does, so don't hand-construct the JSON's `draftHash`
field yourself; the script is the only source of truth for that value.
If the sentinel is missing, the script errors out rather than guessing
— fix the file (see `compactor`'s sentinel note) and re-run.

## Do not over-apply

Gates 1-8 measure whether the draft is *sound*. They do not measure
whether the user is *satisfied*. A user choosing to spend a pass on
breadth signal, a preferred phrasing, or a skill the rubric does not
credit is exercising judgment this skill has no standing to override.
When all nine gates pass, say so and hand the decision over — do not argue
against a taste call, and do not treat one as a failed gate.

Gates 1-3 are the exception to that deference: they are not taste
calls, they're independent measurements of whether the document
actually works (scores, parses, reads well to a human), so a user
overriding one of *those* specifically is accepting a real, named risk
— say so plainly rather than treating it the same as a phrasing
preference.
