import unittest
from datetime import datetime, timezone

from app.utils import parse_device, parse_ts, summarize

CHROME = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
IPAD = "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
ANDROID_PHONE = "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Mobile Safari/537.36"
ANDROID_TABLET = "Mozilla/5.0 (Linux; Android 13; SM-X700) AppleWebKit/537.36 Safari/537.36"


class TestParseDevice(unittest.TestCase):
    def test_classification(self):
        self.assertEqual(parse_device(CHROME), "desktop")
        self.assertEqual(parse_device(IPHONE), "mobile")
        self.assertEqual(parse_device(IPAD), "tablet")
        self.assertEqual(parse_device(ANDROID_PHONE), "mobile")
        self.assertEqual(parse_device(ANDROID_TABLET), "tablet")
        self.assertEqual(parse_device("curl/8.4.0"), "bot")
        self.assertEqual(parse_device("k6/0.50.0"), "bot")
        self.assertEqual(parse_device("Googlebot/2.1"), "bot")
        self.assertEqual(parse_device(""), "unknown")
        self.assertEqual(parse_device(None), "unknown")


class TestSummarize(unittest.TestCase):
    def test_parse_ts_assumes_utc(self):
        self.assertEqual(parse_ts("2026-11-25T10:00:00").tzinfo, timezone.utc)
        self.assertEqual(parse_ts("2026-11-25T10:00:00+00:00").hour, 10)

    def test_summarize(self):
        utc = timezone.utc
        clicks = [
            {"ts": datetime(2026, 11, 24, 23, 0, tzinfo=utc), "device": "mobile", "user_agent": "a"},
            {"ts": datetime(2026, 11, 25, 1, 0, tzinfo=utc), "device": "desktop", "user_agent": "b"},
            {"ts": datetime(2026, 11, 25, 9, 0, tzinfo=utc), "device": "mobile", "user_agent": "c"},
        ]
        s = summarize("abc", clicks, recent_n=2)
        self.assertEqual(s["total"], 3)
        self.assertEqual(s["by_day"], [{"date": "2026-11-24", "clicks": 1}, {"date": "2026-11-25", "clicks": 2}])
        self.assertEqual(s["by_device"], {"mobile": 2, "desktop": 1})
        self.assertEqual([r["user_agent"] for r in s["recent"]], ["c", "b"])
        self.assertFalse(s["truncated"])

    def test_summarize_empty(self):
        s = summarize("x", [])
        self.assertEqual(s["total"], 0)
        self.assertEqual(s["by_day"], [])
        self.assertEqual(s["recent"], [])


if __name__ == "__main__":
    unittest.main()
