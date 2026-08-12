---
name: job-research
description: Research the specific hiring team, product, and company hiring signals behind a job posting, and save the findings alongside that job description. Use after Stage 1 fit rating, or whenever the user asks what the team actually works on or what this employer looks for in a resume.
---

# Job research

Gathers context the JD text itself does not state, and persists it so it
survives the conversation.

## Where it goes

`1-job-descriptions/<slug>/research.md` — **always**, never
`research-notes/`. That folder is generic, cross-application best practice
only; keeping employer names out of it is deliberate, so the repo does not
advertise where the user is applying. If a finding is genuinely generic
(applies to any application), it belongs in `research-notes/` instead —
split the file rather than filing a mixed one in the wrong place.

## What to look for

Two or three targeted searches, aimed at the **specific team or product**
named in the posting, not the company in general:

- The team's engineering handbook / org page, and its neighbours in the
  same org (sibling teams often describe the shared mission more plainly
  than the JD does).
- The product the team owns: what it's actually built with, what its
  configuration surface looks like. Overlap with the candidate's stack
  that the JD never thought to ask for is exactly the kind of signal
  worth having in an interview.
- Company-stated hiring/resume signals: careers-page guidance, hiring
  handbook pages, engineering-blog posts about what they look for.
- First-hand accounts of the hiring process. Note honestly when these
  turn out to contain nothing usable — a recorded dead end saves the next
  person the search.

## Hard constraint

**Findings here are never folded into the rubric score.** The rubric only
scores what the JD itself states; mixing in externally-researched criteria
would make two applications scored against different, undocumented
criteria sets, breaking `CLAUDE.md` rule 5. Report them as **Bonus signals
(not scored)** and keep them out of every numeric component.

They can still legitimately inform: which true bullet to surface, how to
phrase something in the team's own vocabulary, and interview prep.

## File format

```markdown
# Job/company-specific research — <Company>, <Role>

Company- and team-specific findings only. Generic resume best practice
belongs in `research-notes/` at the repo root instead.

## Team/product context (bonus signals, not scored)
- **<finding>** — <why it could land well, and that the JD never asked>

## What <company> itself signals about resumes/hiring
- **<finding>** — <implication for this application>

## How this was applied
<or "Informational only so far — no draft changes made from this note.">

## Sources
- [title](url)
```
