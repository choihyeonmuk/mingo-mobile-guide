#!/usr/bin/env python3
"""Offline structural/link and report-fidelity checks; no network required."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from render_report import SOURCE, TARGET, build, inline, render  # noqa: E402


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.elements, self.text = [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)

    def attrs(self, tag):
        return [attrs for name, attrs in self.elements if name == tag]


def normalize(text):
    return " ".join(text.split())


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {path: Page(path.read_text(encoding="utf-8")) for path in
                     [ROOT / "index.html", ROOT / "mobile.html", TARGET]}

    def test_semantics_and_skip_links(self):
        for path, page in self.pages.items():
            with self.subTest(page=path.name):
                self.assertEqual(page.attrs("html")[0].get("lang"), "ko")
                self.assertEqual(len(page.attrs("main")), 1)
                self.assertEqual(page.attrs("main")[0].get("id"), "main")
                self.assertEqual(len(page.attrs("h1")), 1)
                self.assertTrue(page.attrs("title"))
                self.assertTrue(page.attrs("header"))
                self.assertTrue(page.attrs("footer"))
                self.assertTrue(any(a.get("href") == "#main" for a in page.attrs("a")))
                self.assertTrue(any(m.get("name") == "viewport" for m in page.attrs("meta")))
                ids = [a["id"] for _, a in page.elements if "id" in a]
                self.assertEqual(len(ids), len(set(ids)), "duplicate ID")

    def test_internal_links_assets_and_anchors(self):
        checked = 0
        for path, page in self.pages.items():
            for tag, attrs in page.elements:
                for attribute in ("href", "src"):
                    value = attrs.get(attribute)
                    if value is None:
                        continue
                    parsed = urlsplit(value)
                    if parsed.scheme or parsed.netloc:
                        self.assertIn(parsed.scheme, ("http", "https"))
                        continue
                    with self.subTest(page=path.name, link=value):
                        self.assertFalse(value.startswith("/"), "must work at Pages subpath")
                        self.assertTrue(value)
                        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                        self.assertTrue(target.is_relative_to(ROOT), "outside site root")
                        self.assertTrue(target.is_file(), f"missing {value}")
                        if parsed.fragment:
                            target_page = self.pages.get(target) or Page(target.read_text(encoding="utf-8"))
                            self.assertIn(unquote(parsed.fragment), [a.get("id") for _, a in target_page.elements])
                        checked += 1
        self.assertGreater(checked, 20)

    def test_full_report_matches_source(self):
        source = SOURCE.read_text(encoding="utf-8")
        self.assertEqual(TARGET.read_text(encoding="utf-8"), build(source), "run tools/render_report.py")
        # Join text nodes without separators: inline <strong>/<em> split words,
        # and a space join would invent whitespace the browser never renders.
        visible = normalize("".join(self.pages[TARGET].text))
        for line in source.splitlines():
            line = re.sub(r"^(?:#{1,6} |>|- |\d+\. )\s*", "", line).replace("**", "").strip()
            if line and line != "---":
                self.assertIn(normalize(line), visible)
        self.assertIn("2026-11-10", visible)
        self.assertIn("2026-11-14", visible)
        self.assertIn("기술선정 제안 / 구현 전 검토", visible)

    def test_report_toc_and_source_download(self):
        page = self.pages[TARGET]
        _, headings = render(SOURCE.read_text(encoding="utf-8"))
        self.assertEqual(len(headings), 10)
        for anchor, _ in headings:
            self.assertTrue(any(a.get("href") == "#" + anchor for a in page.attrs("a")))
        self.assertTrue(any(a.get("href") == SOURCE.name and "download" in a for a in page.attrs("a")))

    def test_existing_apk_preserved(self):
        expected = "https://expo.dev/artifacts/eas/D10cQNuM06lpQvPUGpzkoNafRk5pHOhT-XoEkKPHYfo.apk"
        page = self.pages[ROOT / "mobile.html"]
        self.assertEqual([a["href"] for a in page.attrs("a") if a.get("href", "").endswith(".apk")], [expected])
        self.assertTrue(any(a.get("href") == "index.html" for a in page.attrs("a")))

    def test_no_runtime_js_or_new_remote_styles(self):
        for path, page in self.pages.items():
            self.assertFalse(page.attrs("script"), path.name)
            if path.name != "mobile.html":
                self.assertTrue(page.attrs("nav"))
                self.assertTrue(all(not a.get("href", "").startswith("http") for a in page.attrs("link")))
        css = (ROOT / "assets/workbench.css").read_text(encoding="utf-8")
        self.assertIn(":focus-visible", css)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn("overflow-wrap:anywhere", css)

    def test_renderer_escapes_raw_html(self):
        dangerous = '<script>alert("x")</script>'
        self.assertNotIn("<script>", inline(dangerous))
        self.assertIn("&lt;script&gt;", inline(dangerous))
        self.assertEqual(inline("**강조** *기울임* `코드`"), "<strong>강조</strong> <em>기울임</em> <code>코드</code>")
        self.assertIn('href="https://example.org/?a=1&amp;b=2"', inline("https://example.org/?a=1&b=2"))
        self.assertNotIn('href="javascript:', inline("javascript:alert(1)"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
