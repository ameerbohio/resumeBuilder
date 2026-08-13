---
name: hr-simulation
description: Role-played recruiter screen of a resume draft against a job description, giving a gut-reaction Advance/Maybe/Reject verdict independent of the rubric. Use when asked to "HR sim", "recruiter check", "would this pass a screen", or as one of the three gating evals pass-criteria requires before a draft can finalize.
---

# HR simulation

`raw-score` and `ats-score` both measure the draft against a
checklist. Neither measures the thing that actually decides most real
applications: a person spends single-digit seconds on first pass,
forms an impression, and only reads closely if that impression earns
it. This skill simulates that read directly, instead of inferring it
from a checklist.

## How this differs from "Why This Could Be Rejected"

`draft-initial` (Stage 2) already produces a `## Why This Could Be
Rejected` soft-risk list — but that's the *main* agent, which has
full pipeline context (the rubric, the gaps already found, the
candidate's own framing of their experience), doing analytical
risk-spotting. This skill is a **role-play by a subagent that has
none of that context** — it only ever sees the JD and the resume, the
way an actual screener would, and reacts in character rather than
auditing a checklist. The two are complementary: one tells you what an
expert reviewer of the *pipeline* thinks could go wrong; this tells
you what a specific, uninformed human reader's gut says on first
contact.

## This runs in a subagent

Same reasoning as `raw-score` and `ats-score` — spawn a fresh `Agent`
tool call (`subagent_type: general-purpose`, `run_in_background:
false`). The blindness here is even more load-bearing than the other
two evals: this skill's entire value is a genuine first impression, so
the subagent must not be told the rubric, any prior score, any gap
list, or that this is part of a scored pipeline at all. Build the
prompt from scratch each time. Give it:

1. The job description text.
2. The draft's rendered text (below the Compaction Log, if scoring a
   `3-compact-drafts/<slug>.md` file).
3. The persona and task instructions from the Procedure section below,
   verbatim.
4. The exact output format from this file.
5. Nothing else. In particular, do **not** give it: the rubric, the
   current raw-score, the Compaction Log, `research.md`, or any framing
   that this resume already survived other checks — a screener doesn't
   know that either, and telling the subagent would bias the very
   reaction this skill exists to capture.

## Procedure (the subagent's instructions)

Role-play a specific persona, stated explicitly in the prompt: a
recruiter or hiring-manager screener for the role in this job
description, doing a first-pass resume review among a stack of other
applicants for the same posting. Two passes, in order:

1. **The 6-second skim.** Look at the resume the way a screener
   actually does first — top third of the page, section headers, any
   bolded text, job titles/companies, overall density. Write down the
   immediate, gut-level impression *before* reading closely: what
   registers, what's confusing, what's missing at a glance, whether it
   looks like a fit for this specific posting or a generic resume.
2. **The considered read.** Now read the whole thing. Note what
   changed from the skim impression (confirmed, contradicted, or
   added to). Identify:
   - **Top 3 strengths** — what would make this candidate stand out
     against other applicants for this specific role.
   - **Top 3 concerns/red flags** — anything that would make a
     screener hesitate, set the resume aside, or want to screen it out
     before a phone call: unclear scope, unexplained gaps, seniority
     mismatch (over- or under-qualified for how the posting reads),
     jargon that doesn't map to the JD's own language, generic
     boilerplate that doesn't feel targeted to this role, anything
     that reads as inflated or vague.
   - **Verdict:** Advance / Maybe / Reject — the actual call a
     screener makes at this stage, not a hedge.
   - **Confidence:** 0-10, "how likely I'd move this to a phone
     screen against a realistic applicant pool for this posting."

Stay in character throughout — react the way the persona would, not
the way an assistant summarizing a rubric would. Do not soften a
Reject into a Maybe out of politeness; the whole point is an honest
gut call.

## Scoring and threshold

There is no weighted numeric formula here by design — a real screening
decision isn't computed from components, and forcing one would just
reintroduce the rubric this skill exists to get away from. The gate is
the verdict itself:

**Threshold to pass this gate: Verdict = Advance AND Confidence ≥
7/10.** A Maybe, a Reject, or an Advance with low confidence all fail
the gate — a "would probably advance but I'm not sure" read is exactly
the ambiguous case worth catching before finalizing, not a pass.

## Output format

```
## HR simulation — Verdict: ADVANCE / MAYBE / REJECT (confidence X/10)

### 6-second skim
<what registers first, before close reading>

### Considered read

**Top 3 strengths**
1. ...

**Top 3 concerns / red flags**
1. ...

**Verdict:** Advance / Maybe / Reject
**Confidence:** X/10 — <one line: what would move this up or down>
```

## Notes

- This is one of three gating evaluations (with `raw-score` and
  `ats-score`) that `pass-criteria` requires to all clear their
  thresholds before a draft finalizes. Per the pipeline's cadence
  decision, this runs only at `pass-criteria` checkpoints, not on
  every compaction pass.
- If the verdict comes back Maybe/Reject, the concerns list is the
  next-pass input — a scope/seniority concern usually routes back to
  wording (`compactor`/rewording), a "doesn't feel targeted" concern
  usually routes to `reorder` (leading with the wrong material), and a
  density/confusion concern usually routes to `skim-readability`. Route
  by what the concern actually names, not reflexively to `compactor`.
- Because this skill role-plays rather than checklists, re-running it
  on an unchanged draft can legitimately return a different Confidence
  number (a real screener isn't perfectly deterministic either) — a
  swing of a point or two on repeat runs is expected noise, not a bug.
  A verdict flip (Advance <-> Reject) on an unchanged draft is not
  expected noise and is worth a second run before trusting either one.
- A "seniority mismatch" or "doesn't feel like what this company
  wants" concern is a world-assumption, not a literal-text finding —
  the persona is guessing at company norms it was never shown, by
  design. Run `sanity-check` on a concern like that before routing it
  to a content pass; grounding it against a sibling posting or the
  company's own handbook can confirm, sharpen, or dissolve it. A
  concern about something literally on the page (density, jargon,
  an unclear line) doesn't need this — only ones asserting what's
  "normal" or "expected" for the employer.
