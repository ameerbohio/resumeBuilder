---
name: bold
description: Bold the highest-value metric and JD-matched keyword in each bullet, within a density ceiling, so a skimming reader's eye lands on the strongest signal without the page looking noisy. Use as the last content-adjacent pass in Stage 3, once wording and order are settled and just before page-fit-check/finalize.
---

# Bold

A pure emphasis pass. No wording changes, no new claims, no reordering —
if a bullet needs any of those, that's `compactor`, `skim-readability`,
or `reorder` first. Full rationale in
`research-notes/resume-bold-emphasis.md`; the summary that matters:

- Bolding exists to catch a 6-7 second skim, not to add visual weight.
- ATS parsing is irrelevant — parsers strip formatting before matching.
  This is entirely a human-skimmer play; never reason about it as a
  rubric lever.
- Past ~10-15% of bulleted text bolded, emphasis stops being an anchor
  and starts reading as noise. Over-bolding is the default failure mode.

## When to run

**Last**, after `compactor`, `skim-readability`, and `reorder` have all
settled — bolding a phrase that a later wording pass then rewrites away
is wasted work, the same reason Stage 2.5 runs before compaction. Re-run
whenever a bullet's wording changes after this pass ran.

Operates on `3-compact-drafts/<slug>.md`'s current-best draft (the body
below the Compaction Log). `0-experience/experience.md` stays plain —
bold is presentation layer only, never applied to the source.

## Selection, per bullet

Pick **one** bolded span per bullet by default. A bullet may earn a
second only if it carries both a metric and a JD keyword that don't
overlap and the bullet is long enough to carry two anchors without
crowding. Never bold a whole clause or a filler word — a bolded span
must mean something read in isolation.

Priority when a bullet has multiple candidates:

1. **The bullet's own quantified result** — the number/percentage/scale
   word plus its unit, not a bare digit. `"cutting p95 latency 10.79ms
   to 5.80ms"` bolds `5.80ms` or the delta, not `5.80`.

   **Exclude vanity/size metrics** — a count with no outcome attached
   (lines of code being the canonical example; ~40 years of engineering
   consensus treats LOC as a bad-to-meaningless signal — see
   `research-notes/resume-bold-emphasis.md`'s correction note). The test
   is not "is there a digit here," it's "does this number show scale of
   *impact or efficiency*, or *scope tied to a scored claim*." A count
   that only measures volume of output (LOC, a bare item tally with
   nothing depending on it) fails this test even though it's a number —
   route to a JD keyword in that bullet instead, or skip the bullet.
2. **A literal JD Required/Highly-Valued term**, in the JD's own
   wording where the draft already uses it — pull the term list from
   `1-job-descriptions/<slug>/job-description.md`'s `## Fit Rating`
   evidence, since those are exactly the phrases a recruiter is
   pattern-matching against for *this* application. Prefer the term
   that scored Clear pass or Partial and is currently unbolded
   elsewhere — don't bold the same keyword twice across bullets unless
   it's the strongest anchor in both.
3. If neither is present, skip the bullet. Not every bullet needs a
   bolded span — a bullet with no metric and no JD term is not the
   place to force one.

Skills-line category labels (`**Languages:**`) and entry headers
(`**Company, Role**`) are structural, not skim-bait, and don't count
toward the density ceiling or need selection logic — leave them as-is.

## Density check

After selecting, measure bolded characters **inside bullet bodies only**
(lines starting with `- `, excluding entry headers and skills-line
category labels) against total bullet-body characters:

```bash
python -c "
import re
lines = [l for l in open('3-compact-drafts/<slug>.md', encoding='utf-8')
          if l.startswith('- ')]
body = ''.join(lines)
bold = sum(len(m) for m in re.findall(r'\*\*(.+?)\*\*', body))
total = len(re.sub(r'\*\*', '', body))
print(f'{bold}/{total} = {bold/total:.1%}')
"
```

If over ~15%, cut the weakest spans first (a metric already implied by
an adjacent bolded number, or a JD keyword that's a Strong-Plus/narrative
item rather than Required/Highly-Valued) until back under the ceiling.

## Page-fit interaction

`**` markers add 4 characters per bolded span. On a page already near
capacity (this repo's compact drafts routinely are), this can push a
draft over. **Always re-run `page-fit-check` after this pass** — do not
assume character-count math predicts the render, same reason that skill
exists at all.

## Log entry

Append to the Compaction Log, same discipline as `reorder`:

```markdown
### Iteration N — Bold pass (density check, no wording change)

- **Score:** X/10 (unchanged — bold markup doesn't add or remove a
  claim; if a fit-rating verdict changed because a keyword's presence
  became more/less legible, that's a `raw-score` question, not this
  pass's to answer)
- **Chars:** before → after (bold markers only) · running total
- **Bolded:** a flat list — bullet (first ~6 words) -> span bolded ->
  which priority tier (metric / JD keyword)
- **Density:** N% of bullet-body characters (ceiling 15%)
- **Risk check:** one line; call out if page-fit-check needed a redo
```

## After finalizing

If this runs on a slug that already has a populated `4-final-drafts/`,
it's a post-finalize edit — copy the bolded clean draft over, re-render
the PDF in the same turn, and say so explicitly. Same rule `finalize`
itself states: a stale PDF next to a corrected markdown file is this
pipeline's worst failure mode.
