---
name: fit-rating
description: Stage 1 of the resume pipeline. Save a new job description verbatim, score experience.md against it with the CLAUDE.md rubric, and append a Fit Rating section with gaps and a pursue/stretch/skip call. Use when the user provides a new job posting to evaluate.
---

# Fit rating (Stage 1)

## Procedure

1. Pick a `<slug>` in `company_role-slug` form (e.g.
   `acme_senior-backend-engineer`). Create
   `1-job-descriptions/<slug>/` and save the posting **verbatim** to
   `job-description.md` inside it. Verbatim means verbatim — do not
   summarize, reformat, or drop the boilerplate; later passes quote the
   JD's own literal phrasing and need it intact.
2. Read `0-experience/experience.md` in full. Not a grep — in full.
3. Score per the `CLAUDE.md` rubric, using the whole experience file as
   the candidate material (nothing is tailored yet).
4. Append `## Fit Rating` to the bottom of `job-description.md`.
5. **Stop.** Report the score and top gaps. Wait for the go-ahead to
   Stage 2.

## Scoring discipline

Apply `CLAUDE.md`'s scoring methodology literally, not impressionistically.
The three failure modes that inflated the score on this repo's first
application, all of which happened in a single pass:

- **Weak-implicit treated as near-pass.** Clear = 1.0, Partial = 0.5,
  Weak-implicit = 0.25, Gap = 0. Evidence that has to be *inferred* is
  much closer to a gap than to a pass.
- **Strong-Plus items folded into requirement coverage.** They are
  narrative only. Only Required + Highly-Valued enter the numerator.
- **Seniority scored as "meets or exceeds = 2/2".** Overqualification
  against a JD's own stated scope is a real deduction. If the posting
  frames a growth/mentee seat ("you'll learn from other engineers",
  intermediate/junior title) and the material shows senior ownership,
  dock it and say why.

A fourth, learned later: **a public personal repo is not an open-source
contribution.** Check for a license permitting reuse and accepted
external contributions before crediting that item, and generalize the
habit — verify the literal claim, not the adjacent-sounding one.

## Output section format

```markdown
## Fit Rating

**Score: X.X/10** (Requirement coverage X/4, Keyword/skill alignment X/2,
Seniority & scope match X/2, Quantified impact X/2)

### <JD's own category name, e.g. Required Experience & Skills>
- **<item>** — <Clear pass|Partial|Weak-implicit|Gap>. <1-2 sentences
  citing the specific experience.md evidence.>

### <next JD category...>

### What Makes You Stand Out (Strong Plus)
<narrative only — state explicitly that these are excluded from coverage>

**Tally: N clear passes, N partial, N weak-implicit, N gaps** (N items scored)

### Seniority note (affects Seniority & scope match, X/2)
<only when there is a real over/under-qualification signal>

### Recommendation: **Pursue | Stretch | Skip**
<one paragraph: what's strong, what the true gaps are, what to manage>
```

Distinguish a **true gap** (no evidence exists) from **underselling**
(evidence exists but is buried or not phrased in the JD's terms). Only
true gaps cost rubric points; underselling is a Stage 2/3 framing note.

If a corrected score ever replaces an earlier one in this file, leave a
one-line recalibration note saying what changed and why. Never silently
overwrite a number.
