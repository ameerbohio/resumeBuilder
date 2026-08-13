---
name: ats-score
description: Standardized ATS-parseability evaluation of a resume draft - simulates how an applicant tracking system parses and keyword-matches the file, independent of the rubric score. Use when asked to "ATS check", "ATS score", "will this parse", or as one of the three gating evals pass-criteria requires before a draft can finalize.
---

# ATS score

`raw-score` measures whether the content earns credit against the JD.
This measures something different and orthogonal: whether an
applicant tracking system's parser can actually *see* that content in
the first place. A resume can be a perfect 10/10 on the rubric and
still lose to a parsing failure — a two-column layout that scrambles
reading order, a date format the parser can't normalize, a skill that
only exists as a synonym the ATS's exact-match index doesn't index.
This skill checks the second thing.

## Why a separate eval, not folded into raw-score

Rubric scoring and ATS parseability fail for different reasons and are
fixed by different people. A rubric gap means the candidate lacks (or
undersells) something — a Stage 2/3 content problem. A parseability
failure means the content is fine but the *document* is hostile to
machine extraction — a formatting problem, usually introduced by
`bold`, `render_resume.py`/`resume.css`, or a structural choice made
early and never re-checked. Merging the two into one number would hide
which kind of fix is actually needed.

## This runs in a subagent

Same reasoning as `raw-score`: spawn a fresh `Agent` tool call
(`subagent_type: general-purpose`, `run_in_background: false` — the
result gates a pass-criteria decision). Build the prompt from scratch;
the subagent has no memory of this pipeline. Give it:

1. The path to the rendered draft — prefer the **rendered PDF**
   (`.claude/skills/render/render_resume.py` output) over the markdown
   source where one exists, since ATS parsers ingest the submitted
   file, not the markdown. If no PDF has been rendered yet for this
   draft, render one first (or note in the report that this run
   checked markdown-as-proxy and flag that as a caveat, not a pass).
2. The job description path, for the literal-keyword-match step.
3. Steps 1-4 below verbatim.
4. The exact output format from this file.
5. An instruction to change no files and return the report as its
   final message. (Rendering the PDF, if needed, is the one allowed
   side effect — same file `page-fit-check` already produces.)

## Procedure

1. **Structural parseability** — check each, PASS/FAIL, no partial credit
   (an ATS parser either handles a construct or it doesn't):
   - Single column, linear reading order (no tables, text boxes, or
     multi-column layout that would interleave when extracted as a
     flat text stream).
   - No images, icons, or graphics carrying information (a rating bar,
     a logo standing in for a company name, etc.) — text only.
   - No headers/footers holding content that matters (name, contact
     info, or any bullet). Many ATS parsers drop header/footer regions
     entirely.
   - Standard, embedded (non-outlined) text — confirm the PDF is
     text-extractable, not a flattened image, by checking that
     `render_resume.py`'s output is generated from HTML/CSS text (it
     is, by construction, but confirm no step rasterized it).
2. **Section recognition** — for each of Summary, Experience, Skills,
   Education (whichever the draft includes): is the header text one of
   the small set of literal strings ATS section-detectors match against
   (e.g. "Experience" / "Work Experience" / "Professional Experience" —
   not a stylized or merged label like "What I've Built")? Flag any
   header that's clever but non-standard.
3. **Contact and date parsing** — name and contact block sit at the top
   as plain text (not the header/footer region); phone/email in a
   recognizable format; every date range uses one consistent, standard
   pattern (e.g. "Mon YYYY – Mon YYYY" or "YYYY–YYYY") parseable by a
   date-range extractor. Flag any inconsistency between entries — a
   parser calibrated on the first date format in the doc often
   misreads a later one that departs from it.
4. **Literal keyword match rate** — unlike `raw-score`'s
   keyword-alignment component (which allows a synonym or a
   near-equivalent phrase to count), most ATS keyword filters do exact
   or near-exact string matching. For every named tool/technology/skill
   in the JD, check whether that **exact string** (reasonable case-
   insensitive, common abbreviation-expansion pairs like "JS" /
   "JavaScript" allowed) appears somewhere in the draft. Report the hit
   rate as a fraction. This is intentionally stricter than raw-score's
   equivalent component — that's the point of a second eval.

## Scoring and threshold

```
Structural parseability: PASS/FAIL per check (4 checks) — any FAIL is
  a **critical fail**: it means content an ATS would otherwise credit
  becomes invisible to it.
Section recognition:     N/M standard headers
Contact & date parsing:  PASS/FAIL per check (3 checks)
Keyword match rate:      N/M exact matches (%)

ATS score = 10 × (structural_pass_fraction × 0.4
                 + section_recognition_fraction × 0.2
                 + contact_date_pass_fraction × 0.2
                 + keyword_match_rate × 0.2)
```

**Threshold to pass this gate: score ≥ 8.5/10 AND zero critical fails
in structural parseability.** A critical fail cannot be averaged away
by a high keyword match rate — a scrambled reading order or a dropped
header/footer means the matched keywords may never reach the parser's
index at all, so the failure mode isn't "somewhat worse," it's
"silently invisible."

## Output format

```
## ATS score: X.X/10 — PASS/FAIL

### Structural parseability
| Check | Result | Note |
|---|---|---|
| Single-column / linear order | PASS/FAIL | |
| No images/icons carrying info | PASS/FAIL | |
| No header/footer content | PASS/FAIL | |
| Text-extractable (not rasterized) | PASS/FAIL | |

### Section recognition: N/M standard
- <header text> — standard / non-standard (suggest: <alt>)

### Contact & date parsing
| Check | Result | Note |
|---|---|---|
| Contact block plain-text, in body | PASS/FAIL | |
| Contact fields recognizable format | PASS/FAIL | |
| Date ranges consistent format | PASS/FAIL | |

### Keyword match rate: N/M (X%)
| JD term | Exact match in draft? |

**Verdict:** PASS (score ≥ 8.5, no critical fails) / FAIL — <what to fix>
```

## Notes

- This is one of three gating evaluations (with `raw-score` and
  `hr-simulation`) that `pass-criteria` requires to all clear their
  thresholds before a draft finalizes. Per the pipeline's cadence
  decision, this runs only at `pass-criteria` checkpoints, not on every
  compaction pass — it's a document-shape check, not a wording check,
  so it doesn't drift on every edit the way `raw-score` can.
- A critical fail here is almost always a formatting regression from
  `bold` or the render pipeline, not a content problem — hand it back
  to whichever pass touched formatting last, not to `compactor`.
- A "non-standard header" call in section recognition is a convention
  judgment, not a hard parsing fact — it's the one part of this skill's
  output that fits `sanity-check`'s "standardness assumption" trigger.
  If a header gets flagged non-standard and it's not obviously true
  (e.g. "Projects" or "Technical Skills," which are common enough to
  just accept), it's worth grounding before rewriting a section title
  over it. The structural-parseability and keyword-match sections are
  literal checks, not assumptions, and never need this.
