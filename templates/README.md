# Resume templates

Reference resumes for **visual/structural format** — entry layout
(company/role/date arrangement), header style, bullet style, spacing —
not for section order. Point Claude at one when you want a draft
formatted like a specific known-good layout.

**Section order is deliberately not part of what a template dictates.**
Whether to lead with Education or Experience, whether Projects earns its
own section, depends on the candidate's experience level and what's
strongest for the JD at hand — that's a per-application judgment call,
not something a template should fix in place. A template supplies format
conventions only, never content and never section ordering: content
still comes solely from `0-experience/experience.md` (hard rules 1 and
2), and the result must stay ATS-safe (hard rule 4).

## How to use one

Tell Claude which file to follow when you kick off `draft-initial`
(Stage 2) — e.g. "follow the format in `templates/jakes_resume_format.pdf`"
or just "use the Jake's Resume format." Claude matches that file's entry
layout, header style, and bullet conventions, while still deciding
section order per-application and pulling all content from
`experience.md`.

If you don't specify one, `draft-initial` falls back to
`jakes_resume_format.pdf` as the default.

## Available templates

| File | Description |
|---|---|
| `jakes_resume_format.pdf` | "Jake's Resume" — one of the most widely recommended ATS-safe formats (a standing recommendation on r/EngineeringResumes): single-line contact block, two-line company/role entries with right-aligned dates, small-caps ruled section headers, categorized skills line. **Default template**, and also the visual calibration reference for the pipeline's built-in PDF renderer — see `.claude/skills/page-fit-check/SKILL.md`'s Calibration section. |

## Adding your own

Drop a reference resume in this folder — a real PDF you like the look
of, or a filled-in `.md` example (fictional content is fine; it's a
format reference, never a content source) written in the renderer's
expected markdown shape. See `.claude/skills/page-fit-check/SKILL.md`'s
Calibration section for that shape. If you add a markdown example, render
it once —

```bash
python .claude/skills/render/render_resume.py templates/<your-file>.md -o "$SCRATCH/check.pdf"
```

— and look at the output before trusting it; a construct the renderer
hasn't seen before can render oddly without failing loudly. Then list it
in the table above so it's discoverable. Note that only the **default**
template doubles as the renderer's visual calibration reference — adding
a second template gives Stage 2 a new format to follow, but the built-in
PDF preview still renders in the single calibrated visual style unless
someone deliberately recalibrates `resume.css` against the new file too.
