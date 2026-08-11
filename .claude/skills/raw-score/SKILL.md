---
name: raw-score
description: Blind, single-pass rubric score of a resume draft against a job description, ignoring prior conversation context and Compaction Log score claims. Use when asked to "raw score", "blind score", "rate check", "sanity check the score", or "re-verify the fit rating" for a resume draft. Also does light research on the hiring team for bonus-fit signals not stated in the job description.
---

# Raw resume score

Blind, fresh rubric pass against a resume draft. Re-derives the score
from what's literally on the page and in the job description, with no
credit carried forward from prior conversation turns or Compaction Log
entries. Use this whenever a score might have drifted — a compaction
pass that claimed "unchanged" without a literal re-check is the most
common cause — or whenever the user just wants a sanity check before
trusting the number currently on record.

## Invocation

`/raw-score <slug>` — `<slug>` matches `1-job-descriptions/<slug>.md`.

If more than one draft stage exists for that slug
(`2-initial-drafts/`, `3-compact-drafts/`, `4-final-drafts/`), ask
which one to score. If only one exists, use it without asking.

## Procedure

1. **Read the job description fresh.** `1-job-descriptions/<slug>.md`,
   the posting text only, not its own `## Fit Rating` section. That
   section is a prior score; don't anchor on it.
2. **Read the target draft fresh.** Only the resume text itself. For a
   `3-compact-drafts/<slug>.md` file, that means the content *below*
   the Compaction Log. Do not treat the log's prior score claims or
   "unchanged" assertions as evidence — read past the log, never into
   it, when forming the score. (The log stays append-only regardless;
   this skill never edits it.)
3. **Score literally, not from memory.** For every Required /
   Highly-Valued / Strong-Plus item in the JD, find the exact phrase
   or claim in the draft's own text that supports it. If the
   supporting evidence was cut in some earlier pass and only survives
   as a bare skills-line keyword with no bullet elaborating it, that's
   Partial at best, not Clear pass — a keyword tag is not proof. This
   is the single most common source of score drift in this pipeline.
4. **Apply the rubric exactly as defined in `CLAUDE.md`:**
   - Requirement coverage (0-4): Required + Highly-Valued items only,
     weighted Clear pass = 1.0, Partial = 0.5, Weak-implicit = 0.25,
     Gap = 0, averaged then multiplied by 4. Strong Plus / Stand-out
     items are narrative only and never enter this numerator.
   - Keyword/skill alignment (0-2): overlap between the JD's named
     tools/tech/skills and what literally appears anywhere in the
     draft (bullets or skills line both count here specifically, this
     component tracks term presence, not depth of proof).
   - Seniority & scope match (0-2): penalize overqualification against
     the JD's own stated scope, not just underqualification.
   - Quantified impact (0-2): concrete, relevant metrics present.
   Show the full component breakdown, the point-by-point verdict list
   grouped by the JD's own categories, and a tally line, per
   `CLAUDE.md`'s Evaluation style preferences.
5. **Research the hiring team for bonus signals not in the JD text.**
   A couple of searches on the specific team or product named in the
   posting, not the company in general: engineering handbook pages,
   the product the team owns, anything that surfaces an adjacent skill
   or interest that would land well with that specific team but that
   the JD itself never asked for. Report these separately as
   **Bonus signals (not scored)**. Do not fold them into any of the
   four numeric components — the rubric only scores against what the
   JD itself states; mixing in externally researched criteria would
   break `CLAUDE.md` rule 5 ("scores are always computed the same
   way") by scoring different applications against different,
   undocumented criteria sets.
6. **Report, don't write.** This skill produces a report in the
   conversation. It does not edit the draft file, the job-description
   file, or the Compaction Log. If the score differs from what's
   currently on record, surface the discrepancy and the specific
   evidence gap that caused it. Logging a correction or restoring
   evidence is a separate decision for the user, same as any other
   file edit in this pipeline (hard rule 3: no auto-advancing without
   explicit go-ahead).

## Output format

```
## Raw score: X.X/10

### Required
| Item | Verdict | Why (literal evidence, or "not found in draft") |

### Highly Valued
| Item | Verdict | Why |

Tally: N clear, N partial, N weak-implicit, N gap (N items)

### Strong Plus (narrative only, not in the coverage numerator)
- ...

### Component breakdown
- Requirement coverage: X/4
- Keyword/skill alignment: X/2
- Seniority & scope: X/2
- Quantified impact: X/2

### Bonus signals (not scored)
- [team-research finding] — why it's not JD-stated but could land well
```

## Notes

- This is intentionally stricter than the Stage 1/Stage 3 scoring
  built into the main pipeline flow — those can, and should, reason
  about `experience.md`'s fuller content when deciding what to *add*.
  This skill only ever asks "what's provably here right now," which
  makes it good for catching drift, not for drafting.
- Re-run this any time a compaction pass has claimed "score unchanged"
  several iterations in a row without a fresh literal check.
