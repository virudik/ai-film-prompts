import importlib.util, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

spec = importlib.util.spec_from_file_location("canon_lock", Path(__file__).resolve().parents[1] / "scripts" / "canon_lock.py")
cl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cl)

T = datetime(2026, 10, 17, 18, 0, tzinfo=timezone.utc)


class CanonLockTest(unittest.TestCase):
    def test_missing_or_free_lock_is_free(self):
        self.assertFalse(cl.is_held({}, T))
        self.assertFalse(cl.is_held({"state": "free"}, T))

    def test_acquire_then_other_writer_is_refused(self):
        lock = cl.acquire({}, "chatgpt", "очередь", 45, T)
        self.assertTrue(cl.is_held(lock, T))
        with self.assertRaises(RuntimeError):
            cl.acquire(lock, "claude", "правка мастера", 45, T + timedelta(minutes=10))

    def test_expired_lock_can_be_taken(self):
        lock = cl.acquire({}, "chatgpt", "очередь", 45, T)
        later = T + timedelta(minutes=46)
        self.assertFalse(cl.is_held(lock, later))
        self.assertEqual(cl.acquire(lock, "claude", "x", 30, later)["holder"], "claude")

    def test_holder_extends_and_keeps_start(self):
        lock = cl.acquire({}, "claude", "x", 45, T)
        ext = cl.acquire(lock, "claude", "x", 45, T + timedelta(minutes=30))
        self.assertEqual(ext["acquired_at"], lock["acquired_at"])
        self.assertGreater(cl.parse(ext["expires_at"]), cl.parse(lock["expires_at"]))

    def test_minutes_are_capped(self):
        lock = cl.acquire({}, "claude", "x", 10000, T)
        self.assertEqual(cl.parse(lock["expires_at"]), T + timedelta(minutes=cl.MAX_MINUTES))

    def test_release_only_by_holder(self):
        lock = cl.acquire({}, "chatgpt", "x", 45, T)
        with self.assertRaises(RuntimeError):
            cl.release(lock, "claude", T)
        freed = cl.release(lock, "chatgpt", T)
        self.assertFalse(cl.is_held(freed, T))

    def test_repository_lock_file_is_valid(self):
        repo = Path(__file__).resolve().parents[1]
        lock = cl.read(repo)
        self.assertIn(lock.get("state"), ("free", "held"))
        if lock["state"] == "held":
            self.assertIsNotNone(cl.parse(lock.get("expires_at")))


if __name__ == "__main__":
    unittest.main()
