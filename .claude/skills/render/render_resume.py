#!/usr/bin/env python3
"""Render a pipeline resume markdown file to a print-ready PDF via headless Chrome.

Usage:
    python render_resume.py <input.md> [-o <output.pdf>] [--html-only]

Prints a summary line ending in "PAGES=<n>" so callers can gate on page count
without parsing the PDF themselves. Exit code is 0 even for multi-page output --
page count is data, not an error.

Expected markdown shape, calibrated against a candidate's own original resume
(`4-final-drafts/!!!!RESUME (1).pdf` -- supersedes the earlier Ameer_Bohio
reference, which was a different person's tech-resume placeholder used only
because it was the first file available when this renderer was built):

    Name
    contact line (not italic)
    link line

    ## Role Title
    (first section header only: centered, larger, no rule -- a title, not a
    section divider)
    Keyword ● Keyword ● Keyword ● Keyword
    (a line with 2+ "●" separators renders centered+bold, like a tagline)
    Summary paragraph, left-aligned normal body text.

    ## Experience
    (every "## " after the first: centered, letter-spaced, ruled underneath)
    **Company**, Location
    *Role, Department*, Date
    (two-line entry: bold company/location row, then italic role/date row --
    NOT the single-line "**Role, Company**, Date" some earlier drafts used)
    - bullet
    ## Education
    **School**
    *Degree*, June 2022
    *Certification Name*, 2024
    (a standalone italic line with a date is its own single-row entry, for
    certifications with no separate institution line)
    ## Technical Skills
    - **Category:** items
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(HERE, "resume.css")

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
# A trailing fragment counts as a date (right-aligned) if it looks like one.
DATE_RE = re.compile(r"(19|20)\d{2}|current|present|expected|ongoing", re.I)


def find_chrome():
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def inline(text):
    """Minimal inline markdown -> HTML. Escapes first, so markers survive."""
    out = html.escape(text, quote=False)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", out)
    return out


def split_header(line):
    """'**Bold part**, trailing text' -> ('Bold part', 'trailing text')."""
    m = re.match(r"^\*\*(.+?)\*\*\s*,?\s*(.*)$", line.strip())
    if not m:
        return line.strip().strip("*"), ""
    return m.group(1).strip(), m.group(2).strip()


def split_italic_header(line):
    """'*Italic part*, trailing text' -> ('Italic part', 'trailing text')."""
    m = re.match(r"^\*(.+?)\*\s*,?\s*(.*)$", line.strip())
    if not m:
        return line.strip().strip("*"), ""
    return m.group(1).strip(), m.group(2).strip()


def entry_row(left_html, trailing, extra_class=""):
    date = f'<span class="date">{inline(trailing)}</span>' if trailing else ""
    cls = f"entry {extra_class}".strip()
    return f'<div class="{cls}"><span class="left">{left_html}</span>{date}</div>'


def entry_html(line, section):
    """Fallback single-line entry: no matching two-line role/date row
    followed it. Covers a Projects line ('**Name: Tagline**, tech, stack')
    and, for backward compatibility, the older single-line
    '**Role, Company**, Date' shape some earlier drafts used."""
    bold, trailing = split_header(line)

    # Education: '**School**, Degree, Date' -- always split degree from date
    # on the LAST comma (a degree name can itself contain commas) and put
    # the degree on the left, date right-aligned. Without this, the generic
    # heuristic below only right-aligns the date when the whole "Degree,
    # Date" trailing text happens to be under 40 chars and produces a
    # completely different (parenthetical, left-side) layout when it's
    # longer -- two education entries of different degree-name length would
    # render inconsistently with each other, which is exactly what happened.
    if section == "education" and trailing and "," in trailing:
        degree, date = (p.strip() for p in trailing.rsplit(",", 1))
        if DATE_RE.search(date):
            left = f"<b>{inline(bold)}</b>, {inline(degree)}"
            return entry_row(left, date)

    if trailing and DATE_RE.search(trailing) and len(trailing) < 40:
        if "," in bold:
            role, company = bold.split(",", 1)
            left = f"<b>{inline(role.strip())}</b>, <i>{inline(company.strip())}</i>"
        else:
            left = f"<b>{inline(bold)}</b>"
        return entry_row(left, trailing)

    if ":" in bold:
        name, tag = bold.split(":", 1)
        left = f"<b>{inline(name.strip())}</b> - <b>{inline(tag.strip())}</b>"
    else:
        left = f"<b>{inline(bold)}</b>"
    if trailing:
        left += f" <i>({inline(trailing)})</i>"
    return f'<div class="entry"><span class="left">{left}</span></div>'


def md_to_html(md, ats_safe=False):
    raw_lines = md.replace("\r\n", "\n").split("\n")
    # Strip any HTML comments (fit-score headers etc.) before parsing.
    lines = [l.strip() for l in raw_lines if l.strip() and not l.strip().startswith("<!--")]
    n = len(lines)

    body = []
    i = 0

    # Head: name / contact line / link line -- up to 3 lines, stop at '#'.
    head = []
    while i < n and len(head) < 3 and not lines[i].startswith("#"):
        head.append(lines[i])
        i += 1
    if head:
        body.append(f'<div class="name">{inline(head[0])}</div>')
        if len(head) > 1:
            body.append(f'<div class="contact">{inline(head[1])}</div>')
        if len(head) > 2:
            body.append(f'<div class="contact">{inline(head[2])}</div>')

    section = ""
    in_list = False
    first_h2 = True
    # A continuation line (no blank line, no special prefix -- how every
    # draft's bullets and summary paragraphs are manually wrapped for
    # git-diff readability) accumulates as RAW text here and is only run
    # through inline() once, on flush. Running inline() per-fragment and
    # then string-splicing the results (an earlier version of this fix)
    # breaks any **bold**/*italic* span that straddles the wrap point --
    # the opening ** and closing ** end up in different fragments and
    # neither half matches on its own, so both render as literal
    # asterisks. Blank lines are stripped before this loop even runs, so
    # this pending buffer is the only surviving paragraph-boundary signal.
    pending_tag = None  # "li" | "p" | None
    pending_raw = ""

    def close_list():
        nonlocal in_list
        if in_list:
            body.append("</ul>")
            in_list = False

    def flush():
        nonlocal pending_tag, pending_raw
        if pending_tag:
            body.append(f"<{pending_tag}>{inline(pending_raw)}</{pending_tag}>")
            pending_tag, pending_raw = None, ""

    while i < n:
        stripped = lines[i]

        if stripped.startswith("## "):
            flush()
            close_list()
            title = stripped[3:].strip()
            key = title.lower()
            if section:
                body.append("</div>")
            section = (
                "education" if "education" in key
                else "skills" if "skill" in key
                else "entries"
            )
            # The centered/no-rule "role title" treatment is for an actual
            # tagline under the name (e.g. "## Senior Backend Engineer"),
            # not for whichever section happens to come first. A resume
            # that opens straight into "## Experience" (no separate title
            # line) must render that header exactly like every other
            # section header -- same left alignment, same rule -- or the
            # first section visually breaks consistency with the rest.
            is_named_section = any(
                k in key for k in ("experience", "project", "education", "skill", "summary")
            )
            if first_h2 and not is_named_section:
                body.append(f'<h2 class="title">{inline(title)}</h2>')
            else:
                body.append(f"<h2>{inline(title)}</h2>")
            first_h2 = False
            body.append(
                f'<div class="{"edu" if section == "education" else section}">'
            )
            i += 1
            continue

        if stripped.startswith("- ") and section == "skills":
            flush()
            close_list()
            pending_tag, pending_raw = "p", stripped[2:]
            i += 1
            continue

        if stripped.startswith("- "):
            flush()
            if not in_list:
                body.append("<ul>")
                in_list = True
            pending_tag, pending_raw = "li", stripped[2:]
            i += 1
            continue

        if stripped.startswith("**"):
            flush()
            close_list()
            bold, trailing = split_header(stripped)
            next_line = lines[i + 1] if i + 1 < n else ""
            next_is_role_line = next_line.startswith("*") and not next_line.startswith("**")
            bold_trailing_is_date = bool(trailing) and DATE_RE.search(trailing)
            if next_is_role_line and not bold_trailing_is_date:
                # Two-line entry: '**Company**, Location' + '*Role*, Date'
                role_bold, role_trailing = split_italic_header(next_line)
                body.append('<div class="entry-block">')
                body.append(entry_row(f"<b>{inline(bold)}</b>", trailing))
                body.append(entry_row(f"<i>{inline(role_bold)}</i>", role_trailing, "sub"))
                body.append("</div>")
                i += 2
                continue
            body.append(entry_html(stripped, section))
            i += 1
            continue

        if stripped.startswith("*") and not stripped.startswith("**"):
            flush()
            close_list()
            # Standalone italic entry, e.g. a certification with no
            # separate institution line: '*Cert Name*, 2024'.
            italic, trailing = split_italic_header(stripped)
            if trailing and DATE_RE.search(trailing):
                body.append(entry_row(f"<i>{inline(italic)}</i>", trailing))
            else:
                pending_tag, pending_raw = "p", stripped
            i += 1
            continue

        if stripped.count("●") >= 2 or stripped.count("•") >= 2:
            # A "Keyword ● Keyword ● Keyword" line renders as a centered,
            # bold tagline rather than a plain paragraph.
            flush()
            close_list()
            body.append(f'<p class="keywords">{inline(stripped)}</p>')
            i += 1
            continue

        # Catch-all: a continuation line with no special prefix. Append
        # its raw text into whatever block is still pending rather than
        # closing it.
        if pending_tag:
            pending_raw += " " + stripped
        else:
            close_list()
            pending_tag, pending_raw = "p", stripped
        i += 1

    flush()
    close_list()
    if section:
        body.append("</div>")

    with open(CSS_PATH, encoding="utf-8") as fh:
        css = fh.read()
    body_class = ' class="ats-safe"' if ats_safe else ""
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<style>{css}</style></head><body{body_class}>\n" + "\n".join(body) + "\n</body></html>"
    )


def page_count(pdf_path):
    with open(pdf_path, "rb") as fh:
        data = fh.read()
    return len(re.findall(rb"/Type\s*/Page[^s]", data)) or 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output")
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument(
        "--ats-safe", action="store_true",
        help="Swap entry-header/bullet layout to a non-flex, non-positioned "
             "variant that keeps PDF content-stream text in document order "
             "for naive/raw ATS parsers. Not the default -- the flex layout "
             "is the calibrated visual standard; use this only when "
             "parseability needs to win over exact visual match.",
    )
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as fh:
        html_doc = md_to_html(fh.read(), ats_safe=args.ats_safe)

    base = os.path.splitext(os.path.abspath(args.input))[0]
    html_path = base + ".render.html"
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html_doc)

    if args.html_only:
        print(f"HTML: {html_path}")
        return 0

    out = os.path.abspath(args.output or base + ".pdf")
    chrome = find_chrome()
    if not chrome:
        print("ERROR: no Chrome/Edge binary found; cannot render PDF.", file=sys.stderr)
        return 2

    url = "file:///" + html_path.replace("\\", "/")
    cmd = [
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", f"--print-to-pdf={out}", url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(out):
        print(proc.stderr[-800:] or "chrome produced no output", file=sys.stderr)
        return 2

    os.remove(html_path)
    n = page_count(out)
    print(f"PDF: {out} PAGES={n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
