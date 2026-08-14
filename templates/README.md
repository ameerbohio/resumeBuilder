# Resume templates

Reference examples of **structure and wording conventions** a draft can
follow — section order, entry format, bullet style — not visual
stylesheets. Point Claude at one when you want a draft shaped like a
specific known-good layout instead of the pipeline's default section
order.

Every draft still renders through the pipeline's single calibrated
`.claude/skills/render/resume.css` (see `page-fit-check`'s Calibration
section in `.claude/skills/page-fit-check/SKILL.md`) regardless of which
template you follow — a template controls what sections exist and what
order they're in, not fonts, spacing, or column layout. All the usual
hard rules from `CLAUDE.md` still apply on top of any template: content
only ever comes from `0-experience/experience.md` (hard rules 1 and 2),
and the result must stay ATS-safe (hard rule 4). A template file supplies
shape, never content.

## How to use one

Tell Claude which file to follow when you kick off `draft-initial`
(Stage 2) — e.g. "follow the template in `templates/jakes-resume.md`" or
just "use the Jake's Resume template." Claude matches that file's section
order and entry conventions while pulling actual content only from
`experience.md`.

If you don't specify one, `draft-initial` falls back to `jakes-resume.md`
as the default.

## Available templates

| File | Description |
|---|---|
| `jakes-resume.md` | "Jake's Resume" — one of the most widely recommended ATS-safe layouts (a standing recommendation on r/EngineeringResumes): tight single-column structure, plain ruled section headers, right-aligned dates, categorized skills line. **Default template.** |

## Adding your own

Drop a filled-in example `.md` file in this folder (fictional content is
fine — it's a shape reference, never a content source) written in the
renderer's expected markdown shape: see `.claude/skills/page-fit-check/SKILL.md`'s
Calibration section, or just copy `jakes-resume.md` and restructure it.
Render it once with

```bash
python .claude/skills/render/render_resume.py templates/<your-file>.md -o "$SCRATCH/check.pdf"
```

and look at the output before trusting it — a construct the renderer
hasn't seen before (per that skill's calibration notes) can render oddly
without failing loudly. Then list it in the table above so it's
discoverable.
