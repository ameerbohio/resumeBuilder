---
name: page-fit-check
description: Render a resume draft to PDF with headless Chrome and report the real page count and remaining space, instead of estimating page fit from character count. Use whenever you need to know if a draft fits one page, or before finalizing.
---

# Page fit check

Answers "does this fit on one page?" by **rendering it**, not by
estimating. Character counts do not predict page breaks — this repo's
first application burned two full iterations on manual Google Docs round
trips to answer exactly this question.

## Run it

```bash
python .claude/skills/render/render_resume.py <draft.md> -o <out.pdf>
```

Prints `PDF: <path> PAGES=<n>`. For a `3-compact-drafts/` file, extract
the body below the Compaction Log first — the renderer expects the resume
text only:

```bash
awk '/^<first line of resume body>/{f=1} f{print}' \
  3-compact-drafts/<slug>.md > "$SCRATCH/fitcheck.md"
python .claude/skills/render/render_resume.py "$SCRATCH/fitcheck.md" \
  -o "$SCRATCH/fitcheck.pdf"
```

Write intermediate files to the scratchpad, not the repo.

## Reading the result

- `PAGES=1` — fits. Read the PDF to judge remaining whitespace: a page
  with visible room at the bottom can absorb another bullet, which is
  the signal `pass-criteria` gate 2 and any "I have room for one more
  line" request depends on.
- `PAGES=2` — does not fit. Report **how much** overflow (read the PDF
  and describe how far down page 2 the content reaches). "Two lines
  over" and "half a page over" call for very different next passes.
- Two pages is only acceptable when seniority genuinely warrants it, and
  `CLAUDE.md` requires the Compaction Log to record that as a deliberate
  call rather than a failure to compact.

## Judging headroom

Read the rendered PDF directly to see the layout. Estimate remaining
capacity in **bullets**, not characters — one more bullet of typical
length is the unit the user actually decides in.

## Calibration

`.claude/skills/render/resume.css` is tuned to match
`4-final-drafts/Ameer_Bohio_Resume_Gitlab.pdf`, the reference one-page
render (Times, ~10.5pt body, 0.5in x 0.6in margins, Letter). Changing
that stylesheet invalidates every prior page-fit judgment — if it must
change, re-render the reference draft and confirm it still lands on one
page with comparable whitespace before trusting any new result.

The renderer expects the pipeline's standard markdown shape (name /
tagline / contact, then `## Section` headers, `**Bold header**, trailing`
entry lines, `- ` bullets, and `- **Category:** items` under Technical
Skills). Structural deviations render oddly rather than failing loudly,
so glance at the PDF, not just the page count.
