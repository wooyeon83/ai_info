import json
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import digest


NOW = datetime(2026, 11, 8, tzinfo=timezone.utc)


def item(url="https://example.com/release/1", age=1):
    return digest.Item("Example", "Release", url, NOW - timedelta(days=age), "Public notes")


class MemoryNotion:
    def __init__(self):
        self.keys = set()

    def exists(self, key):
        return key in self.keys

    def save(self, entry, summary, now):
        self.keys.add(entry.key)
        return {"url": "https://notion.so/saved"}


class DigestTests(unittest.TestCase):
    def test_korean_and_english_topic_matching_avoids_ai_substrings(self):
        self.assertTrue(digest.matches_keywords("생성형 에이전트를 적용했습니다", ["에이전트"]))
        self.assertTrue(digest.matches_keywords("AI-native and MCP tools", ["AI"]))
        self.assertFalse(digest.matches_keywords("email delivery details", ["AI"]))

    def test_rss_namespaced_date_and_content(self):
        feed = '''<rss xmlns:dc="http://purl.org/dc/elements/1.1/"
          xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel><item>
          <title>AI 적용 사례</title><link>https://example.com/ai</link>
          <dc:date>2026-11-07T00:00:00+09:00</dc:date>
          <content:encoded><![CDATA[<p>에이전트 활용</p>]]></content:encoded>
          </item></channel></rss>'''.encode()
        parsed = digest.parse_feed(feed, {"name": "Blog", "keywords": ["에이전트"]})
        self.assertEqual(parsed[0].body, "에이전트 활용")

    def test_atom_html_and_published_date(self):
        feed = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
        <title>v1</title><link rel="alternate" href="https://example.com/v1"/>
        <published>2026-11-07T00:00:00Z</published><updated>2026-11-08T00:00:00Z</updated>
        <content type="html">&lt;p&gt;New &amp;amp; improved&lt;/p&gt;</content>
        </entry></feed>'''
        parsed = digest.parse_feed(feed, {"name": "Example"})
        self.assertEqual(parsed[0].body, "New & improved")
        self.assertEqual(parsed[0].published, NOW - timedelta(days=1))

    def test_rss_filters_topics_and_handles_rfc_dates(self):
        feed = b'''<rss><channel><item><title>Agents</title>
        <link>https://example.com/agents</link><pubDate>Sat, 07 Nov 2026 00:00:00 GMT</pubDate>
        <description>New agent tools</description></item><item><title>Unrelated</title>
        <link>https://example.com/other</link><pubDate>Sat, 07 Nov 2026 00:00:00 GMT</pubDate>
        <description>Unrelated material</description></item></channel></rss>'''
        self.assertEqual(len(digest.parse_feed(feed, {"name": "Example", "keywords": ["agent"]})), 1)

    def test_malformed_feed_is_error_not_no_news(self):
        with self.assertRaises(digest.DigestError):
            digest.parse_feed(b"<html></html>", {"name": "Bad source"})

    def test_feed_with_stray_control_character_preserves_article(self):
        feed = '''<rss><channel><item><title>AI 사례</title>
        <link>https://example.com/ai</link><pubDate>Sat, 07 Nov 2026 00:00:00 GMT</pubDate>
        <description><![CDATA[<p>에이전트 활용</p><img alt="\x08워크플로우"/>]]></description>
        </item></channel></rss>'''.encode()
        parsed = digest.parse_feed(feed, {"name": "Blog"})
        self.assertEqual(parsed[0].body, "에이전트 활용")
        with self.assertRaises(digest.ET.ParseError):
            digest.parse_feed(b"<rss><channel></rss>", {"name": "Bad XML"})

    def test_backlog_filters_future_old_and_duplicate_items(self):
        items = [item(), item(), item("https://example.com/old", 15),
                 item("https://example.com/future", -1)]
        self.assertEqual(len(digest.candidates(items, NOW, 14)), 1)

    def test_rerun_does_not_pay_for_or_save_duplicates(self):
        notion = MemoryNotion()
        calls = []
        def summary(entry, mode):
            calls.append(entry.key)
            return {"summary": "Summary"}
        entries = [item(), item("https://example.com/2")]
        self.assertEqual(len(digest.deliver(entries, notion, "off", NOW, 1, summary)), 1)
        self.assertEqual(len(digest.deliver(entries, notion, "off", NOW, 1, summary)), 1)
        self.assertEqual(len(digest.deliver(entries, notion, "off", NOW, 3, summary)), 0)
        self.assertEqual(len(calls), 2)

    def test_partial_success_survives_later_failure(self):
        notion = MemoryNotion()
        saved = []
        def summary(entry, mode):
            if entry.url.endswith("2"):
                raise digest.DigestError("Temporary failure")
            return {"summary": "Summary"}
        with self.assertRaises(digest.DigestError):
            digest.deliver([item(), item("https://example.com/2")], notion, "off", NOW, 3,
                           summary, saved=saved)
        self.assertEqual(len(saved), 1)
        self.assertTrue(notion.exists(item().key))

    def test_notion_payload_includes_dedup_key_and_no_verified_claim(self):
        client = digest.Notion("dummy-test-token", "dummy-source")
        summary = digest.summarize(item(), "off")
        with patch.object(client, "api", return_value={"url": "https://notion.so/test"}) as api:
            client.save(item(), summary, NOW)
        payload = api.call_args.args[1]
        self.assertEqual(payload["parent"]["type"], "data_source_id")
        self.assertEqual(payload["properties"]["항목 ID"]["rich_text"][0]["text"]["content"], item().key)
        self.assertEqual(payload["properties"]["학습 상태"]["select"]["name"], "미확인")

    def test_ai_invalid_json_never_reaches_delivery(self):
        response = json.dumps({"content": [{"type": "text", "text": "not JSON"}]}).encode()
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test", "ANTHROPIC_MODEL": "test"}), \
                patch.object(digest, "request", return_value=response):
            with self.assertRaises(digest.DigestError):
                digest.summarize(item(), "anthropic")


if __name__ == "__main__":
    unittest.main()
