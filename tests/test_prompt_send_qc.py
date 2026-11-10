"""Узкая проверка уточнений QA пакета: роли, отправка, квитанция, просмотр ролика."""
import re
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def section(text, start, end):
    i = text.index(start)
    j = text.index(end, i + len(start))
    return text[i:j]


class PromptSendQcTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = (ROOT / "PROMPT-STYLE-GUIDE.md").read_text(encoding="utf-8")
        cls.launch = (ROOT / "ops/TOPVIEW-FREE-LAUNCH.md").read_text(encoding="utf-8")
        cls.sync = (ROOT / "SYNC-RUNBOOK.md").read_text(encoding="utf-8")
        cls.handoff = (ROOT / "NEW-CHAT-HANDOFF.md").read_text(encoding="utf-8")
        cls.handoff_archive = (ROOT / "archive/handoff-log.md").read_text(encoding="utf-8")

    def test_roles_do_not_ban_first_last(self):
        block = section(self.guide, "### A. Структура", "### B. Персонажи")
        self.assertIn("не взаимозаменяемы", block)
        self.assertIn("Мудборд не фиксирует форму реального изделия", block)
        self.assertIn("Reference-only не равен принудительным first/last/keyframe", block)
        self.assertIn("настоящий конец предыдущей части", block)
        self.assertNotIn("запрещены first", block.lower())

    def test_state_chain_has_no_numeric_cap(self):
        block = section(self.guide, "### C. Исполнимость", "### D. Реализм")
        self.assertIn("Порога «не больше N действий» нет", block)
        self.assertIn("на пересечении горловины", block)
        self.assertIsNone(re.search(r"не больше \d+", block))

    def test_send_receipt_and_video_qc_are_general(self):
        block = section(self.guide, "### G. Отправка", "## 12.")
        self.assertIn("любого адаптера генерации", block)
        self.assertIn("не блокируют сохранение мастера", block)
        self.assertIn("дословный реально отправленный промт", block)
        self.assertIn("Хеш мастера не доказывает", block)
        self.assertIn("не выдумывать принятый переписанный текст", block)
        self.assertIn("не заменяют проверку движения", block)
        self.assertIn("не выдумывать покадровую зависимость", block)
        for phrase in (
            "QC ассистента",
            "техническое завершение задачи",
            "готовность пакета к генерации",
            "человеческая приёмка",
        ):
            self.assertIn(phrase, block)

    def test_new_scene_stays_one_package(self):
        done = section(self.guide, "## 15. Definition of Done", "## 16.")
        self.assertIn("Создать сцену с нуля", done)
        self.assertIn("Черновик и мудборд", done)
        self.assertIn("честный блокер", done)
        routine = section(self.sync, "## 4. Routine: добавить новую scene", "## 5. Routine")
        self.assertIn("`PROMPT-STYLE-GUIDE.md` §15", routine)
        self.assertIn("§11", routine)

    def test_topview_keeps_free_route_and_points_at_receipt(self):
        # Check the current free-route contract, not an obsolete exact sentence.
        # The owner's selected-free UI rule may clarify how zero cost is shown;
        # it must never remove the zero-cost and no-paid-launch boundaries.
        route = next(line for line in self.launch.splitlines()
                     if "Бесплатный маршрут обязателен:" in line)
        for required in ("720p, 16:9, один ролик", "бесплатный Unlimited",
                         "стоимость 0", "стоимость больше 0 блокируют"):
            self.assertIn(required, route)
        self.assertIn("`PROMPT-STYLE-GUIDE.md` §11.G", self.launch)
        self.assertIn("дословный отправленный промт", self.launch)
        self.assertIn("Кадр стыка не заменяет просмотр движения", self.launch)
        # The header can move and its checked date is expected to advance.
        headers = re.findall(r"^Статус: действует\. Проверено: (\d{2}\.\d{2}\.\d{4})\.$",
                             self.launch, re.M)
        self.assertEqual(len(headers), 1)
        datetime.strptime(headers[0], "%d.%m.%Y")

    def test_handoff_is_one_pointer_line(self):
        # A dated handoff entry is allowed to move to the documented history.
        # Keep one intact pointer, without restoring stale history to the live handoff.
        pointer = (
            "- **06.11.2026:** проверка пакета до готовности к генерации, фактическая отправка "
            "и просмотр ролика — `PROMPT-STYLE-GUIDE.md` §11 и §15, указатель запуска — "
            "`ops/TOPVIEW-FREE-LAUNCH.md`. Черновик и мудборд не равны готовому пакету."
        )
        self.assertIn("archive/handoff-log.md", self.handoff)
        lines = self.handoff.splitlines() + self.handoff_archive.splitlines()
        self.assertEqual(lines.count(pointer), 1)

    def test_free_route_guard_rejects_paid_or_multiple_outputs(self):
        for old, new in (("720p, 16:9, один ролик", "720p, 16:9, два ролика"),
                         ("бесплатный Unlimited", "платный режим"),
                         ("стоимость больше 0 блокируют", "стоимость больше 0 допускают")):
            with self.subTest(removed=old):
                original = self.launch
                try:
                    self.launch = original.replace(old, new)
                    self.assertNotEqual(self.launch, original)
                    with self.assertRaises(AssertionError):
                        self.test_topview_keeps_free_route_and_points_at_receipt()
                finally:
                    self.launch = original

    def test_handoff_pointer_guard_rejects_loss_or_duplication(self):
        original = self.handoff_archive
        pointer = next(line for line in original.splitlines()
                       if line.startswith("- **06.11.2026:** проверка пакета"))
        try:
            for changed in (original.replace(pointer, ""), original + "\n" + pointer):
                with self.subTest(duplicate=changed.endswith(pointer)):
                    self.handoff_archive = changed
                    with self.assertRaises(AssertionError):
                        self.test_handoff_is_one_pointer_line()
        finally:
            self.handoff_archive = original


if __name__ == "__main__":
    unittest.main()
