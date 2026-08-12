---
name: propagate-edit
description: Apply an approved factual or wording change across the whole pipeline - source of truth first, then every draft stage - with a Compaction Log entry. Use whenever a correction, metric, or rewording needs to land in more than one file.
---

# Propagate edit

The primitive underneath `accuracy-checkpoint`, `metrics-interview`, and
any user-reported correction. Editing one stage's file directly is how
the stages silently diverge; always route through this.

## Order (do not vary)

1. **`0-experience/experience.md` first.** It is the source of truth. A
   change that does not belong here does not belong in a draft either
   (`CLAUDE.md` hard rule 1: every claim must trace back to this file).
   Editing it is a user-initiated, explicit act — which is exactly what
   this skill is (hard rule 2 forbids resume passes editing it
   *implicitly*, not this).
2. **`2-initial-drafts/<slug>.md`** — verbose Stage 2 phrasing.
3. **`3-compact-drafts/<slug>.md`** — the tightened Stage 3 phrasing,
   plus a new append-only log entry.
4. **`4-final-drafts/<slug>.md`** — only if already populated. If it is,
   re-render the PDF too (`finalize`), or the shipped artifact silently
   goes stale.

Re-word for each stage's register. Do not paste Stage 2's sentence into
the compacted draft; match the surrounding bullets' density.

## Applying to more than one application

If several applications are in flight, a change to `experience.md`
affects all of them. Apply it to every slug's drafts, or tell the user
explicitly which ones you left alone and why. Silently updating one is
how two applications end up making contradictory claims.

## Verification before finishing

- `grep` the changed phrase across all stages to confirm it landed
  everywhere it should and nowhere it should not.
- Confirm every JD-scored keyword still present verbatim in the compact
  draft. If the edit removed evidence for a scored item, run `raw-score`
  and record the recalibrated number.
- Recount characters for the log entry.

## Log entry

```markdown
### Iteration N — Correction: <what was wrong> (score recalibration, not a compaction loss)

- **Score:** X/10 (<unchanged, or the component that moved and why>)
- **Chars:** before → after (±N, N%) · running total saved: N (N%)
- **Correction note:** <what the user corrected, and where it was fixed
  at the source>
- **Changed:** <the specific edits per file>
- **Risk check:** <one line>
```

When a correction *lowers* the score, say plainly that this is not a
compaction regression: the prior number was inflated by a claim that was
not true, and hard rule 1 outranks "never accept a compaction that costs
points." Without that sentence, a later pass will read the drop as a
mistake to undo.

## The append-only guarantee

`CLAUDE.md` hard rule 6: the Compaction Log is never edited, removed, or
truncated. If entries appear to be missing (an editor clip, a bad paste),
**stop and flag it** — restore from conversation history if available,
and never continue as though the record were intact.
