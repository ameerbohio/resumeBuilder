---
name: reorder
description: Rank and resequence the bullets within each resume section by job-description relevance, quantified impact, and scope appropriateness, without changing any wording. Use when a draft's content is settled and the ordering should be optimized for a skimming reader.
---

# Reorder

Pure resequencing. **No wording changes** — if a bullet needs rewording,
that is `compactor` or `skim-readability`, in a separate pass. Keeping
this pass wording-free is what makes "character count identical
before/after" a valid proof that nothing was lost.

## When

Once the bullet set is stable. Re-run whenever a later pass adds or
removes a bullet, or the ordering goes stale silently. It is cheap —
treat it as opportunistic, not a one-time ceremony at the end.

## Ranking method

Score each bullet within its section on three axes, then sort high to
low. Full rationale in `research-notes/bullet-order-priority.md`.

1. **JD relevance (dominant).** Near-verbatim echo of the JD's own
   phrasing beats a thematic match. Rank against the JD's own priority
   order: its "what you'll do" list is written highest-to-lowest, so a
   bullet matching item #1 outranks one matching item #4. Then Required
   items, then Highly-Valued.
2. **Quantified impact (tiebreaker).** A concrete number outranks a
   process or scope statement.
3. **Scope appropriateness (tiebreaker, and a real one).** Under a
   growth/mentee-framed JD, individual-contributor phrasing ranks above
   ownership language ("led", "owned", "primary"). Leading a section
   with the most senior-sounding bullet front-loads exactly the
   overqualification read the rubric already penalizes. Under a
   senior-framed JD, invert this.

## Two exceptions

- **Context bullets stay first.** A project section that opens with what
  the project *is* reads better than one opening mid-detail, even if a
  later bullet scores higher on relevance. Orientation beats ranking for
  a section's first line only.
- **Section and entry order are untouched.** Reverse chronological for
  roles, and the order of the sections themselves, are not this skill's
  business.

## Verification

Character count **must** be identical before and after. Check it:

```bash
awk '/^<first line of resume body>/{f=1} f{print}' 3-compact-drafts/<slug>.md | wc -c
```

A changed count means wording drifted during the rewrite — revert and
redo. Re-scoring is unnecessary in principle (the rubric scores presence,
not position) but the char-count check is not optional, since it is the
only thing proving no bullet was dropped or altered in the shuffle.

## Log entry

Append to the Compaction Log. State the before-order and after-order for
each section as a plain list, then one clause per moved bullet saying
which axis moved it. Score line reads `X/10 (unchanged — the rubric
scores literal presence of evidence, not its position)`. Chars line reads
`N → N (no change — pure reorder)`.
