import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import propose_handoff_trim as proposal  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

FIXTURE = """# Пример

> **01.11.2026 — правило запуска:** см. `ops/LAUNCHER-COORDINATION.md`.

## СЕЙЧАС (обновлено 10.11.2026)

**Ранее 08.11.**
- Передача 08.11: исторический статус.
- **Приоритет 23.10:** свободный слот берёт следующий готовый сюжет.

### Очередь сюжетов (09.11.2026)

52 успешен. Не запускать: 62.

**Кто что делает.**
- **ChatGPT:** читает очередь.

**Действующие решения владельца**
- **Две версии промта** остаются.

### Новое с последней чистки

- **10.11 — сцена 88:** текущая.
- **09.11 — старое фото:** не пересоздавать; длинная история.
- **08.11 — чат:** уже сдано.

## ВАЖНО: граница

Не генерировать платно.

## Исторический снимок · 02.11.2026

Старые цены.
"""


class ProposeHandoffTrim(unittest.TestCase):
    def test_moves_old_dated_blocks_and_keeps_rules(self):
        result = proposal.propose(FIXTURE, "", "NEW-CHAT-HANDOFF.md")
        self.assertIsNotNone(result)
        live, archive, labels = result
        self.assertIn("Приоритет 23.10", live)
        self.assertIn("Две версии промта", live)
        self.assertIn("Кто что делает", live)
        self.assertIn("правило запуска", live)
        self.assertIn("10.11 — сцена 88", live)
        self.assertIn("не пересоздавать", live)
        self.assertIn("ВАЖНО", live)
        self.assertNotIn("Передача 08.11", live)
        self.assertNotIn("08.11 — чат", live)
        self.assertNotIn("Старые цены", live)
        self.assertIn("Передача 08.11", archive)
        self.assertIn("Старые цены", archive)
        self.assertIn("08.11 — чат", archive)
        self.assertTrue(labels)
        self.assertIsNone(proposal.propose(live, archive, "NEW-CHAT-HANDOFF.md"))

    def test_notice_tells_the_reviewer_not_to_merge_blindly(self):
        text = proposal.notify_text("https://example.test/pull/1", [{"file": "NEW-CHAT-HANDOFF.md", "moved": ["old"]}])
        body = proposal.pr_body([{"file": "NEW-CHAT-HANDOFF.md", "moved": ["old"]}])
        for message in (text, body):
            self.assertIn(proposal.REVIEW_SENTENCE, message)
            self.assertIn("не вливает", message)
        self.assertIn("https://example.test/pull/1", text)

    def test_workflow_trims_registers_and_does_not_merge_handoff_prs(self):
        workflow = (ROOT / ".github/workflows/service-maintenance.yml").read_text(encoding="utf-8")
        rules = (ROOT / "ops/SERVICE-MAINTENANCE.md").read_text(encoding="utf-8")
        self.assertIn("python3 scripts/trim_service_files.py . --write --skip-held-locks", workflow)
        self.assertIn("scripts/propose_handoff_trim.py", workflow)
        self.assertIn("40 4 * * *", workflow)
        self.assertNotIn("gh pr merge", workflow)
        self.assertIn("does not merge", workflow)
        self.assertIn(proposal.REVIEW_SENTENCE, rules)
        self.assertIn("source: self-heal", (ROOT / "ops/SELF-HEAL.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
