from __future__ import annotations

import functools
import importlib.util
import json
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.categories = load("catalog/categories.seed.json")
        cls.skills = load("catalog/skills.seed.json")

    def test_release_counts(self):
        first = sum(s["source"]["kind"] == "lianlin-first-party" for s in self.skills)
        third = sum(s["source"]["kind"] == "pinned-third-party" for s in self.skills)
        self.assertEqual((len(self.skills), len(self.categories), first, third), (187, 18, 10, 177))

    def test_ids_and_paths_are_unique_and_present(self):
        ids = [s["id"] for s in self.skills]
        self.assertEqual(len(ids), len(set(ids)))
        for skill in self.skills:
            for relative in skill["paths"].values():
                with self.subTest(skill=skill["id"], path=relative):
                    self.assertTrue((ROOT / relative).is_file())

    def test_bilingual_fields_have_parity(self):
        for skill in self.skills:
            for field in ("title", "summary", "capabilities", "inputs", "outputs"):
                with self.subTest(skill=skill["id"], field=field):
                    self.assertEqual(set(skill[field]), {"zh-CN", "en"})
                    self.assertTrue(skill[field]["zh-CN"])
                    self.assertTrue(skill[field]["en"])

    def test_forced_ad_skill_is_absent(self):
        self.assertNotIn("offer-k-dense-web", {s["id"] for s in self.skills})

    def test_site_catalog_matches_canonical(self):
        site = load("site/data/catalog.json")
        self.assertEqual(site["summary"]["skillCount"], len(self.skills))
        self.assertEqual(site["summary"]["categoryCount"], len(self.categories))
        self.assertEqual({s["id"] for s in site["skills"]}, {s["id"] for s in self.skills})

    def test_first_party_frontmatter_and_locales(self):
        for skill in (s for s in self.skills if s["source"]["kind"] == "lianlin-first-party"):
            skill_path = ROOT / skill["paths"]["skill"]
            text = skill_path.read_text(encoding="utf-8")
            header = text.split("---", 2)[1]
            keys = {line.split(":", 1)[0] for line in header.splitlines() if ":" in line}
            with self.subTest(skill=skill["id"]):
                self.assertEqual(keys, {"name", "description"})
                self.assertIn(f"name: {skill['id']}", header)
                self.assertIn("## Workflow", text)


class LocalServerSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("ll_serve", ROOT / "scripts" / "serve.py")
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        handler = functools.partial(module.SafeRepositoryHandler, directory=str(ROOT))
        cls.server = module.http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def fetch_status(self, path: str) -> int:
        request = urllib.request.Request(f"http://127.0.0.1:{self.port}{path}")
        opener = urllib.request.build_opener(NoRedirect())
        try:
            with opener.open(request, timeout=3) as response:
                return response.status
        except urllib.error.HTTPError as error:
            return error.code

    def test_published_site_is_served(self):
        self.assertEqual(self.fetch_status("/site/"), 200)
        self.assertEqual(self.fetch_status("/site/data/catalog.json"), 200)
        self.assertEqual(self.fetch_status("/skills/academic-core/ll-paper-search/SKILL.md"), 200)

    def test_root_redirects_to_site(self):
        self.assertEqual(self.fetch_status("/"), 302)

    def test_sensitive_and_internal_paths_are_blocked(self):
        for path in ("/.env", "/.git/config", "/scripts/serve.py", "/catalog/skills.seed.json", "/reports/audit.json"):
            with self.subTest(path=path):
                self.assertEqual(self.fetch_status(path), 404)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


if __name__ == "__main__":
    unittest.main()
