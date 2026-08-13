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

`/raw-score <slug>` — `<slug>` matches `1-job-descriptions/<slug>/job-description.md`.

If more than one draft stage exists for that slug
(`2-initial-drafts/`, `3-compact-drafts/`, `4-final-drafts/`), ask
which one to score. If only one exists, use it without asking.

## This runs in a subagent, not inline

"Blind" only holds if the scorer genuinely cannot see prior turns. A
score computed inline in the main conversation — even one that says
"ignoring prior context" — still shares a context window with every
score claim, Compaction Log entry, and prior verdict already said out
loud this session, and language models anchor on numbers they've
already produced. The fix is structural, not instructional: **the
agent invoking this skill must spawn a fresh `Agent` tool call
(`subagent_type: general-purpose`, `run_in_background: false` — the
result gates the next pipeline step, so this is not a fire-and-forget
call) rather than running steps 1-6 below itself.** The subagent
starts cold, so it cannot anchor on anything said earlier in this
conversation even if it wanted to.

Build the subagent prompt from scratch each time — it has no memory of
this skill file, the rubric, or the pipeline. Include, inline in the
prompt:

1. The two file paths to read (job description, target draft — and for
   a `3-compact-drafts/<slug>.md` target, the explicit instruction to
   read only the content *below* the `## Compaction Log`).
2. The full rubric text from `CLAUDE.md` (components, per-item credit
   weights, the Required/Highly-Valued/Strong-Plus split) — copy it in,
   don't tell the subagent to go read `CLAUDE.md` itself, since that
   file also carries this application's own prior Fit Rating and
   Compaction Log numbers that would defeat the blindness this exists
   for.
3. Steps 3-5 below verbatim (scoring literally, the bonus-signal
   research, where to save it).
4. The exact output format from this file.
5. An instruction to return the report as its final message and change
   nothing else — no file edits beyond the optional `research.md`
   append in step 5.

Report the subagent's output back to the user/orchestrator exactly as
returned; do not re-summarize or round it.

## Procedure

1. **Read the job description fresh.**
   `1-job-descriptions/<slug>/job-description.md`, the posting text
   only, not its own `## Fit Rating` section. That section is a prior
   score; don't anchor on it.
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
   **Bonus signals (not scored)**, and save any findings worth keeping
   to `1-job-descriptions/<slug>/research.md` (create it if absent,
   append if present) — this is job/company-specific, so per
   `CLAUDE.md`'s repo layout it belongs alongside the job description,
   never in `research-notes/`. Do not fold bonus signals into any of
   the four numeric components — the rubric only scores against what
   the JD itself states; mixing in externally researched criteria
   would break `CLAUDE.md` rule 5 ("scores are always computed the
   same way") by scoring different applications against different,
   undocumented criteria sets.
6. **Report, don't write to the draft.** This skill never edits the
   draft file, the job-description file's `## Fit Rating`, or the
   Compaction Log — those stay a separate decision for the user, same
   as any other file edit in this pipeline (hard rule 3: no
   auto-advancing without explicit go-ahead). The one exception is
   `1-job-descriptions/<slug>/research.md` per step 5: that file exists
   specifically to persist reusable research rather than lose it at
   the end of the conversation, so saving to it is not "advancing a
   stage."

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
- This is one of three gating evaluations (with `ats-score` and
  `hr-simulation`) that `pass-criteria` requires to all clear their
  thresholds before a draft is allowed to finalize. It runs on every
  compactor pass (cheap, catches drift immediately); the other two run
  only at `pass-criteria` checkpoints — see that skill.
- The Seniority & scope component is the most common source of a
  world-assumption finding — a verdict like "reads senior for this
  scope" is only checkable against what the company itself actually
  calls senior, which this skill's blind subagent has no way to know.
  If that component is what's costing points, don't treat the number
  as final without a `sanity-check` pass on it — see that skill and
  `pass-criteria`'s "Sanity-checking assumption-based findings" section.
