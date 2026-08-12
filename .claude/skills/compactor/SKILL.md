---
name: compactor
description: Run one Stage 3 compaction pass on a resume draft - cut redundancy, merge overlapping bullets, tighten wording - then re-score, verify no rubric loss, and append a Compaction Log entry. Use when the user says to compact, tighten, shorten, or trim a draft.
---

# Compactor (one Stage 3 pass)

One pass. Not a loop — `run-pipeline` or the user decides whether to run
another, and `pass-criteria` decides when to stop.

## What compaction is for

Page fit, not brevity for its own sake. The only reason to cut a true,
relevant bullet is that it does not fit. So:

- **Check `page-fit-check` before compacting.** If the draft already
  fits, do not run this skill reflexively — ask what the space is for.
- **When the draft overflows, cut to fit.** That is this skill's job.
- **When cutting overshoots and leaves whitespace, stop compacting and
  add material back** from `experience.md` until the page is exactly
  full. That is the normal, expected ending — not a failure of the
  compaction loop, and the resulting non-decreasing passes are logged
  like any other.

A draft that fits the page exactly, with content the user wants, is
**done**. Squeezing it further just creates space that gets refilled.

Everything happens in `3-compact-drafts/<slug>.md`: `## Compaction Log`
at the top (append-only), current-best draft below it. First pass copies
`2-initial-drafts/<slug>.md` in as the starting point.

## Procedure

1. **Read the draft below the log.** Never read *into* the log for
   evidence — prior "score unchanged" claims are assertions, not proof.
2. **Pick one lever and apply it.** Mixing several in one pass makes a
   score drop impossible to attribute:
   - *Relevance cut* — drop material genuinely low-relevance to this JD.
   - *Redundancy merge* — two bullets proving the same capability become
     one that keeps each one's distinct detail.
   - *Rewording* — same claims, fewer words.
   - *Telegraphic trim* — drop articles/connectives ("a", "the",
     "and"->"/") where it stays readable. Ask first; imperfect grammar
     is a user preference, not a default.
3. **Re-score** with `raw-score` — literally, against the new text, not
   by reasoning about what the edit "should not have" affected.
4. **Compare to the baseline ceiling** in `2-initial-drafts/<slug>.md`:
   - Score **dropped** -> identify the exact bullet/phrase that carried
     the lost evidence, restore or rework it, re-score. Never accept a
     compaction that costs points.
   - Score **held** -> append a log entry, replace the draft below it.
5. **Run `skim-readability`** if wording changed, and `page-fit-check` if
   length changed meaningfully.

## What must survive every pass

Before accepting, verify **verbatim** that every phrase carrying a scored
verdict is still present. Keyword-alignment credit tracks literal term
presence, so a synonym is a loss. The recurring trap in this repo's
history: a bullet gets cut, its keyword is moved to the Technical Skills
line, and the pass claims equivalence. It is not equivalent — a
skills-line tag with no bullet elaborating it is **Partial** evidence,
not a Clear pass. That single mistake cost 0.2 points and took three
passes to notice and undo.

Corollary: cutting a bullet whose keyword also lives in the skills line
is still a downgrade. Check the verdict, not the string.

## Log entry format (terse by default)

```markdown
### Iteration N — <short title>

- **Score:** X/10 (unchanged, or the component delta if it moved)
- **Chars:** before → after (−saved, %) · running total saved: N (N%)
- **Cut/changed:** <flat list of item names — no rationale paragraphs.
  One clause of why only when non-obvious: a score-affecting call, or
  keeping something that looks cuttable but isn't.>
- **Risk check:** <one line. "No new risk" is the expected answer most
  passes. Expand only if this pass introduced or changed a Stage 2
  "Why This Could Be Rejected" risk.>
```

`Chars:` before/after/saved plus running total is non-negotiable on every
entry (`CLAUDE.md` hard rule 6) — brevity trims prose, never the count.
Get the count with:

```bash
awk '/^<first line of resume body>/{f=1} f{print}' 3-compact-drafts/<slug>.md | wc -c
```

## Non-decreasing passes are legitimate

A pass that *adds* characters (restoring evidence, using space freed
elsewhere, a user-requested breadth addition) is still a logged
iteration. Say plainly that it grew and why; do not disguise it as a
compaction.
