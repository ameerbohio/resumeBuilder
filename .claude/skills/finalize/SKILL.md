---
name: finalize
description: Close out an application - copy the winning draft clean into 4-final-drafts, render the submission PDF, and report the final score against the baseline ceiling. Use when pass-criteria passes, or the user says to finalize or move a resume to final drafts.
---

# Finalize (Stage 3 steps 5-6)

## Precondition

`pass-criteria` returns PASS. If the user asks to finalize with gates
open, say which are open and let them decide — do not silently skip the
check, and do not refuse a deliberate call.

## Procedure

1. **Extract the clean draft** from `3-compact-drafts/<slug>.md` — the
   body below the Compaction Log, with no log, no HTML comments, no
   annotations. The log stays intact in the compact draft
   (`CLAUDE.md` hard rule 6); it is simply omitted from the copy.

   ```bash
   awk '/^<first line of resume body>/{f=1} f{print}' \
     3-compact-drafts/<slug>.md > 4-final-drafts/<slug>.md
   ```

2. **Verify byte-identical** to the compact draft's body:

   ```bash
   diff <(awk '/^<first line>/{f=1} f{print}' 3-compact-drafts/<slug>.md) \
     4-final-drafts/<slug>.md && echo IDENTICAL
   ```

3. **Render the PDF:**

   ```bash
   python .claude/skills/render/render_resume.py \
     4-final-drafts/<slug>.md -o "4-final-drafts/<Name>_Resume_<Company>.pdf"
   ```

   Confirm `PAGES=` matches the target, then read the PDF to check the
   layout actually looks right — the renderer degrades quietly on
   unexpected markdown rather than erroring.

4. **Report:** final score next to the baseline ceiling (they should be
   equal), number of passes it took, total character reduction since
   Stage 2, and the PDF path.

## After finalizing

`4-final-drafts/<slug>.md` is the submittable artifact — no further
automatic changes. If a later turn edits it (a user request, a
correction), that edit goes through `propagate-edit` and the PDF must be
re-rendered, or the shipped file and the markdown silently diverge.

Keep the `.md` and the `.pdf` in sync as a pair. A stale PDF next to a
corrected markdown file is the worst failure mode this stage has, because
nothing in the repo makes it visible.
