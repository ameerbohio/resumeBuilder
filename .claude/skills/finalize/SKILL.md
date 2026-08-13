---
name: finalize
description: Close out an application - copy the winning draft clean into 4-final-drafts, render the submission PDF, and report the final score against the baseline ceiling. Use when pass-criteria passes, or the user says to finalize or move a resume to final drafts.
---

# Finalize (Stage 3 steps 5-6)

## Precondition

`pass-criteria` returns PASS **and has persisted that verdict** via
`.claude/hooks/record-pass-criteria-state.ps1` (see that skill's last
step). This isn't just a courtesy check anymore: a `PreToolUse` hook
(`.claude/hooks/check-finalize-gate.ps1`) hard-blocks any write to
`4-final-drafts/<slug>.md` — by this step's own copy, a direct `Write`/
`Edit`, whatever — unless `.claude/pipeline-state/<slug>.json` records
a PASS whose hash matches the *current* `3-compact-drafts/<slug>.md`
draft body exactly. If the user asks to finalize with gates open, say
which are open and let them decide — do not silently skip the check —
but know that the hook will refuse the write regardless of what's said
in conversation; there is no "finalize anyway" path around it except
actually getting `pass-criteria` to PASS and persist first.

## Procedure

1. **Extract the clean draft** from `3-compact-drafts/<slug>.md` — the
   body below the Compaction Log, with no log, no HTML comments, no
   annotations. The log stays intact in the compact draft
   (`CLAUDE.md` hard rule 6); it is simply omitted from the copy. The
   split point is the `<!-- draft-below -->` sentinel that `compactor`
   keeps immediately before the draft body (see that skill) — this
   replaced an earlier per-application "first line of resume body"
   pattern specifically so this extraction and the finalize-gate hook
   always agree on where the draft starts:

   ```bash
   awk '/<!-- draft-below -->/{f=1;next} f' \
     3-compact-drafts/<slug>.md > 4-final-drafts/<slug>.md
   ```

2. **Verify byte-identical** to the compact draft's body:

   ```bash
   diff <(awk '/<!-- draft-below -->/{f=1;next} f' 3-compact-drafts/<slug>.md) \
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

4. **Report:** final raw-score next to the baseline ceiling (they should
   be equal), the ats-score and hr-simulation results that cleared
   `pass-criteria`'s gates, number of passes it took, total character
   reduction since Stage 2, and the PDF path.

## After finalizing

`4-final-drafts/<slug>.md` is the submittable artifact — no further
automatic changes. If a later turn edits it (a user request, a
correction), that edit goes through `propagate-edit` and the PDF must be
re-rendered, or the shipped file and the markdown silently diverge.
Because `propagate-edit` changes `3-compact-drafts/<slug>.md` first,
the finalize-gate hook's recorded PASS immediately goes stale (the hash
no longer matches) — `pass-criteria` must run and persist again before
the corrected content can be copied back into `4-final-drafts/`. This
is the hook enforcing the exact invariant this section warns about, not
an extra hoop — a stale PDF beside corrected markdown can no longer
happen silently.

Keep the `.md` and the `.pdf` in sync as a pair. A stale PDF next to a
corrected markdown file is the worst failure mode this stage has, because
nothing in the repo makes it visible.
