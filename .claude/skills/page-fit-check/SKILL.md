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

Prints `PDF: <path> PAGES=<n>`.

**Stage 3's first `page-fit-check` runs against `3-compact-drafts/<slug>.md`**,
not `2-initial-drafts/<slug>.md`. Copy the Stage 2 draft in as the
starting point first (Stage 3 step 1 in `CLAUDE.md`), including any
structural/formatting fixes — never edit `2-initial-drafts` after it's
confirmed; it's the frozen baseline-ceiling record, not a working file.

For a `3-compact-drafts/` file, extract
the body below the Compaction Log first — the renderer expects the resume
text only:

```bash
awk '/^<first line of resume body>/{f=1} f{print}' \
  3-compact-drafts/<slug>.md > "$SCRATCH/fitcheck.md"
python .claude/skills/render/render_resume.py "$SCRATCH/fitcheck.md" \
  -o "$SCRATCH/fitcheck.pdf"
```

Write intermediate files to the scratchpad, not the repo.

**Send the rendered PDF to the user** (via the file-send tool) every time
this runs during Stage 3 — a scratchpad render that only Claude reads
means the user is taking compaction progress on faith. This applies even
to intermediate, not-yet-finished states; label the caption so it's
clearly a Stage 3 preview and not the submission-ready file from
`finalize`.

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
`4-final-drafts/!!!!RESUME (1).pdf`, the candidate's own original resume
(Times, ~10.5pt body, 0.5in x 0.6in margins, Letter). An earlier version
of this file was calibrated against `Ameer_Bohio_Resume_Gitlab.pdf`
instead — a different person's tech resume, used only because it was the
one reference file on hand when the renderer was first built. That
mismatch is why an early session produced bullets whose wrapped lines
and entry headers didn't match what the user actually wanted; if you're
looking at a draft that still cites the Ameer file, its formatting is
stale and should be re-run through the current renderer. Changing
`resume.css` invalidates every prior page-fit judgment — if it must
change, re-render the reference and confirm comparable layout before
trusting any new result.

The renderer expects this shape:

```
Name
contact line (not italic)
link line

## Role Title              <- first "## " only: centered, larger, no rule
Keyword ● Keyword ● Keyword     <- 2+ "●" separators -> centered, bold
Summary paragraph, left-aligned.

## Experience               <- every "## " after the first: centered,
                                letter-spaced, ruled underneath
**Company**, Location
*Role, Department*, Date    <- two-line entry, NOT one line
- bullet

## Education
**School**
*Degree*, Date
*Certification Name*, Date  <- standalone italic entry, no institution line

## Technical Skills
- **Category:** items
```

Structural deviations render oddly rather than failing loudly, so glance
at the PDF, not just the page count.

**Manually-wrapped source lines need the renderer to merge them back.**
Every draft wraps bullets and paragraphs across 2+ source lines for
git-diff readability. Both renderers track the last-appended block and
merge a plain continuation line into it — without that, a continuation
line silently closes the current list/paragraph and starts a new,
unindented one (the actual cause of an earlier "bullet indentation looks
wrong" report, which single-line isolated tests failed to reproduce).
If you ever touch the parsing loop in `render_resume.py` or
`render_docx.py`, re-render a draft with a genuinely multi-line bullet
and check the generated HTML/DOCX structure directly, not just the
visual page count.

**A construct the reference never uses can silently break this
calibration.** The current reference *does* use a Summary section and
bare paragraphs (unlike the old Ameer reference, which had none), so the
browser's default `<p>` margin (~1em top+bottom, ~20pt/paragraph) is
already accounted for via a `p { margin: 0 0 3pt; }` reset — but if a
future draft introduces some *other* construct neither reference uses
(a Projects section, a multi-line bullet sub-list, anything not in the
shape above), render it and look at the spacing before trusting the page
count. Don't assume the CSS already covers it just because it covered
the last new construct.
