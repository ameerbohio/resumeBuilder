---
name: sanity-check
description: Ground an eval finding that assumes something about the real world beyond the JD/resume text - a seniority bar, a company convention, a "reads as X" call - against actual research (sibling postings, company handbook, existing job research), and confirm/revise/overturn it with cited evidence. Triggered by "wait a minute" assumption-based verdicts from raw-score, ats-score, or hr-simulation. Use whenever an eval finding hinges on what's normal/required/typical rather than on something literally checkable in the JD or draft text.
---

# Sanity check (grounding pass for eval findings)

`raw-score`, `ats-score`, and `hr-simulation` are deliberately blind —
each sees only the JD text, the draft text, and (for raw-score) the
rubric. That blindness is what stops the pipeline from grade-inflating
by rationalizing away problems, and it must not be undone. But
blindness has a specific, predictable blind spot: some verdicts don't
depend on what's literally in the JD or the draft at all — they depend
on an assumption about the outside world (a company's actual leveling
bar, whether a sibling role exists, whether a convention is real or
just plausible-sounding) that a context-isolated subagent has no way
to check. This skill is the deliberate, evidence-only follow-up pass
that fills that specific gap, for that specific class of finding —
never a general excuse to re-litigate a score.

The concrete case that motivated this: the GitLab Platform Readiness
application's Seniority & Scope component and HR-sim concern both
rested on "this reads senior for a role framed as a growth/mentee
seat" — true as far as the JD text goes, but the question "is 4 years
actually short of what this company calls Senior, or is the candidate
genuinely over-scoped for it" is a **checkable, external fact** (the
company's sibling Senior posting stated "5+ years"), not something
either blind eval could have known. Manually researching that
sibling-posting and handbook context and folding the finding back into
the read is exactly what this skill formalizes into a repeatable step.

## What triggers it

Scan eval output (raw-score, ats-score, hr-simulation) for verdicts
that fall into any of these categories — not every Gap or Partial, only
ones asserting something about the world beyond the two texts:

1. **Seniority/level mismatch claims** — "overqualified," "reads
   senior/junior," any verdict tying candidate scope to a title-level
   assumption (`Seniority & scope` component; HR-sim's "seniority
   mismatch" concerns).
2. **Culture/expectation assumptions** — a claim about what "this
   company typically wants" or "this team values" that isn't a literal
   quote from the JD text.
3. **Standardness assumptions** — `ats-score`'s standard-vs-non-standard
   section-header or format calls, when the call is a judgment about
   convention rather than a hard parsing fact.
4. **Hedge language attached to a threshold-moving verdict** — "seems,"
   "likely," "typically," "probably," "reads as" in an eval's own report,
   specifically where that hedge sits next to a number or verdict that
   feeds a `pass-criteria` gate.

This is a taxonomy, not a fixed list — extend it if a future eval type
introduces its own class of world-assumption. A true Gap ("Ruby: not
found in draft") is never a trigger; it's already fully checkable from
the two texts given and re-researching it would just be busywork.

## Procedure

1. **List every triggered claim explicitly**, with which eval produced
   it and the exact wording.
2. **Check what's already gathered first.**
   `1-job-descriptions/<slug>/research.md` and `job-description.md` —
   this is the material the blind evals were deliberately never shown,
   so it's the cheapest and most likely place an answer already exists
   (a prior `job-research` or `raw-score` bonus-signal pass may have
   already found it).
3. **If unanswered, do targeted, bounded external research** — 2-4
   searches per trigger, not an open-ended spiral:
   - Sibling postings at the same company, same team where possible
     (a Senior/Staff variant of the same req is the single best source
     for an actual leveling bar).
   - The company's own public engineering career-ladder/handbook page,
     if one exists.
   - A general industry source only if the company publishes nothing
     itself — and flag it explicitly as "no company-specific source,
     using industry convention" so the report doesn't overstate its own
     certainty.
4. **Verdict each trigger** — one of:
   - **CONFIRMED** — research supports the eval's original claim as
     stated.
   - **REVISED** — research partially supports it but changes the
     framing or magnitude; state the new framing plainly.
   - **OVERTURNED** — research contradicts the claim; state why.
   - **INCONCLUSIVE** — no citable public data found. **The original
     eval verdict stands untouched** — absence of grounding is not
     evidence toward the friendlier reading, and defaulting toward
     "well, we couldn't find anything wrong with it" would quietly
     reintroduce the grade inflation blindness exists to prevent.
5. **Never edit the original eval's report.** This is a companion
   finding, appended alongside it, same as every other append-only
   pattern in this pipeline (`CLAUDE.md` hard rule 6's spirit extends
   here even though this isn't the Compaction Log itself). Save the
   finding to `1-job-descriptions/<slug>/research.md` — it's
   job/company-specific by definition (a sibling posting, a company
   handbook page), so per `CLAUDE.md`'s repo layout it never belongs in
   `research-notes/`.
6. **If a REVISED or OVERTURNED verdict changes a number or threshold
   call feeding a `pass-criteria` gate**, report both the original and
   the grounded number side by side — `pass-criteria` uses the grounded
   one for its gate decision when one exists, but the original stays on
   record rather than being silently replaced (mirrors the existing
   `CLAUDE.md` recalibration-note rule for corrected scores).

## Guardrails — this is not a rescue mission

- **Only cited, checkable facts move a verdict.** Never re-reasoning
  about the resume's own text (the blind eval already did that) and
  never "the candidate feels this read is unfair." If there's no
  external source, the verdict is INCONCLUSIVE, not softened.
- **This is symmetric.** Research can make a finding worse just as
  easily as better — a sibling posting could confirm the company's bar
  is even more mentorship-heavy than assumed, or reveal a second,
  sharper mismatch. Approach every trigger without a preferred
  direction for the answer.
- **Ground each triggered claim once, not every checkpoint.** If the
  same trigger keeps getting re-run against unchanged JD/company facts
  at every `pass-criteria` pass, that's a sign it's being used to wear
  down an inconvenient finding rather than to genuinely check it. A
  claim already grounded in `research.md` doesn't need re-grounding
  unless the underlying draft language actually changed.

## Output format

```
## Sanity check

### Trigger 1: <exact claim + source eval>
- Existing research checked: <found in research.md? / none>
- New research: <sources>
- Verdict: CONFIRMED / REVISED / OVERTURNED / INCONCLUSIVE
- Grounded reading: <if REVISED/OVERTURNED, the corrected framing/number; otherwise "original stands">

### Trigger 2: ...

**Gate impact:** <which pass-criteria gate(s), if any, use the grounded number instead of the original, and what changes>
```

## Where this plugs into the pipeline

Runs after `raw-score`/`ats-score`/`hr-simulation` at a `pass-criteria`
checkpoint — same cadence as those two evals (not every `compactor`
pass), and only when a trigger actually fires, so it doesn't add cost
to checkpoints that don't need it. `pass-criteria` gates 1-3 report
"Sanity-checked: `<trigger>` — `<verdict>`" whenever this ran, and use
the grounded reading over the raw blind one when REVISED or OVERTURNED.
