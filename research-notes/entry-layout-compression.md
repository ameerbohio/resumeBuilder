---
Searched: how to save vertical space on an entry (company/role/date row)
without cutting bullet content. Prompted by comparing the pipeline's
default two-line entry against `4-final-drafts/Ameer_Bohio_Resume_GitLab.pdf`,
which uses a single-line entry for the same information.
---

# Entry layout compression

## The two formats

**Two-line entry** (this pipeline's Stage 2 default — see
`page-fit-check`'s Calibration section):

```
**Company**, Location
*Role, Department*, Date
- bullet
```

**Single-line entry** (already supported by `render_resume.py`'s
`entry_html` fallback — triggers whenever a bold entry line isn't
followed by a matching italic role line):

```
**Role**, Company                                          Date
- bullet
```

written as `**Role**, Company, Date` in the markdown — one line, no
follow-up italic line. Seen in production in
`4-final-drafts/Ameer_Bohio_Resume_GitLab.pdf`'s Experience section
(`**Software Engineer**, Pratt & Whitney Canada` / `Sept 2024 - Current`)
and its Projects section (`**Automail - E2EE Physical Document
Delivery**, Go, TypeScript, ...` as a bold name + italic parenthesized
tech list, also one line).

## Trade-off

The single-line form saves a full text row per entry — real space on a
page where the two-line form is the single biggest per-entry cost. It
costs two things:

- **Location drops out** (or has to be folded into the bullet text if
  it's JD-relevant — e.g. a location-restricted role).
- **Company loses its own bold line** — it's now a comma-clause after
  the bold Role, visually subordinate to it. Fine when the Role title is
  the stronger signal for this JD (common in tech/engineering resumes,
  where the JD matches against title/seniority); worse when the
  employer's name is doing real credibility work the reader needs to see
  first (a recognizable brand, a target-company connection).

## When it's worth it

- A section with **many short entries** (several roles at the same
  company, a list of certifications) where the two-line form's fixed
  per-entry overhead compounds fastest.
- Entries where **Location carries no JD signal** (JD isn't
  location-sensitive, or every entry is in the same place anyway, so
  repeating it two-line-style adds nothing).
- As a **Stage 3 compaction lever** when a draft is close to fitting and
  cutting further bullet content would cost rubric points — layout
  compression buys space without touching wording or evidence. See
  `compactor`'s lever list.

Not a Stage 2 default: `draft-initial` still writes two-line entries so
the initial draft carries full information, and this compression is
applied deliberately, entry-by-entry, only where the trade-off is worth
it for a specific draft.
