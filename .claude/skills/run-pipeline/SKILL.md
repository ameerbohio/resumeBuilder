---
name: run-pipeline
description: Orchestrate a resume application end to end, from a new job description through to a submission-ready one-page PDF, by invoking the pipeline's atomic sub-skills in the order that minimizes rework. Use when the user provides a new job posting, says "run the pipeline", "start a new application", or asks to take an application from scratch to final.
---

# Run pipeline

Top-level orchestrator. Does not do the work itself — it decides **which
sub-skill runs next** and enforces the stage gates in `CLAUDE.md`.

## The ordering rule (why this order)

The 26-iteration GitLab application in this repo's history wasted passes by
gathering metrics (iteration 22) and catching factual errors (iterations 6, 7,
23, 24) *after* twenty-odd passes had already reworded the same bullets.
Accuracy and metrics are therefore front-loaded here, before any compaction
touches wording. Do not reorder these phases for convenience.

```
Stage 1   fit-rating          -> STOP for go-ahead
          job-research         (same turn as fit-rating; cheap, informs framing)
Stage 2   draft-initial       -> STOP for go-ahead
          accuracy-checkpoint  (BEFORE compaction: every claim confirmed true)
          metrics-interview    (BEFORE compaction: real numbers sourced once)
                              -> STOP for go-ahead
Stage 3   page-fit-check       (first: does it even overflow?)
          loop {
            compactor          (only while it overflows)
            skim-readability   (after any wording change)
            raw-score          (after any wording change; fresh subagent each time)
            page-fit-check     (after any length change)
            pass-criteria      (all nine gates -> stop or name the next job;
                                 this is where ats-score and hr-simulation run
                                 — checkpoint cadence, not every compactor pass;
                                 sanity-check runs inline, only if a gate 1-3
                                 finding trips its trigger taxonomy)
          }
          add material back    (if cutting overshot, fill the page exactly)
          reorder              (once the bullet set is stable)
          bold                 (once wording/order are settled — last content pass)
          page-fit-check       (bold markup adds chars — re-verify before trusting fit)
          pass-criteria        (final confirmation, all nine gates)
Stage 3.5 finalize            -> 4-final-drafts/<slug>.md + PDF
```

**Stage 3.5 is hook-enforced, not just instruction-enforced.** A
`PreToolUse` hook (`.claude/hooks/check-finalize-gate.ps1`) hard-blocks
any write to `4-final-drafts/<slug>.md` unless `pass-criteria` has
persisted a PASS (via `record-pass-criteria-state.ps1`, its own last
step) whose hash matches the current `3-compact-drafts/<slug>.md` draft
body. There's no conversational override for this — if the user wants
to finalize with gates open, that has to happen by getting
`pass-criteria` to actually PASS, not by asking `finalize` to skip its
precondition.

**All three gating evals (`raw-score`, `ats-score`, `hr-simulation`)
must independently clear their threshold at the `pass-criteria`
checkpoint that ends the loop — a plateaued or high score on one does
not offset a fail on another.** `raw-score` runs every compactor pass
because wording drift is cheap to catch early; `ats-score` and
`hr-simulation` check the document shape and the human read
respectively, which don't drift on every wording tweak, so they only
run when `pass-criteria` is deciding whether to stop the loop — not on
every iteration inside it. **`sanity-check` runs conditionally, on top
of that** — only when one of the three evals produces a finding that
rests on a world-assumption (a seniority bar, a company convention)
rather than something literally checkable in the JD/draft text; most
checkpoints trigger nothing and it's skipped entirely.

**The Stage 3 loop targets page fit, not minimum length.** It ends when
the page is exactly full of content the user wants — reached either by
cutting down to it or by adding back up to it. Do not keep compacting a
draft that already fits.

## Rules

1. **Never cross a STOP without an explicit user go-ahead** (`CLAUDE.md` hard
   rule 3). Report the result plainly and wait. This applies even when the next
   step is obvious. **This governs stage-to-stage transitions only** — once a
   stage is approved, don't re-confirm each sub-decision inside its own loop
   (each compactor pass, each bold/reorder choice, each restored bullet).
   Apply the change and let the append-only Compaction Log carry the record;
   the user reviews and corrects from there, not before each edit. ("why do
   you ask approval for these things... i should raise concerns when i read
   logs, id rather progress not be stopped" — direct user feedback.)
2. **`pass-criteria` decides when the loop ends, not the score alone.** A
   plateaued score is not "done" — see that skill for the nine gates, and
   in particular that all three gating evals (score, ATS parseability, HR
   read) must independently pass, not just the rubric score.
3. **Any factual/wording change goes through `propagate-edit`**, never a direct
   edit of one stage's file, so `0-experience/experience.md` stays the source of
   truth and every downstream copy stays in sync.
4. **The Compaction Log is append-only** (`CLAUDE.md` hard rule 6). Every
   sub-skill that changes `3-compact-drafts/<slug>.md` appends an entry; none
   ever edits or removes one. If a prior entry appears to have gone missing,
   stop and flag it rather than silently continuing.
5. **User taste calls are not failures.** If the user overrides an
   "optimal" recommendation (breadth over JD-relevance, keeping a bullet the
   rubric doesn't credit), log it as a user-directed pass and move on. The goal
   is zero *wasted* iterations, not zero iterations.

## Sub-skills

| Skill | Role |
|---|---|
| `fit-rating` | Stage 1 score + gap list |
| `job-research` | Company/team signals -> `1-job-descriptions/<slug>/research.md` |
| `draft-initial` | Stage 2 comprehensive draft + baseline ceiling |
| `accuracy-checkpoint` | Confirm every claim is literally true, before compaction |
| `metrics-interview` | Source real numbers for unquantified bullets |
| `compactor` | One tighten/cut/merge pass with re-score and log entry |
| `raw-score` | Blind re-score (fresh subagent); catches drift from "unchanged" claims |
| `ats-score` | ATS-parseability eval (fresh subagent); gates finalize with raw-score/hr-simulation |
| `hr-simulation` | Role-played recruiter screen (fresh, context-blind subagent); gates finalize |
| `sanity-check` | Grounds a world-assumption finding (seniority bar, company convention) against real research; conditional, only when triggered |
| `skim-readability` | Per-bullet scannability checks |
| `reorder` | Rank bullets within each section by JD relevance/impact |
| `bold` | Bold top metric/JD keyword per bullet within a density ceiling |
| `page-fit-check` | Real rendered page count, not a character estimate |
| `pass-criteria` | The nine-gate stop test |
| `propagate-edit` | Apply one change across experience.md -> all draft stages |
| `finalize` | Clean copy to `4-final-drafts/` + PDF |
