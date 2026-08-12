---
name: metrics-interview
description: Find bullets with no quantified result and interview the user for the real numbers behind them, then propagate the approved metrics into experience.md and every draft stage. Use after the Stage 2 draft is confirmed, or when a resume reads light on numbers.
---

# Metrics interview

## When to run

Right after `accuracy-checkpoint`, **before** compaction. Running it late
(it was pass 22 of 26 on this repo's first application) means compaction
has already reworded the exact bullets that are about to change.

## Procedure

1. **Audit.** Count, per section, how many bullets contain a hard number.
   Benchmark from `research-notes/metric-quantification-density.md`: 3-6
   metric-bearing bullets per role. A paid role at zero is the signal to
   act on — especially when a projects section is metric-dense, since
   that contrast reads as "strong side project bolted onto thin day-job
   bullets" (a Stage 2 soft risk, quantified).
2. **Ask.** One message, numbered, grouped by section, quoting each
   bullet. For each, suggest *which kind* of number would fit rather than
   asking an open "any metrics?" — users recall concrete prompts better:
   - performance: latency, load time, throughput
   - scale: users served, requests/month, records processed
   - reliability: incidents before/after, failure rate
   - delivery: time saved, cycle-time change
   - quality: defects found, coverage, review volume
   - scope: how many requirements, services, projects, people
3. **Say up front that "I don't remember" is a fine answer.** It is —
   forcing a number is exactly what `CLAUDE.md` hard rule 1 forbids.
4. **Clarify anything ambiguous before writing it.** Truncated answers,
   "a lot", "several", and estimates-vs-measurements all need one
   follow-up. Ask which it is; do not pick the flattering reading.
5. **Phrase honestly.** A user-estimated figure gets `est.` or `~` in
   the bullet text itself, not just in the log. A measured one does not
   need the hedge.
6. **Apply via `propagate-edit`** so the numbers land in
   `0-experience/experience.md` first and flow to every draft stage.

## Weaving numbers in

Prefer editing the existing bullet over adding a new one — a metric
should cost a few characters, not a line:

- `Built customer-facing request portal;` -> `Built customer-facing
  request portal (~20 requests/month);`
- `Closed critical login security gap by` -> `Closed critical login
  security gap affecting 600+ users by`
- `Eliminated concurrent-editing conflicts by` -> `Eliminated
  concurrent-editing conflicts (2-3/week to 0) by`

When a bullet has a genuine measured outcome, restructure it to lead with
the result (XYZ / Result-then-Method), which is what
`research-notes/project-bullet-readability.md` calls for:

- `Rebuilt the test bench's instrument control service via PyVISA` ->
  `Cut instrument-testing time ~20% by rebuilding the test bench's
  instrument control service via PyVISA`

## Expect the score not to move

Most sourced numbers do not map to a Required or Highly-Valued JD item,
and Quantified impact is often already at 2/2 from elsewhere. That is
fine and expected — this pass buys skim quality and credibility, not
rubric points. Say so in the log rather than implying a score gain.
