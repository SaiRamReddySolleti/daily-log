#!/usr/bin/env python3
"""Write one dated learning-log entry and refresh the README index.

Run daily by .github/workflows/daily-log.yml. Idempotent: if today's entry
already exists, it exits 0 without touching anything, so a re-run or a second
scheduled attempt is harmless.
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "topics.md"
ENTRIES = ROOT / "entries"
README = ROOT / "README.md"

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")
API_URL = "https://api.anthropic.com/v1/messages"
MAX_ATTEMPTS = 3

SYSTEM = """You write a short daily engineering learning-log entry for Sai, a \
ServiceNow developer with ~2.5 years of consulting experience (CSM, ITSM, HRSD, SPM) \
who is also finishing an M.S. in Applied Artificial Intelligence.

Rules for the entry:
- 150-250 words. No preamble, no sign-off, no "today I learned" throat-clearing.
- Open with the specific claim or mechanism, not a definition of the field.
- Include exactly one concrete artifact: a short code/script snippet, a config
  fragment, a query, or a worked numeric example. Fence it properly.
- Prefer the non-obvious detail a practitioner would actually get wrong over the
  textbook summary. Name the failure mode.
- Write plainly. No marketing adjectives, no bullet-point padding, no emoji.
- Output GitHub-flavoured Markdown only. Do NOT include a top-level H1 title -
  the script adds it.
"""


def api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        sys.exit("ANTHROPIC_API_KEY is not set. Add it under Settings > Secrets and variables > Actions.")
    return key


def call_claude(prompt: str) -> str:
    body = json.dumps({
        "model": MODEL,
        "max_tokens": 1200,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    last = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        req = urllib.request.Request(
            API_URL,
            data=body,
            headers={
                "content-type": "application/json",
                "x-api-key": api_key(),
                "anthropic-version": "2023-06-01",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                payload = json.load(resp)
            return "".join(
                b.get("text", "") for b in payload.get("content", []) if b.get("type") == "text"
            ).strip()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last = exc
            detail = ""
            if isinstance(exc, urllib.error.HTTPError):
                detail = exc.read().decode("utf-8", "replace")[:400]
                # Client errors other than rate limiting will not fix themselves.
                if exc.code not in (408, 409, 429) and exc.code < 500:
                    sys.exit(f"Anthropic API returned {exc.code}: {detail}")
            print(f"attempt {attempt}/{MAX_ATTEMPTS} failed: {exc} {detail}", file=sys.stderr)
            if attempt < MAX_ATTEMPTS:
                time.sleep(5 * attempt)

    sys.exit(f"Anthropic API unreachable after {MAX_ATTEMPTS} attempts: {last}")


def load_topics() -> tuple[list[str], list[str]]:
    """Return (pending, done) topic titles from topics.md checkboxes."""
    if not TOPICS.exists():
        return [], []
    pending, done = [], []
    for line in TOPICS.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*-\s*\[( |x|X)\]\s+(.*\S)\s*$", line)
        if m:
            (done if m.group(1).lower() == "x" else pending).append(m.group(2))
    return pending, done


def mark_done(topic: str) -> None:
    if not TOPICS.exists():
        return
    out = []
    hit = False
    for line in TOPICS.read_text(encoding="utf-8").splitlines():
        m = re.match(r"(\s*-\s*)\[ \](\s+)(.*\S)\s*$", line)
        if m and not hit and m.group(3) == topic:
            line = f"{m.group(1)}[x]{m.group(2)}{m.group(3)}"
            hit = True
        out.append(line)
    TOPICS.write_text("\n".join(out) + "\n", encoding="utf-8")


def pick_topic(done: list[str], pending: list[str]) -> str:
    if pending:
        return pending[0]
    recent = "\n".join(f"- {t}" for t in done[-40:]) or "- (nothing yet)"
    topic = call_claude(
        "The backlog is empty. Propose ONE new learning-log topic for Sai that is "
        "not a repeat of anything below and is narrow enough to cover properly in "
        "200 words. Reply with the topic title alone - no quotes, no punctuation at "
        f"the end, no explanation.\n\nAlready covered:\n{recent}"
    )
    return topic.splitlines()[0].strip().lstrip("-").strip()[:120]


def slug(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def rebuild_readme(count: int) -> None:
    rows = []
    for path in sorted(ENTRIES.rglob("*.md"), reverse=True)[:14]:
        first = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                first = line[2:].strip()
                break
        rel = path.relative_to(ROOT).as_posix()
        rows.append(f"| `{path.stem}` | [{first or path.stem}]({rel}) |")

    table = "\n".join(rows) if rows else "| | _no entries yet_ |"
    README.write_text(
        f"""# daily-log

A short, dated engineering note every day — things I'm working through as a
ServiceNow developer and an Applied AI grad student. One entry, one idea, one
concrete example.

Written and committed automatically each morning by a
[GitHub Actions workflow](.github/workflows/daily-log.yml); the topic backlog
lives in [`topics.md`](topics.md).

**{count} {"entry" if count == 1 else "entries"}** · browse them all in [`entries/`](entries/)

## Recent

| Date | Entry |
| --- | --- |
{table}

---

<sub>Generated with Claude. Content is a learning log, not documentation — expect
rough edges and the occasional thing I got wrong and corrected later.</sub>
""",
        encoding="utf-8",
    )


def main() -> None:
    today = date.today()
    out = ENTRIES / str(today.year) / f"{today.isoformat()}.md"

    if out.exists():
        print(f"{out.relative_to(ROOT)} already exists; nothing to do.")
        return

    pending, done = load_topics()
    topic = pick_topic(done, pending)
    print(f"topic: {topic}")

    covered = "\n".join(f"- {t}" for t in done[-25:]) or "- (nothing yet)"
    body = call_claude(
        f"Write today's entry on: {topic}\n\n"
        f"For context, these were covered recently — do not rehash them:\n{covered}"
    )
    if len(body) < 120:
        sys.exit(f"Generated entry looks truncated ({len(body)} chars); refusing to commit.")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"# {topic}\n\n*{stamp}*\n\n{body}\n", encoding="utf-8")

    mark_done(topic)
    rebuild_readme(len(list(ENTRIES.rglob("*.md"))))

    msg = f"{today.isoformat()}: {topic}"
    print(f"wrote {out.relative_to(ROOT)}")
    if env_file := os.environ.get("GITHUB_ENV"):
        with open(env_file, "a", encoding="utf-8") as fh:
            fh.write(f"ENTRY_MSG={msg}\n")


if __name__ == "__main__":
    main()
