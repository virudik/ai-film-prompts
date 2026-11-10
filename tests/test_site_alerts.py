"""Grok is told about a changed warn/fail set, not about unchanged info notes."""
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import site_alerts  # noqa: E402


NOW = datetime(2026, 11, 10, 1, 50, tzinfo=timezone.utc)


def write(root, rel, data):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


class AlertTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "ops").mkdir()
        (self.root / "ops" / "relay-wake.json").write_text(json.dumps({
            "enabled": True, "api_base": "https://cast.agentrelay.com/v1",
            "address": "chatgpt@example", "site_alert_enabled": True,
            "site_alert_address": "GrokBot@example"}), encoding="utf-8")
        self.sent = []

    def sender(self, text):
        self.sent.append(text)
        return "sent", "message_id=1"

    def base(self, **extra):
        checked = (NOW - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        write(self.root, "topview-status.json", {"checked_at": checked, "occupied_slots": 6, "free_slots": 0})
        write(self.root, "automation-monitor-status.json", {
            "last_scheduled_cycle": {"completed_at": checked, "health": "ok", "note": "ok"}})
        write(self.root, "project-status.json", {"health": "ok"})
        write(self.root, "instruction-sync-status.json", {"health": "ok"})
        write(self.root, "canon-health.json", extra.get("health") or {"problems": []})

    def test_info_notes_do_not_notify_and_the_same_warn_does_not_repeat(self):
        self.base(health={"problems": [
            {"level": "info", "code": "ops-stale", "file": "ops/X.md", "text": "воскресная чистка"},
            {"level": "warn", "code": "handoff-size", "file": "NEW-CHAT-HANDOFF.md", "text": "Хендоф 35 КБ"},
        ]})
        first = site_alerts.notify(self.root, NOW, self.sender)
        self.assertEqual(first["action"], "sent")
        self.assertEqual(len(self.sent), 1)
        self.assertIn("Хендоф 35 КБ", self.sent[0])
        self.assertNotIn("воскресная чистка", self.sent[0])
        again = site_alerts.notify(self.root, NOW, self.sender)
        self.assertEqual((again["action"], len(self.sent)), ("unchanged", 1))

    def test_stale_topview_is_one_stable_banner_and_a_fresh_file_clears_it(self):
        self.base()
        old = (NOW - timedelta(hours=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        write(self.root, "topview-status.json", {"checked_at": old})
        self.assertEqual(site_alerts.notify(self.root, NOW, self.sender)["action"], "sent")
        self.assertIn("ДАННЫЕ TOPVIEW УСТАРЕЛИ", self.sent[0])
        later = NOW + timedelta(minutes=30)
        write(self.root, "topview-status.json", {"checked_at": later.strftime("%Y-%m-%dT%H:%M:%SZ")})
        # Same stale condition five minutes later must not be a new set.
        self.sent.clear()
        write(self.root, "topview-status.json", {"checked_at": old})
        self.assertEqual(site_alerts.notify(self.root, later, self.sender)["action"], "unchanged")
        fresh = (later - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
        write(self.root, "topview-status.json", {"checked_at": fresh})
        self.assertEqual(site_alerts.notify(self.root, later, self.sender)["action"], "cleared")
        self.assertEqual(self.sent, [])

    def test_a_failed_delivery_does_not_count_as_sent(self):
        self.base(health={"problems": [{"level": "warn", "code": "handoff-size", "file": "H.md", "text": "большой"}]})
        result = site_alerts.notify(self.root, NOW, lambda text: ("no_token", "secret AGENT_RELAY_TOKEN is not set"))
        self.assertEqual(result["action"], "no_token")
        self.assertFalse((self.root / "ops" / "site-alert-state.json").exists())


class NavDefaultTests(unittest.TestCase):
    def test_phone_filters_start_open_and_can_still_collapse(self):
        html = Path(__file__).resolve().parents[1].joinpath("index.html").read_text(encoding="utf-8")
        self.assertIn('class="side side-open"', html)
        self.assertIn('aria-expanded="true"', html)
        self.assertIn("✕ Скрыть фильтры и оглавление", html)
        media = html.split("@media(max-width:820px)", 1)[1].split("@media", 1)[0]
        self.assertIn(".side:not(.side-open) #filters", media)
        self.assertIn(".side:not(.side-open) #toc", media)
        self.assertLess(html.find(".side-toggle{display:none}"), html.find("@media(max-width:820px)"))

    def test_unmapped_slot_is_not_rendered_as_scene_zero(self):
        html = Path(__file__).resolve().parents[1].joinpath("index.html").read_text(encoding="utf-8")
        now = html.split("function renderNowView", 1)[1].split("function instructionLabel", 1)[0]
        finished = html.split("function finishedTopviewRows", 1)[1].split("function renderTopview", 1)[0]
        self.assertIn("sceneNum(x)", now)
        self.assertIn("слот без сцены", now)
        self.assertIn("id==null", now)
        self.assertNotIn("Number(x.scene_id)", now)
        self.assertNotIn("#scene-0", now)
        self.assertIn("sceneNum", finished)
        self.assertNotIn("Number(x.scene_id)", finished)


if __name__ == "__main__":
    unittest.main()
