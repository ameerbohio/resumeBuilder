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
            raw-score          (after any wording change)
            page-fit-check     (after any length change)
            pass-criteria      (all six gates -> stop or name the next job)
          }
          add material back    (if cutting overshot, fill the page exactly)
          reorder              (once the bullet set is stable)
          bold                 (once wording/order are settled — last content pass)
          page-fit-check       (bold markup adds chars — re-verify before trusting fit)
          pass-criteria        (final confirmation, all seven gates)
Stage 3.5 finalize            -> 4-final-drafts/<slug>.md + PDF
```

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
   plateaued score is not "done" — see that skill for the six gates.
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
| `raw-score` | Blind re-score; catches drift from "unchanged" claims |
| `skim-readability` | Per-bullet scannability checks |
| `reorder` | Rank bullets within each section by JD relevance/impact |
| `bold` | Bold top metric/JD keyword per bullet within a density ceiling |
| `page-fit-check` | Real rendered page count, not a character estimate |
| `pass-criteria` | The seven-gate stop test |
| `propagate-edit` | Apply one change across experience.md -> all draft stages |
| `finalize` | Clean copy to `4-final-drafts/` + PDF |
