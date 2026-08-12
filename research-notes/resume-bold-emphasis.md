# Bold-text emphasis: what earns it, how much is too much

Generic, cross-application research — not tied to any employer or JD.
Gathered 2026-08-11 while building the `bold` skill.

## Searched

- Recruiter eye-tracking / skim-time studies and what bolding does for them
- Whether ATS parsing is affected by bold formatting
- Practical guidance on JD-keyword bolding vs. generic emphasis

## Key findings

- **Skim time is ~6-7.4 seconds** (TheLadders eye-tracking study; corroborated
  by Jobscan). Bolding exists to create eye-anchors inside that window, not
  to add visual weight for its own sake.
- **Density ceiling: ~10-15% of total text bolded.** Past that, the document
  reads as visually overwhelming and the emphasis stops functioning as an
  anchor — "the most common error is excessive bolding, which defeats the
  formatting's purpose." (Climb the Ladder, Weekday) This is a ceiling to
  stay under, not a target to hit.
- **Bold complete, standalone-meaningful phrases only** — a metric with its
  unit ("reduced costs by 25%"), or a real keyword/tool name. Never a
  fragment, and never filler ("very", "the") — each bolded span needs to
  carry its meaning if a reader's eye catches only the bolded spans and
  nothing else. (Climb the Ladder)
- **Two candidate categories, in priority order:**
  1. Numbers/quantified results — "the most impactful application of
     bolding" per multiple sources, since scale of impact is what a
     6-second skim is hunting for.
  2. JD-named tools/skills/keywords — matches what the specific reader is
     pattern-matching against for *this* application, not resumes in
     general. (Jobscan: "highlight the keywords in the job description...
     map them to your experience, using the posting's wording.")
  A bullet with both should get at most one of each, not every candidate
  it contains.
- **ATS parsing does not care.** Applicant tracking systems strip
  formatting and match on raw text before a human ever sees the resume, so
  bold has zero effect on keyword-matching scores — it is purely a
  human-skimmer optimization. (ResuFit, Kickresume) This means bolding
  should never be reasoned about as a scoring lever; it only affects the
  soft "does a skimming human decide to interview me" read.
- **Structural bold (role/company/project headers, skills-line category
  labels) is a different thing and doesn't count toward the density
  ceiling** — those are navigation aids, not skim-bait. The ceiling applies
  to bold added *inside* bullet bodies.

## Correction (2026-08-11): vanity/size metrics are not metric-tier candidates

Found on the first real run of the `bold` skill: "~11K LOC" (lines of
code) was bolded as the metric candidate on Automail's overview bullet.
Wrong call. Lines-of-code has roughly 40 years of engineering consensus
against it as a productivity/quality signal — Dijkstra called it "a very
costly measuring unit because it encourages the writing of insipid
code," and the standard criticism holds that great engineers often write
*less* code, that it can't compare across languages/paradigms, and that
a good refactor often *reduces* the count. (CodePulse, Workweave, The
Pragmatic CTO) It's the textbook case of a **vanity metric** — easy to
produce, high-looking number, no correlation to skill or outcome — as
opposed to an **impact metric** (financial, operational-efficiency, or
scope/outcome-tied). (Databowl, Teal)

**Rule this produces:** a raw size/volume count with no outcome attached
(lines of code, but also things in the same shape — a bare item count
that doesn't map to scope, scale, or a before/after) does not qualify as
a metric-tier bold candidate, even though it is technically a number.
The test isn't "is there a digit here," it's "does this number show
scale of impact or efficiency gained." Counts that *do* map to a scored
requirement's scope (e.g. "50+ requirements" evidencing a
structured-requirements-body claim, "17 versioned design specs"
evidencing schema-evolution work) are not vanity metrics under this
test — they're scope evidence for a specific claim, which is a real
signal. The distinguishing question: does the count exist to prove
*this bullet's own achievement*, or does it just describe volume of
output with no tie to a result? LOC failed that test; requirements-count
and design-spec-count pass it.

## How this was applied

Used to build `.claude/skills/bold/SKILL.md`: one bolded span per bullet
by default (two only on a bullet carrying both a distinct metric and a
distinct JD-named keyword), prioritizing metrics then JD-Required/
Highly-Valued keyword matches, with a hard 10-15% density check on the
bullet-body character count before finishing the pass.

## Sources

- [TheLadders Eye-Tracking Study](https://www.bu.edu/com/files/2018/10/TheLadders-EyeTracking-StudyC2.pdf)
- [Should You Bold Words in Your Resume? — Climb the Ladder](https://climbtheladder.com/should-you-bold-words-in-your-resume/)
- [Should You Bold Keywords in Your Resume? — Weekday](https://www.weekday.works/post/bold-text-resume)
- [Does Italic and Bold Formatting Hurt ATS Compatibility? — ResuFit](https://resufit.com/blog/does-italics-and-bold-formatting-hurt-your-resumes-ats-compatibility/)
- [Resume Job Description keyword tailoring — Jobscan](https://www.jobscan.co/blog/tailor-resume-job-description/)
