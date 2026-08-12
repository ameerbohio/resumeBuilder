---
name: draft-initial
description: Stage 2 of the resume pipeline. Pull all relevant experience into a comprehensive uncompacted draft, score it as the baseline ceiling, and append a "Why This Could Be Rejected" soft-risk read. Use after a fit rating is approved and the user says to proceed to a draft.
---

# Initial draft (Stage 2)

## Procedure

1. Pull **all** experience relevant to this JD from
   `0-experience/experience.md`. Err toward inclusion. This draft is a
   quarry of material, not a resume — length and tightness are Stage 3's
   problem, and material cut here is expensive to rediscover later.
2. Organize into standard ATS-safe sections (Experience, Projects,
   Education, Technical Skills; reverse chronological; no tables,
   columns, images, or icons). **Write it in the renderer's expected
   shape from the start**, so Stage 3 doesn't burn its first iteration on
   a throwaway "normalize markdown for the renderer" pass:
   - Name line with no leading `#`.
   - Two-line entries: `**Company**, Location` then `*Role, Department*,
     Date` — never a separate `### Company` header, and never the two
     folded onto one line.
   - A standalone certification with no separate institution line is its
     own one-line entry: `*Certification Name*, Date`.
   - Skills as `- **Category:** items` bullets, not bare bold
     paragraphs.
   - See `page-fit-check`'s Calibration section for the full expected
     shape and why deviations render oddly instead of failing loudly.
3. Save as `2-initial-drafts/<slug>.md`.
4. Re-run the rubric against **this draft** and put the score at the top
   as an HTML comment:
   `<!-- fit score: X/10 (components: ...) -->`
   This is the **baseline ceiling**. Stage 3 must never drop below it.
5. Append `## Why This Could Be Rejected` (format below).
6. **Stop.** Report the score and ask the user to review for
   completeness and accuracy — what got missed, what's misrepresented.
   Iterate here until they confirm. Do not start compaction.

## Why This Could Be Rejected

Holistic soft-risk read against the **full, uncompacted** material. Not the
requirement-gap list from Stage 1, and not anything compaction will later
introduce. Standing factors to check every time:

- **Skimmability/density** — bullets packing 3-4 claims into one line, so
  a 6-10 second scan misses the JD-matching phrase buried mid-sentence.
- **Paid work vs. project work balance** — if every JD-critical data
  point comes from a personal project rather than a paid role, a
  recruiter who discounts side-project evidence loses the strongest fit
  evidence on the page. Say so plainly when it's true.
- **Wording vs. the JD's literal terms** — near-synonyms a human reads as
  equivalent but a keyword pass may not.
- **Seniority-level ambiguity** — ownership/leadership language against a
  growth-seat JD (or the reverse), as a screen-out risk independent of
  the scored deduction.
- **In-progress degree / availability signal.**
- **Location/visa ambiguity** against the JD's stated locations.

## Why this stage is worth being slow at

Stage 3 can only tighten what Stage 2 collected. In this repo's first
application, material cut in compaction pass 1 had to be restored in
passes 12 and 17 because its value was underrated the first time. A
thorough Stage 2 plus an explicit user review is what makes those
restore-passes unnecessary.

After the user confirms this draft, run `accuracy-checkpoint` and then
`metrics-interview` **before** any compaction. Both edit
`0-experience/experience.md` via `propagate-edit`, and doing them first
means compaction never rewords a bullet that is about to change anyway.
