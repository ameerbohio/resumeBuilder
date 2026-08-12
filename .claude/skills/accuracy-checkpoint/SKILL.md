---
name: accuracy-checkpoint
description: Walk the user through every factual claim in a draft to confirm it is literally true before compaction begins, flagging overclaims, unproven skills, and attribution errors. Use after the Stage 2 draft is complete, or whenever the user says a claim is wrong.
---

# Accuracy checkpoint

One structured pass where the user confirms each claim, run **before**
compaction reshapes any wording.

## Why this exists as its own gate

Every factual error in this repo's first application surfaced by
accident, spread across four separate late passes: an "open source"
claim that was really a public personal repo (pass 6), a Jira/Azure
DevOps employer swap (pass 7), a C++ skill with no backing bullet (pass
10), a structural-coverage/requirements misattribution across two
projects (pass 23), and a "drove the fix" overclaim on a bug the user
only diagnosed (pass 24). Each triggered a correction *and* a rescore
after compaction had already reworded the bullet. Asking once, up front,
collapses all of that.

An LLM cannot verify these against reality. Only the user can. So this
skill's job is to **ask well**, not to check.

## What to flag for confirmation

Read the draft and surface every claim in these categories. Do not ask
about all bullets uniformly — ask about the ones where being wrong is
plausible and costly:

1. **Verb strength vs. actual involvement.** "Led", "owned", "drove",
   "designed" — for each, ask whether the user did the thing or
   contributed to/reported it. This is the single most common overclaim.
2. **Attribution across projects/employers.** Any bullet bundling
   several accomplishments — did all of them happen on that project, at
   that company, in that role? Bundled bullets imply a link between the
   items that may not exist.
3. **Skills-line entries with no supporting bullet.** List them
   explicitly: "these appear only in Technical Skills with nothing in
   the draft demonstrating them." True-but-unproven is a judgment call
   for the user, but they should make it knowingly.
4. **Claims whose plain reading differs from the technical truth.**
   Public repo vs. open source; "certified" vs. "targeting
   certification"; "production" vs. "dev branch".
5. **Numbers already present** — confirm each is measured, not
   remembered-as-approximately. Hedge with "est." / "~" where it's an
   estimate, per `CLAUDE.md` hard rule 1.

## How to ask

Group them into one message as a numbered list with the exact current
wording quoted, so the user can answer "1, 4 wrong, rest fine" in one
pass. Do not interrogate bullet by bullet across several turns.

For anything the user corrects: propose the corrected wording, get
approval, then apply it with `propagate-edit` so
`0-experience/experience.md` is fixed at the source and every draft
stage is updated together.

## After corrections

If a correction removes evidence for a scored rubric item, run
`raw-score` and record the recalibrated number with a one-line note
explaining what changed. A score that drops here is **not** a compaction
loss — the prior number was inflated by a claim that was not true, and
`CLAUDE.md` hard rule 1 outranks the "never accept a compaction that
costs points" rule. Say that explicitly in the log entry so the drop is
not mistaken for a regression later.
