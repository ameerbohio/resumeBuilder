#!/usr/bin/env python3
"""Render a pipeline resume markdown file to a print-ready PDF via headless Chrome.

Usage:
    python render_resume.py <input.md> [-o <output.pdf>] [--html-only]

Prints a summary line ending in "PAGES=<n>" so callers can gate on page count
without parsing the PDF themselves. Exit code is 0 even for multi-page output --
page count is data, not an error.

Expected markdown shape (what the pipeline's 4-final-drafts files look like):

    Name
    Tagline line
    contact • line • with [links](url)

    ## Experience
    **Role, Company**, Sept 2024 - Current
    - bullet
    ## Projects
    **Project: Tagline**, Tech, Stack, List
    - bullet
    ## Education
    **School**, Degree, June 2022
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


def entry_html(line, section):
    bold, trailing = split_header(line)

    if section == "education":
        # '**School**, Degree, Expected 2028' -> school | degree | date(right)
        degree, date = trailing, ""
        if "," in trailing:
            head, tail = trailing.rsplit(",", 1)
            if DATE_RE.search(tail):
                degree, date = head.strip(), tail.strip()
        left = f"<b>{inline(bold)}</b>"
        if degree:
            left += f", {inline(degree)}"
        return (
            f'<div class="entry"><span class="left">{left}</span>'
            f'<span class="date">{inline(date)}</span></div>'
        )

    if trailing and DATE_RE.search(trailing) and len(trailing) < 40:
        # Job entry: '**Role, Company**, Date'
        if "," in bold:
            role, company = bold.split(",", 1)
            left = f"<b>{inline(role.strip())}</b>, <i>{inline(company.strip())}</i>"
        else:
            left = f"<b>{inline(bold)}</b>"
        return (
            f'<div class="entry"><span class="left">{left}</span>'
            f'<span class="date">{inline(trailing)}</span></div>'
        )

    # Project entry: '**Name: Tagline**, tech, stack' -> name - tagline (tech)
    if ":" in bold:
        name, tag = bold.split(":", 1)
        left = f"<b>{inline(name.strip())}</b> - <b>{inline(tag.strip())}</b>"
    else:
        left = f"<b>{inline(bold)}</b>"
    if trailing:
        left += f" <i>({inline(trailing)})</i>"
    return f'<div class="entry"><span class="left">{left}</span></div>'


def md_to_html(md):
    lines = md.replace("\r\n", "\n").split("\n")
    # Strip any HTML comments (fit-score headers etc.) before parsing.
    lines = [l for l in lines if not l.strip().startswith("<!--")]

    body, section, in_list = [], "", False
    head = [l for l in lines[:6] if l.strip()][:3]
    consumed = 0
    if head:
        body.append(f'<div class="name">{inline(head[0])}</div>')
        consumed = 1
        if len(head) > 1 and not head[1].startswith("#"):
            body.append(f'<div class="tagline">{inline(head[1])}</div>')
            consumed = 2
        if len(head) > 2 and not head[2].startswith("#"):
            body.append(f'<div class="contact">{inline(head[2])}</div>')
            consumed = 3

    seen = 0
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if seen < consumed and not stripped.startswith("#"):
            seen += 1
            continue

        def close():
            nonlocal in_list
            if in_list:
                body.append("</ul>")
                in_list = False

        if stripped.startswith("## "):
            close()
            title = stripped[3:].strip()
            key = title.lower()
            if body and body[-1].startswith("</div>"):
                pass
            if section:
                body.append("</div>")
            section = (
                "education" if "education" in key
                else "skills" if "skill" in key
                else "entries"
            )
            body.append(f"<h2>{inline(title)}</h2>")
            body.append(
                f'<div class="{"edu" if section == "education" else section}">'
            )
        elif stripped.startswith("- ") and section == "skills":
            close()
            body.append(f"<p>{inline(stripped[2:])}</p>")
        elif stripped.startswith("- "):
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{inline(stripped[2:])}</li>")
        elif stripped.startswith("**"):
            close()
            body.append(entry_html(stripped, section))
        else:
            close()
            body.append(f"<p>{inline(stripped)}</p>")

    if in_list:
        body.append("</ul>")
    if section:
        body.append("</div>")

    with open(CSS_PATH, encoding="utf-8") as fh:
        css = fh.read()
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<style>{css}</style></head><body>\n" + "\n".join(body) + "\n</body></html>"
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
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as fh:
        html_doc = md_to_html(fh.read())

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
