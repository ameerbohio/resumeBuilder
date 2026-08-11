# Project/technical bullet readability: best practices

Researched during the `gitlab_intermediate-backend-engineer-platform-readiness`
application, before the Iteration 15 rewording pass in `3-compact-drafts/`.

## The core tension

Being technical and specific is what makes a bullet credible (names
the tools, states the mechanism) — but stacking too many distinct
technical facts into one sentence (via semicolons, comma chains, or
parenthetical asides) makes it easy for a reader to skim past the
exact phrase that would have mattered to them. Both failure modes are
real: a vague bullet ("worked on backend systems") is invisible to
keyword search; an overloaded bullet ("built X using Y, enforced Z via
W, and validated V through U, backed by T") loses the reader before
they reach the part that matters.

## Recommended structure

**Action + Tech + Impact/Scope**, roughly: start with the verb, name
the specific technology/technique, then state the outcome or scope.
The XYZ formula is a variant: "Accomplished [X] as measured by [Y], by
doing [Z]."

- Lead with the plain-English outcome or problem solved before
  drilling into implementation mechanism — readers (and especially
  non-specialist recruiters) anchor on the first clause.
- Avoid "tool-only" bullets that name technologies without describing
  the decision or result — they don't demonstrate judgment, just
  exposure.
- Avoid cramming 3+ independent technical facts into one bullet via
  semicolons. If a bullet has two genuinely separate ideas (e.g. "how
  the system was built" and "how it was tuned/documented"), splitting
  into two focused bullets usually reads better than one dense one,
  even though it costs an extra line.
- Recruiters spend seconds per resume; every bullet needs to pull its
  weight with a specific result, skill, or achievement rather than
  being a list of everything true about the project.

## How this was applied

Iteration 13 tightened prose density without cutting content
(compressed a named-tool list into a shorter phrase). Iteration 15
went further: reordered the schema-validation and CI/CD bullets to
lead with outcome before mechanism, and split one overloaded
sentence (agentic-loop architecture + prompt-tuning + documentation,
originally joined by a semicolon) into two single-idea bullets. Every
rewording pass checked that JD-scored keywords/phrases survived
verbatim before being accepted — readability changes should never
silently cost rubric evidence (see `CLAUDE.md` hard rule 3).

## Sources

- [Ultimate Guide to Writing Software Engineering Bullet Points - Canyon](https://www.usecanyon.com/career-center/ultimate-guide-to-writing-software-engineering-bullet-points)
- [Strong Bullets for Technical Resumes - UT Austin CNS Career Services](https://careerservices.cns.utexas.edu/resources/resumes/strong-bullets-technical-resumes)
- [An Ex-Meta Recruiter's Inside Guide to Creating a Stand Out SWE Resume - Formation](https://formation.dev/blog/software-engineer-resume-guide-examples)
- [Software Engineer Resume Bullets: 25 Metric-Driven Examples - CareerScribeAI](https://blog.careerscribeai.com/software-engineer-resume-bullets-2/)
