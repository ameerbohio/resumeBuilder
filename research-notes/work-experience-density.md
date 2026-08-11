# Work experience density and redundancy: best practices

Researched during the `gitlab_intermediate-backend-engineer-platform-readiness`
application, before the Iteration 17 pass in `3-compact-drafts/` (internal
redundancy review + "experience feels light" fix).

## Bullets per job

- Entry-level roles: 3-5 bullets per job.
- Mid-level roles: 5-7 bullets per job.
- Senior/executive roles: 7-10 bullets per job.
- By recency: 4-5 bullets for the most recent/high-impact job, 1-3 for
  older or less-relevant ones.
- Floor: at least 3 bullets per job; if that's genuinely unattainable,
  1-2 detailed bullets beat padding with weak ones.
- Quality still wins: recruiters scan for roughly 6 seconds, so a
  resume padded to hit a bullet-count target without each bullet
  pulling its own weight is worse than a shorter, tighter one. The
  guidance is a range to sanity-check against, not a quota to fill.

## Avoiding redundant skill demonstration

- Don't restate the same skill in near-identical language across
  multiple bullets (or between a bullet and the skills section) — it
  reads as padding and, per some sources, can look like the candidate
  is short on genuinely distinct things to say.
- If two bullets both exist primarily to prove the same capability
  (e.g. two separate "reviewed pull requests" bullets), merge them
  into one bullet that keeps whatever distinct detail each one had,
  and use the freed-up slot for a bullet that proves something the
  resume doesn't yet show.
- Vary action verbs across bullets within a role — repeated opening
  verbs are a mild version of the same "lack of variety" signal.

## How this was applied

Iteration 17 found two real cases of the same skill being demonstrated
twice: P&W had two separate "pull request review" bullets (one
mentorship-framed, one Azure-DevOps/CI-CD-framed), and Aviya repeated
"requirement writing" in a bullet that already sat right next to the
bullet that owns that claim (DO-178C traceability). Both were merged/
trimmed, and the freed capacity was spent on three previously-cut
bullets that each prove something genuinely new: production debugging
+ cross-team Infrastructure collaboration, concurrency/distributed-
systems reasoning (component locking), and real-time performance
optimization (DMA offload, ~15% CPU headroom recovered). This moved
P&W from 5 to 6 bullets and Aviya from 4 to 5 — both now sit inside
the 5-7 mid-level range instead of at its floor — while every rubric-
scored keyword from the pre-existing bullets was verified to survive
the merge before the pass was accepted.
