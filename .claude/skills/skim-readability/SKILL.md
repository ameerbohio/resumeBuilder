---
name: skim-readability
description: Check every resume bullet for skimmability - fact-stacking, mechanism-before-outcome, unexplained jargon, over-length lines, and AI-writing tells - and propose fixes that preserve scored keywords. Use after any wording change, or when asked whether bullets are easy to follow.
---

# Skim readability

The reader gives the page 6-10 seconds. A bullet that is accurate but
unparseable in that window has failed, regardless of its rubric value.

Run after any wording change. Report findings; apply fixes only with the
user's go-ahead if they alter meaning.

## The five checks

Run all five against **every** bullet. Report per-bullet pass/fail, not
an average — one unreadable bullet is a real defect that an average
hides.

**1. Fact-stacking.** Flag bullets carrying 3+ *independent* claims —
ones that do not share a single outcome. Count **clusters, not clauses**:
one stated outcome plus the multi-part mechanism that produced it is
**one** cluster no matter how many tools it names. A comma-chain listing
what a pipeline checks, or how a platform was built, is fine. What is not
fine is several unrelated accomplishments sharing a bullet because they
happened at the same job.

*Fails (three independent facts, no shared outcome):* "Hosted/organized
training modules in GitLab across company's active projects; used GitHub
and Bitbucket for day-to-day code work; managed/estimated work via Jira
issues/epics through sprint planning." — a tool inventory, not an
achievement.

*Fails (two accomplishments + documentation, joined by a semicolon):*
"Ran development as a spec-first agentic loop — implementer agent
drafting one phase at a time and a reviewer agent evaluating against
acceptance criteria, tuning prompt and criteria design to raise
assessment accuracy; documented across 30+ explainers, a runbook, and a
release checklist."

*Passes (one outcome, multi-part mechanism):* "Built 8-job CI/CD pipeline
that blocks bad merges automatically: security/race/fuzz scanning,
integration tests, and k6 load baselines that fail build on any
performance regression."

Fix a failure by splitting into single-idea bullets, or by cutting the
inventory clause that carries no outcome. A split costs a line but a
bullet nobody finishes is worth less than two that get read.

**2. Outcome before mechanism.** Flag bullets opening with *how* instead
of *what happened*. Readers anchor on the first clause.

*Fails:* "Maintained 17 versioned design specs as the source of truth and
enforced structure in CI via kubeconform JSON-Schema validation."
*Passes:* "Caught schema errors before deploy by validating every
Kubernetes manifest against JSON Schema in CI (kubeconform), backed by 17
versioned design specs."

**3. Length.** Flag any bullet that would wrap past two rendered lines.
Use `page-fit-check`'s HTML output rather than guessing from character
count; a two-line bullet is fine, a three-line one is where readers drop
out.

**4. Jargon without an anchor.** Flag domain acronyms and tool names with
no plain-English clause nearby. The test: would a recruiter who is not a
specialist know why this line matters? Names that carry weight with the
target team (the JD's own terms) stay. Names that only mean something
inside the candidate's former industry need a clause saying what they
bought — or should be cut.

*Fails:* "Performed structural coverage analysis (MC/DC)."
*Passes:* naming it inside a bullet whose outcome is already legible, or
cutting it if it does not earn the space.

**5. AI-writing tells.** Em/en dashes inside bullet prose, "leveraged",
"utilized", "spearheaded", "robust", "seamless", "cutting-edge",
rule-of-three lists that pad rather than inform, and vague intensifiers
("significantly", "dramatically") that stand in for a number. Header and
date-range separators are formatting, not prose — leave those alone.

## The constraint on every fix

Rewriting must not silently drop a phrase that carries a scored verdict.
Before proposing a fix, note which JD-scored terms the bullet contains
and confirm they survive verbatim. When readability and keyword-presence
genuinely conflict, keep the keyword and say so — but check whether a
split (check 1) resolves it, since it usually does.

## Calibration

These checks are tuned so that a genuinely good resume passes. The
reference is `4-final-drafts/Ameer_Bohio_Resume_Gitlab.pdf` — a finished,
one-page draft where **1 of 17 bullets** fails (the GitLab/Bitbucket/Jira
tool inventory above, kept deliberately because its keywords carry a
Highly-Valued verdict).

If a run flags a third or more of the bullets, the checks are being
applied too literally, not the resume being bad — most likely by counting
clauses instead of clusters in check 1. Recalibrate against the reference
before reporting a wall of failures.

## Output

```
| # | Bullet (first ~40 chars) | Stack | Outcome-1st | Len | Jargon | Tells |
|---|--------------------------|-------|-------------|-----|--------|-------|

Failing: N of M bullets
<for each failure: the proposed rewrite, and the scored keywords it preserves>
<and, where a failure is being kept deliberately, say why>
```
