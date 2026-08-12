# Resume Builder — Rules of Operation

This is not a codebase. It is a personal, private pipeline for producing
job-tailored resumes from a single source-of-truth experience file. Claude
acts as the operator of this pipeline. Follow this file exactly — the stages
below are gated on purpose, and gates must not be skipped or merged.

## Repo layout

Folders are numbered in pipeline order:

```
0-experience/
  experience.md              Master experience dump. Single source of truth.
1-job-descriptions/
  <slug>/
    job-description.md       The job posting, pasted verbatim, plus a
                              "## Fit Rating" section appended by Stage 1.
    research.md               Job/company-specific research (hiring-team
                              signals, product/team context, handbook
                              pages, etc.) — optional, created whenever
                              Stage 1 or a scoring pass turns up something
                              worth keeping. Company-specific research
                              never goes in research-notes/ — see that
                              folder's entry below.
2-initial-drafts/
  <slug>.md                  Stage 2 output: all relevant experience, uncompacted,
                              with a fit score noted at the top and a
                              "## Why This Could Be Rejected" holistic risk
                              read at the bottom. Frozen once the user
                              confirms it — Stage 3 work (including any
                              markdown/formatting fixes) happens in
                              3-compact-drafts instead, never here.
3-compact-drafts/
  <slug>.md                  Stage 3 working file: a "## Compaction Log" section
                              (one entry per pass, with a character count,
                              running total saved, and a Risk check line)
                              followed by the current-best tightened draft.
                              The log is append-only — see hard rule 6.
4-final-drafts/
  <slug>.md                  Stage 3 output once compaction is done: a clean copy
                              of the winning draft with no logs/comments — this is
                              what gets submitted. Empty until a job reaches this
                              point.
research-notes/
  README.md                  Index. Generic, cross-application best-practice
                              research only (skills-section structure,
                              bullet-point readability, work-experience
                              density, etc.) — nothing tied to a specific
                              company, team, or role. Gathered while working
                              applications through the pipeline, kept so it
                              doesn't need re-searching on the next one. Not a
                              pipeline stage — no hard rule reads from it.
                              Company/job-specific research belongs in
                              `1-job-descriptions/<slug>/research.md`
                              instead, never here.
```

The same `<slug>` names the folder under `1-job-descriptions/` and the files
across `2-initial-drafts/` through `4-final-drafts/`, so everything for one
application lines up by name. Naming convention: `company_role-slug` (e.g.
`acme_senior-backend-engineer`) — no date prefix needed since the numbered
folders already separate things by stage.

## Hard rules (apply at every stage)

1. **Never fabricate.** Every bullet, skill, tool, and metric in any draft
   must trace back to something actually present in `0-experience/experience.md`.
   If a job requirement has no basis in that file, say so explicitly (in the
   `## Fit Rating` section as a gap) — do not invent experience to cover it.
2. **`0-experience/experience.md` is read-only during this pipeline.** Stages
   only ever copy/select/rephrase from it into a job's files. If it needs new
   content, that's a separate, explicit editing task the user initiates — not
   something a resume pass does implicitly.
