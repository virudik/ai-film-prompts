"""Узкая проверка уточнений QA пакета: роли, отправка, квитанция, просмотр ролика."""
import re
import unittest
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
        self.assertIn("720p, 16:9, один ролик, unlimited, стоимость 0", self.launch)
        self.assertIn("`PROMPT-STYLE-GUIDE.md` §11.G", self.launch)
        self.assertIn("дословный отправленный промт", self.launch)
        self.assertIn("Кадр стыка не заменяет просмотр движения", self.launch)
        self.assertIn("Проверено: 06.11.2026", self.launch.splitlines()[6])

    def test_handoff_is_one_pointer_line(self):
        lines = [x for x in self.handoff.splitlines() if x.startswith("- **06.11.2026:**")]
        self.assertEqual(lines, [
            "- **06.11.2026:** проверка пакета до готовности к генерации, фактическая отправка "
            "и просмотр ролика — `PROMPT-STYLE-GUIDE.md` §11 и §15, указатель запуска — "
            "`ops/TOPVIEW-FREE-LAUNCH.md`. Черновик и мудборд не равны готовому пакету."
        ])


if __name__ == "__main__":
    unittest.main()
