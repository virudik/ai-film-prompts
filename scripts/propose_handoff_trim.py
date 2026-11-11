#!/usr/bin/env python3
"""Propose a handoff trim as a reviewable diff. Never merges.

Owner decision 11.11.2026: when canon-health reports handoff-size or
project-handoff-size, the robot may move old dated blocks into the archive and
open a pull request. It does not trim the handoff on main and it does not merge
that pull request. The reviewer compares every moved block with the current
state and puts back anything that is still current or important.

Kept in the live file:
* the preamble before the first heading;
* the newest «СЕЙЧАС» / «Сейчас» section, including its rule subsections
  («Кто что делает», «Действующие решения», «Что открыто», «Как продолжать»);
* any other section whose heading is a standing rule;
* bold-label bullets (they carry rules) even when they sit under «Ранее».

Moved verbatim, newest proposal first:
* older «СЕЙЧАС» sections;
* dated non-rule sections older than the current date;
* «Ранее …» groups, except bold-label rule bullets;
* bullets under «Новое с последней чистки» whose date is strictly older;
* dated ### subsections of the current «СЕЙЧАС» that are not rule subsections.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DATE_RE = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(20\d\d)\b")
SHORT_DATE_RE = re.compile(r"(?<!\d)(\d{1,2})\.(\d{1,2})(?!\.\d)")
YEAR_RE = re.compile(r"\b(20\d\d)\b")
HEADING_RE = re.compile(r"^(#{1,3}) ")
SEICHAS_RE = re.compile(r"сейчас", re.I)
RULE_RE = re.compile(
    r"правил|как чистить|источник истины|старт для сменщика|живое состояние|"
    r"важно|абсолютн|решени[ея] владельца|продолжай и приём|кнопки владельца|"
    r"медленная генерация|папка и id",
    re.I)
PROTECTED_SUB_RE = re.compile(
    r"кто что делает|действующие решения|что открыто|как продолжать",
    re.I)
NOVOE_RE = re.compile(r"новое с последней чистки", re.I)
RANEE_RE = re.compile(r"^\*\*Ранее\b", re.I)
BOLD_BULLET_RE = re.compile(r"^\s*[-*]\s+\*\*")
REVIEW_SENTENCE = (
    "Перед вливанием проверяющий сверяет перенос с текущим состоянием: "
    "каждый уносимый блок должен быть действительно устаревшим. "
    "Всё, что ещё актуально или важно, нужно вернуть в хендоф. "
    "Робот этот PR не вливает."
)


def document_year(text, now=None):
    years = [int(y) for y in YEAR_RE.findall(text or "")]
    if years:
        return max(years)
    return (now or datetime.now(timezone.utc)).year


def parse_date(text, year=None):
    match = DATE_RE.search(text or "")
    if match:
        try:
            return datetime(int(match.group(3)), int(match.group(2)), int(match.group(1)), tzinfo=timezone.utc)
        except ValueError:
            return None
    if year:
        short = SHORT_DATE_RE.search(text or "")
        if short:
            try:
                return datetime(int(year), int(short.group(2)), int(short.group(1)), tzinfo=timezone.utc)
            except ValueError:
                return None
    return None


def split_level(text, level):
    """Split on headings of exactly `level` hashes. Preamble stays put."""
    mark = "#" * level + " "
    lines = text.splitlines(keepends=True)
    pre, sections, current = [], [], None
    for line in lines:
        if line.startswith(mark) and not line.startswith(mark + "#"):
            current = [line]
            sections.append(current)
        elif current is None:
            pre.append(line)
        else:
            current.append(line)
    return "".join(pre), ["".join(part) for part in sections]


def first_line(block):
    for line in block.splitlines():
        if line.strip():
            return line.strip()
    return ""


def archive_entry(source, blocks):
    body = "\n\n".join(block.strip() for block in blocks if block.strip())
    return (
        f"# Предложение чистки · блоки из `{source}`\n\n"
        "Дословный перенос. Это не новое правило: проверяющий возвращает в хендоф всё, что ещё действует.\n\n"
        + body
        + "\n"
    )


def newest_date(parts, year=None):
    found = [parse_date(part, year) for part in parts]
    found = [item for item in found if item]
    return max(found) if found else None


def trim_seichas(section, current, moved, year):
    """Return the kept «СЕЙЧАС» section. Appends moved pieces to `moved`."""
    lines = section.splitlines(keepends=True)
    heading, rest = lines[0], "".join(lines[1:])
    pre, subs = split_level(rest, 3)
    kept_pre, moved_pre = trim_ranee(pre)
    moved.extend(moved_pre)
    kept_subs = []
    for sub in subs:
        title = first_line(sub)
        if PROTECTED_SUB_RE.search(title):
            kept_subs.append(sub)
            continue
        if NOVOE_RE.search(title):
            kept_subs.append(trim_novoe(sub, current, moved, year))
            continue
        when = parse_date(title, year)
        if when and current and when < current:
            head, tail = peel_embedded_rules(sub)
            if head.strip():
                moved.append(head)
            if tail.strip():
                kept_subs.append(tail)
            continue
        kept_subs.append(sub)
    body = kept_pre.rstrip() + "\n\n" + "".join(kept_subs)
    return heading + body.lstrip("\n") if body.strip() else heading


def trim_ranee(text):
    """Move «**Ранее …**» groups. Bold-label bullets stay in the live text."""
    lines = text.splitlines(keepends=True)
    kept, moved, bucket, moving = [], [], [], False

    def flush():
        nonlocal bucket, moving
        if not bucket:
            return
        chunk = "".join(bucket)
        if moving and chunk.strip():
            moved.append(chunk)
        else:
            kept.append(chunk)
        bucket, moving = [], False

    for line in lines:
        if RANEE_RE.match(line.lstrip()):
            flush()
            moving = True
            bucket = [line]
            continue
        if moving and BOLD_BULLET_RE.match(line) and re.search(
                r"приоритет|не запускать|не восстанавливать|правило", line, re.I):
            flush()
            kept.append(line)
            continue
        if moving and line.strip() == "" and bucket and bucket[-1].strip() == "":
            flush()
            kept.append(line)
            continue
        bucket.append(line)
    flush()
    return "".join(kept), moved


def trim_novoe(section, current, moved, year):
    lines = section.splitlines(keepends=True)
    heading, body = lines[0], lines[1:]
    kept, chunk = [heading], []

    def flush():
        nonlocal chunk
        if not chunk:
            return
        text = "".join(chunk)
        when = parse_date(first_line(text), year)
        if when and current and when < current and text.strip() and not lead_kept(text):
            moved.append(text)
        else:
            kept.append(text)
        chunk = []

    for line in body:
        if BOLD_BULLET_RE.match(line) and chunk:
            flush()
        chunk.append(line)
    flush()
    return "".join(kept)


def propose(text, archive_text, source, now=None):
    """Return (live, archive, moved_labels) or None when nothing old is dated."""
    now = now or datetime.now(timezone.utc)
    year = document_year(text, now)
    pre, sections = split_level(text, 2)
    # A single '#' title is inside `pre` when the next heading is '##'.
    title_pre, title_sections = split_level(pre, 1)
    candidates = [parse_date(title_pre, year)]
    candidates.extend(parse_date(first_line(section), year) for section in sections if SEICHAS_RE.search(first_line(section)))
    dated = [item for item in candidates if item]
    current = max(dated) if dated else newest_date([title_pre], year)

    moved = []
    kept_titles = [trim_loose_dated(section, current, moved, year) for section in title_sections]
    kept_sections = []
    for section in sections:
        title = first_line(section)
        when = parse_date(title, year)
        if SEICHAS_RE.search(title):
            if when and current and when < current:
                moved.append(section)
            else:
                kept_sections.append(trim_seichas(section, current, moved, year))
            continue
        if RULE_RE.search(title):
            kept_sections.append(section)
            continue
        if when and current and when < current:
            moved.append(section)
            continue
        kept_sections.append(trim_loose_dated(section, current, moved, year))

    if not moved:
        return None
    live = title_pre + "".join(kept_titles) + "".join(kept_sections)
    live = re.sub(r"\n{3,}", "\n\n", live).rstrip() + "\n"
    labels = [first_line(block)[:160] for block in moved]
    entry = archive_entry(source, moved)
    archive = entry.rstrip() + "\n\n" + (archive_text or "").lstrip()
    if not archive.endswith("\n"):
        archive += "\n"
    return live, archive, labels


def peel_embedded_rules(section):
    """A dated subsection can contain the live role/decision block. Keep that tail."""
    lines = section.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if re.match(r"^\*\*(Кто что делает|Действующие решения)", line):
            return "".join(lines[:index]), "".join(lines[index:])
    return section, ""


def lead_kept(text):
    """Blockquotes and standing-rule lines stay even when they carry an old date."""
    lead = first_line(text)
    if lead.startswith(">"):
        return True
    return bool(RULE_RE.search(text) or re.search(
        r"приоритет|не запускать|не восстанавливать|потолок 6|только с согласия|не пересоздавать", text, re.I))


def trim_loose_dated(section, current, moved, year):
    """Inside a kept non-rule section, move top-level dated blocks older than current.

    Blockquotes and lines that state a standing rule stay.
    """
    lines = section.splitlines(keepends=True)
    if not lines:
        return section
    heading, body = lines[0], lines[1:]
    kept, chunk = [heading], []

    def flush():
        nonlocal chunk
        if not chunk:
            return
        text = "".join(chunk)
        lead = first_line(text)
        when = parse_date(lead, year)
        if when and current and when < current and text.strip() and not lead_kept(text):
            moved.append(text)
        else:
            kept.append(text)
        chunk = []

    for line in body:
        if (re.match(r"^\s*[-*]\s+", line) or re.match(r"^\*\*", line)) and chunk:
            flush()
        if re.match(r"^#{1,3} ", line):
            flush()
            kept.append(line)
            continue
        chunk.append(line)
    flush()
    return "".join(kept)


def targets(root):
    health_path = Path(root) / "canon-health.json"
    try:
        health = json.loads(health_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    found = []
    for problem in health.get("problems") or []:
        if not isinstance(problem, dict):
            continue
        if problem.get("level") != "warn" or problem.get("code") not in ("handoff-size", "project-handoff-size"):
            continue
        rel = problem.get("file")
        if isinstance(rel, str) and rel.endswith("HANDOFF.md"):
            found.append(rel)
    return found


def archive_for(root, handoff_rel):
    path = Path(handoff_rel)
    if path.parent == Path("."):
        return "archive/handoff-log.md"
    return str(path.parent / "archive" / "handoff-log.md")


def apply(root, now=None):
    root = Path(root)
    changed = []
    for rel in targets(root):
        src = root / rel
        if not src.is_file():
            continue
        arch_rel = archive_for(root, rel)
        arch = root / arch_rel
        result = propose(src.read_text(encoding="utf-8"),
                         arch.read_text(encoding="utf-8") if arch.is_file() else "",
                         rel, now)
        if not result:
            continue
        live, new_arch, labels = result
        src.write_text(live, encoding="utf-8")
        arch.parent.mkdir(parents=True, exist_ok=True)
        arch.write_text(new_arch, encoding="utf-8")
        changed.append({"file": rel, "archive": arch_rel, "moved": labels})
    return changed


def pr_body(changed):
    lines = [
        "Робот предлагает чистку хендофа. Он не вливает этот PR.",
        "",
        REVIEW_SENTENCE,
        "",
        "В архив уходят только старые датированные блоки. Блок «СЕЙЧАС» и правила остаются.",
        "",
    ]
    for item in changed:
        lines.append(f"### `{item['file']}`")
        lines.extend(f"- {label}" for label in item["moved"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def notify_text(pr_url, changed):
    files = ", ".join(item["file"] for item in changed) or "хендоф"
    return (
        "Робот подготовил отдельный PR с предлагаемой чисткой хендофа и сам его не вливает.\n"
        f"{REVIEW_SENTENCE}\n"
        f"PR: {pr_url}\n"
        f"Файлы: {files}"
    )


def send_notice(root, pr_url, changed):
    """DM the same Agent Relay address that receives canon-health warnings."""
    import relay_wake
    cfg = relay_wake.load_config(root)
    text = notify_text(pr_url, changed)
    return relay_wake.send_dm(
        root, text, address=cfg.get("site_alert_address"), key_prefix="handoff-trim-", require_enabled=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--write", action="store_true", help="write the proposal into the worktree; do not merge")
    parser.add_argument("--pr-body", action="store_true", help="print the pull-request body for a proposal already applied")
    parser.add_argument("--body-json", help="read a previous --write JSON report and print the PR body or notice")
    parser.add_argument("--notify-text", help="print the Agent Relay notice for this PR url")
    args = parser.parse_args(argv)
    if args.body_json:
        report = json.loads(Path(args.body_json).read_text(encoding="utf-8"))
        changed = report.get("proposals") or []
        if args.notify_text:
            print(notify_text(args.notify_text, changed))
        else:
            print(pr_body(changed), end="")
        return 0
    if args.pr_body or args.notify_text:
        changed = []
    else:
        changed = apply(args.root) if args.write else []
        if not args.write:
            root = Path(args.root)
            for rel in targets(root):
                src = root / rel
                arch_rel = archive_for(root, rel)
                arch = root / arch_rel
                if not src.is_file():
                    continue
                result = propose(src.read_text(encoding="utf-8"),
                                 arch.read_text(encoding="utf-8") if arch.is_file() else "", rel)
                if result:
                    _, _, labels = result
                    changed.append({"file": rel, "archive": arch_rel, "moved": labels})
    if args.notify_text:
        print(notify_text(args.notify_text, changed))
        return 0
    if args.pr_body:
        print(pr_body(changed), end="")
        return 0
    print(json.dumps({"changed": bool(changed), "proposals": changed}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