3. **Do not advance stages without explicit user go-ahead.** Each stage below
   ends with a stop-and-wait point. Produce the output, state the result
   plainly (score, what changed, what's flagged), and wait. Do not
   auto-continue to the next stage in the same turn.
4. **Resumes are ATS-safe.** Plain markdown that maps to: standard section
   headers (Summary, Experience, Skills, Education, etc.), reverse
   chronological order, no tables/columns/images/icons, action-verb bullets,
   quantified impact where the source material supports a number.
5. **Scores are always computed the same way** (see rubric below) so they're
   comparable across stages and across iterations within Stage 3.
6. **The `## Compaction Log` in `3-compact-drafts/<slug>.md` is append-only
   and must never be removed, edited, or truncated once written.** Each
   iteration gets a new entry; earlier entries stay exactly as written,
   forming a permanent record of every pass tried on that application. The
   *draft* below the log gets replaced each iteration — the *log* never
   does. (The clean copy sent to `4-final-drafts/<slug>.md` in Stage 3 step 5
   omits the log, but the log stays intact in `3-compact-drafts/<slug>.md`
   itself.) Entries are terse (see Stage 3 step 3), but a `Chars:`
   before/after/saved line plus running total is non-negotiable on every
   entry — brevity trims prose, never the character count.

## Fit rubric (score out of 10)

Score the job description against the candidate material being evaluated
(`experience.md` for Stage 1, a draft for Stage 3) using these weighted
components, then sum:

- **Requirement coverage (0–4):** fraction of the JD's stated
  must-have/preferred requirements that are demonstrably met.
- **Keyword/skill alignment (0–2):** overlap between JD's named tools,
  technologies, and skills and what appears in the candidate material.
- **Seniority & scope match (0–2):** does the title, years of experience,
  and scope of responsibility shown match what the JD is asking for.
- **Quantified impact (0–2):** presence of concrete, relevant metrics/outcomes
  that speak to the JD's priorities.

Always show the component breakdown, not just the total. Always list the
specific gaps that cost points.

### Scoring methodology (avoid grade inflation)

These rules govern how point-by-point verdicts (Clear pass / Partial /
Weak-implicit / Gap) convert into the numeric components above. Apply them
literally rather than eyeballing a number — this is where scores tend to
drift high if done impressionistically:

- **Per-item credit weights**, when averaging verdicts into a component:
  Clear pass = 1.0, Partial = 0.5, Weak-implicit = 0.25, Gap = 0. A
  weak-implicit item (evidence inferred, not stated) is much closer to a gap
  than to a pass — do not let it pull a score up like a near-pass would.
- **Requirement coverage counts only the JD's stated must-have and
  preferred/highly-valued items.** "Stand out" / "strong plus" / bonus
  differentiator sections are explicitly framed by the employer as beyond
  the requirements — mention them in the narrative (they matter for
  competitiveness) but do not fold them into the requirement-coverage
  numerator, since doing so inflates coverage on criteria the JD never
  required.
- **Seniority & scope match penalizes overqualification, not just
  underqualification.** If the JD's own framing signals a growth/mentee
  seat (e.g. "you'll learn from other engineers," scoped-down
  responsibilities, junior/intermediate title) and the candidate material
  shows senior-level ownership/leadership beyond that scope, dock points and
  say so explicitly — this is a real mismatch risk (interview framing, comp
  expectations, retention concern), not a neutral non-issue that rounds up
  to a full match.
- When a corrected score replaces an earlier one within the same file
  (e.g. after catching an inflated first pass), leave a one-line
  recalibration note explaining what changed and why, rather than silently
  overwriting the number.

## Evaluation style preferences

Applies to Stage 1 Fit Rating and Stage 3 re-scoring, as supporting detail
alongside the fixed rubric — rule 5 still holds, the rubric score and
component breakdown are always computed and shown. This section governs the
analysis layered on top of it.

- Break requirements into the JD's own categories (e.g. Required / Highly
  Valued / Strong Plus, or whatever grouping the posting itself uses) and
  give each line item its own verdict — Clear pass / Partial / Weak-implicit
  / Gap — with one to two sentences citing the specific `experience.md`
  evidence behind it.
