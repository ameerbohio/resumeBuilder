# Technical skills section: best practices

Researched during the `gitlab_intermediate-backend-engineer-platform-readiness`
application, before the Iteration 8 rework in `3-compact-drafts/`.

## Two schools of thought

1. **Comprehensive keyword index** — list everything you've touched,
   grouped by category, so ATS parsers and quick-scan recruiters can
   pattern-match against the JD. Produces long, many-category lists.
2. **Curated proof list** — fewer categories (2-4), fewer items,
   everything defensible in a live interview. Dominant in current
   recruiter-facing advice; a bloated list reads as keyword-stuffing
   and costs credibility with a human reviewer even if it helps a
   naive ATS match.

## Findings

- **Count:** most successful resumes land at 6-12 items total in the
  skills section (median ~8-9), not 40-50.
- **Categories:** 2-4 is typical for a strong resume. Narrow, one-off
  categories (e.g. splitting out "Security & Identity" or "Testing" as
  their own buckets) read as padding.
- **Quality over quantity, explicitly:** "Ten highly relevant skills
  that align with the job description will always outperform twenty
  random abilities you happened to pick up over the years."
- **Drop "Soft Skills" as a category** — recruiters scan this section
  for verifiable hard skills/tools specifically.
- Standard header names ("Technical Skills," not "My Stack") still
  matter for ATS parsing.

## Should the skills section repeat what's in the bullets?

Yes, and it should — they serve different jobs. Bullets are proof
(skill applied, with outcome/context). The skills section is an index
(bare keyword) so a fast scan finds the term without reading every
bullet. Overlap is expected; the skills section shouldn't introduce
net-new tools that appear nowhere else in the narrative (reads as
unproven), but it also shouldn't try to avoid repetition for its own
sake.

## How this was applied

Iteration 8 of the GitLab compact draft cut the Technical Skills
section from 7 categories / ~48 items down to 4 categories / 13 items,
keeping only JD-named terms or terms load-bearing for a specific
scored rubric verdict. Iterations 9-10 and 16 partially reversed this
at explicit user request, trading rubric purity for a "show
versatility to adjacent teams" signal (see
[work-experience-density.md](work-experience-density.md) for the
parallel reasoning applied to the Experience section) — landing around
5 categories / 20+ items as a deliberate compromise, not a reversion
to the original ungoverned list.

## Sources

- [Skill Categories For Your Resume That Recruiters Will Love](https://resumeworded.com/skill-categories-for-resume-key-advice)
- [How to List Skills on a Resume: The Complete 2026 Guide](https://blog.theinterviewguys.com/how-to-list-skills-on-a-resume/)
- [Resume Skills Section Guide - Monster](https://www.monster.com/career-advice/resume/resume-skills-section)
- [How to Write a Skills Section of a Resume - Rezi](https://www.rezi.ai/posts/skills-section-of-resume)
- [Tech Resume Best Practices 2026 - OmniCV](https://www.omnicv.io/blog/tech-resume-best-practices)