- End the point-by-point section with a tally line (e.g. "5 clear passes, 2
  partial, 1 gap") before restating the overall rubric score.
- Distinguish a true gap (no evidence exists in `experience.md`) from
  underselling (evidence exists but is buried, low in the draft, or not
  phrased in the JD's own terms). Underselling is a framing/placement fix for
  Stage 2/3, not a requirements gap for Stage 1 — call it out separately.
- When asked "what's missing" or similar, answer with a terse bullet list
  only — no restated reasoning, no scores.
- **"Why this could be rejected" is a standing soft-risk list, separate from
  the scored rubric** — factors like skimmability/density, whether wording
  mirrors the JD's literal terms, seniority-level ambiguity
  (over/under-qualified read), project-work vs. paid-work balance,
  in-progress-degree or availability signals, location/visa ambiguity. It is
  produced proactively at two fixed points (Stage 2 step 4 and Stage 3 step
  3, see below) with different framing at each, and also on demand whenever
  asked directly.
- When proposing specific new or reworded bullets for a draft, score each
  proposed addition individually (0–10, JD relevance) in a small table
  (point / score / why) before folding accepted ones into the draft.

## Stage 1 — Fit Rating

Trigger: user provides or points to a job description for a new application.

1. Pick a `<slug>` (`company_role-slug`) and save the JD verbatim to
   `1-job-descriptions/<slug>/job-description.md`.
2. Read `0-experience/experience.md` in full.
3. Score the fit per the rubric above, using the full experience file as the
   candidate material (not yet tailored to anything).
4. Append a `## Fit Rating` section to the bottom of
   `1-job-descriptions/<slug>/job-description.md`: total score, component
   breakdown, explicit list of gaps/unmet requirements, and a one-line
   recommendation (pursue / stretch / skip).
5. **Stop.** Report the score and top gaps to the user. Wait for them to say
   whether to proceed to Stage 2.

## Stage 2 — Initial Draft

Trigger: user approves the fit rating and says to proceed.

1. Pull **all** experience relevant to this JD from `experience.md` — err
   toward inclusion, not compression. This draft is a comprehensive
   quarry of material, not a final resume. Organize it into standard resume
   sections but do not worry yet about length or tightness.
2. Save as `2-initial-drafts/<slug>.md`.
3. Re-run the fit rubric against this draft and include the score at the top
   of the file as `<!-- fit score: X/10 (components: ...) -->` — this score
   is the **baseline ceiling** that Stage 3 must not drop below.
4. Append a `## Why This Could Be Rejected` section to the bottom of
   `2-initial-drafts/<slug>.md`: a holistic read of the candidate against
   this JD, using the soft-risk factors from Evaluation style preferences
   above. This is evaluated against the full, uncompacted candidate material
   — it's the "even at a good fit score, what makes a recruiter or hiring
   manager set this aside" read for the candidate as a whole, distinct from
   Stage 1's requirement-gap list and from anything compaction will later
   introduce.
5. **Stop.** Report the score and ask the user to review for completeness/
   accuracy — did anything relevant get missed, is anything misrepresented.
   Iterate on this draft directly with the user until they say it's good.
   Do not move to Stage 2.5 until they explicitly confirm.

## Stage 2.5 — Accuracy and metrics (before any compaction)

Trigger: user confirms the Stage 2 draft is complete.

Both steps edit `0-experience/experience.md` at the source (user-initiated
and explicit, so hard rule 2 is satisfied) and propagate downstream. They
run **here**, not later, because compaction rewords bullets — and rewording
a bullet that is about to be corrected or gain a metric is wasted work.
This ordering is the main lever for reducing total iteration count.

1. **Accuracy checkpoint.** Walk the user through every claim whose
   plain reading could overstate what happened: verb strength ("led",
   "owned", "drove"), attribution across projects/employers, skills-line
   entries with no supporting bullet, claims where the technical truth
   differs from the plain reading, and whether existing numbers are
   measured or estimated. Ask once, as one grouped list.
2. **Metrics interview.** Audit which bullets carry no hard number,
   then interview the user for the real ones. "I don't remember" is a
   valid answer — hard rule 1 means no invented figure fills the gap.
3. Apply approved changes to `experience.md` first, then every draft
   stage.
4. **Stop.** Report what changed and re-score if any correction touched
   scored evidence. Wait for the go-ahead to compact.

## Stage 3 — Compaction (iterate to final)

Trigger: user confirms the initial draft is accurate and complete, and says
to compact it.

This is a loop, not a single pass, worked entirely inside
`3-compact-drafts/<slug>.md`. That file has two parts: a `## Compaction Log`
section at the top, and the current-best draft below it.

1. Take the current best version (first pass: `2-initial-drafts/<slug>.md`,
   copied in as the starting point) and produce a tighter version: cut
   redundancy, merge overlapping bullets, sharpen wording, drop material
   that's genuinely low-relevance to this JD.
2. Re-score the tightened version against
   `1-job-descriptions/<slug>/job-description.md` using the same rubric.
3. Compare to the baseline ceiling from `2-initial-drafts/<slug>.md` (and the
   previous iteration's score):
   - If the score **dropped**, identify exactly which component/bullet
     caused the loss, restore or rework that specific point, and re-score.
     Never accept a compaction that costs points.
   - If the score **held**, append an entry to the `## Compaction Log`
     section and replace the draft below it with this new current-best. Per
     hard rule 6, this is strictly additive — never edit or delete a prior
     log entry.
   - **Log entries are terse by default** — the user knows their own
     experience and will ask if something needs explaining, so don't
     re-justify it up front. Format:
     - `Score:` X/10 (unchanged, or component delta if it moved)
     - `Chars:` before → after (−saved, %) · running total saved since
       Stage 2 baseline
     - `Cut/changed:` a flat list of item names only — no rationale
       paragraphs. One clause of "why" only when it's non-obvious (e.g. a
       score-affecting call, or keeping something that looks cuttable but
       isn't).
     - `Risk check:` one line. "No new risk" is a valid, expected answer
       most passes — only expand past one line if this pass actually
       introduced or changed a Stage 2 "Why This Could Be Rejected" risk.
4. Repeat until the seven-gate stop test passes (score floor, page fit,
   accuracy clean, readability clean, diminishing returns confirmed,
   ordering current, bold-emphasis density current — see the
   `pass-criteria` skill). A plateaued score
   is **not** by itself a reason to stop: it measures rubric coverage,
   not whether a skimming human can read the page.

   **Compaction targets page fit, not minimum length.** Cut while the
   draft overflows; once it fits, stop. If cutting overshoots and leaves
   whitespace, add material back from `experience.md` until the page is
   exactly full — those non-decreasing passes are logged like any other.
   A draft that fills the page with content the user wants is done, and
   needs no further compaction pass to prove it.
5. Copy the winning draft — clean, with no log/comments — to
   `4-final-drafts/<slug>.md`, and render the submission PDF. This file
   should be submission-ready as-is.
6. Report the final score next to the baseline ceiling (should be equal) and
   how many compaction passes it took. `4-final-drafts/<slug>.md` is the
   finished, submittable resume — no further automatic changes. If it is
   ever edited later, re-render the PDF in the same turn; a stale PDF
   beside corrected markdown is invisible and is this stage's worst
   failure mode.

## Skills

The pipeline is implemented as atomic skills in `.claude/skills/`,
orchestrated by `run-pipeline`. Prefer invoking the relevant skill over
improvising the stage by hand — each one encodes a mistake this pipeline
has already made once.

| Skill | Stage | Role |
|---|---|---|
| `run-pipeline` | all | Orchestrator; enforces ordering and stage gates |
| `fit-rating` | 1 | Score JD vs. `experience.md`, append Fit Rating |
| `job-research` | 1 | Team/company signals -> `<slug>/research.md` |
| `draft-initial` | 2 | Comprehensive draft + baseline ceiling + risk read |
| `accuracy-checkpoint` | 2.5 | Confirm every claim is literally true |
| `metrics-interview` | 2.5 | Source real numbers for unquantified bullets |
| `compactor` | 3 | One tighten/cut/merge pass, re-score, log |
| `raw-score` | 3 | Blind re-score; catches drift |
| `skim-readability` | 3 | Per-bullet scannability checks |
| `reorder` | 3 | Rank bullets by JD relevance/impact/scope |
| `bold` | 3 | Bold top metric/JD keyword per bullet within a density ceiling |
| `page-fit-check` | 3 | Real rendered page count via headless Chrome; sends the PDF to the user as a preview |
| `pass-criteria` | 3 | The six-gate stop test |
| `propagate-edit` | any | One change across `experience.md` -> all stages |
| `finalize` | 3 | Clean copy to `4-final-drafts/` + PDF |

PDF rendering: `.claude/skills/render/render_resume.py` (+ `resume.css`,
calibrated against `4-final-drafts/!!!!RESUME (1).pdf`, the candidate's
own original resume — two-line `**Company**, Location` /
`*Role, Department*, Date` entries, centered letter-spaced section
headers, round bullets. An earlier version of this calibration used
`Ameer_Bohio_Resume_Gitlab.pdf`, a different person's tech resume kept
only because it was the sole reference file on hand when the renderer
was first built; that mismatch produced visibly wrong entry formatting
and bullet spacing until caught by user feedback. See `page-fit-check`'s
Calibration section for the current expected markdown shape before
trusting a page count on a draft shaped differently from the reference.

Every `page-fit-check` run in Stage 3 sends the rendered PDF to the user
as a preview, not just an internal render read by Claude — the user
should be able to see compaction progress directly, not take it on
faith from a text description.

## Tone/format for resume content

- Bullets start with a strong action verb, past tense for past roles.
- Prefer one line per bullet; avoid nested sub-bullets.
- No first-person pronouns, no photos/graphics.
- A generic objective statement ("seeking a role where I can...") is
  weak and gets skimmed past — but an achievement-focused, quantified,
  role-targeted **summary** is worth the space, per
  `research-notes/professional-summary-effectiveness.md`. Include one
  when there's a real proof point to anchor it; skip or keep to one line
  otherwise.
- Keep to one page of content unless the seniority/experience genuinely
  requires two — note in the `## Compaction Log` if two pages was a
  deliberate call rather than a failure to compact.
