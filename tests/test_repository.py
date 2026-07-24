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
        cls.showcase_descriptions = load("catalog/showcase-descriptions.zh-CN.json")["descriptions"]

    def test_release_counts(self):
        first = sum(s["source"]["kind"] == "lianlin-first-party" for s in self.skills)
        third = sum(s["source"]["kind"] == "pinned-third-party" for s in self.skills)
        self.assertEqual((len(self.skills), len(self.categories), first, third), (187, 18, 10, 177))

    def test_academic_core_is_the_first_category(self):
        self.assertEqual(
            [category["order"] for category in self.categories],
            list(range(1, 19)),
        )
        self.assertEqual(self.categories[0]["id"], "academic-core")
        self.assertEqual(self.categories[0]["zh"], "学术核心能力")
        self.assertEqual(self.categories[0]["en"], "Academic Core")

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

    def test_chinese_readme_showcase_is_complete(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("首期明确只支持", readme)
        self.assertNotIn("固定第三方", readme)
        self.assertNotIn("上游能力说明", readme)
        self.assertNotIn("<sub>环境：", readme)
        self.assertEqual(readme.count('<a id="category-'), len(self.categories))
        self.assertEqual(readme.count("| [详细用法]("), len(self.skills))
        self.assertNotIn("**准备：**", readme)
        self.assertNotIn("**执行：**", readme)
        self.assertNotIn("**获得：**", readme)
        self.assertIn(
            "| 01 | [学术核心能力](#category-academic-core) | **10** | "
            "检索、精读、写作、审稿与证据治理工作流 |",
            readme,
        )
        self.assertLess(
            readme.index('<a id="category-academic-core"></a>'),
            readme.index('<a id="category-literature-management"></a>'),
        )
        third_party = [skill for skill in self.skills if skill["source"]["kind"] == "pinned-third-party"]
        self.assertEqual(set(self.showcase_descriptions), {skill["id"] for skill in third_party})
        self.assertEqual(readme.count("<strong>能力说明：</strong>"), len(third_party))
        for skill_id, description in self.showcase_descriptions.items():
            with self.subTest(skill=skill_id, field="showcase-description"):
                self.assertRegex(description, r"[\u3400-\u9fff]")
        for skill in self.skills:
            with self.subTest(skill=skill["id"]):
                self.assertIn(f"./{skill['paths']['zh-CN']}", readme)

    def test_chinese_quick_start_is_systematic_and_complete(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("## 立即开始", readme)
        self.assertLess(readme.index("## 你可以做什么"), readme.index("## 快速开始"))
        self.assertLess(
            readme.index("## 快速开始"),
            readme.index("## 不想本地安装？直接使用链邻科研 AI 平台"),
        )
        self.assertIn(
            "[不想本地安装？直接使用链邻科研 AI 平台](#lianlin-platform)",
            readme,
        )
        self.assertIn('<a id="lianlin-platform"></a>', readme)
        quick_start = readme.split("## 快速开始", 1)[1].split(
            "## 不想本地安装？直接使用链邻科研 AI 平台", 1
        )[0]
        for step in range(1, 7):
            self.assertIn(f"### 第 {step} 步", quick_start)
        for category in self.categories:
            self.assertIn(f"(#category-{category['id']})", quick_start)
        self.assertIn("研究目标、已有材料、任务范围、期望产出、质量要求", quick_start)
        self.assertIn("请从 LL-AcademicSkillsHub 中选择最合适的技能或技能组合", quick_start)
        self.assertIn("不补造缺失信息", quick_start)
        self.assertIn("分阶段检查比一次生成全部结果更容易发现", quick_start)

    def test_english_quick_start_matches_the_onboarding_structure(self):
        readme = (ROOT / "README.en.md").read_text(encoding="utf-8")
        self.assertLess(readme.index("## What you can do"), readme.index("## Quick start"))
        self.assertLess(
            readme.index("## Quick start"),
            readme.index(
                "## Don't want to install locally? Use Lianlin Research AI Platform"
            ),
        )
        self.assertIn(
            "[Don't want to install locally? Use Lianlin Research AI Platform]"
            "(#lianlin-platform)",
            readme,
        )
        quick_start = readme.split("## Quick start", 1)[1].split(
            "## Don't want to install locally? Use Lianlin Research AI Platform", 1
        )[0]
        for step in range(1, 7):
            self.assertIn(f"### Step {step}", quick_start)
        for category in self.categories:
            self.assertIn(category["en"], quick_start)
        self.assertIn(
            "research goal, available materials, task scope, expected output, "
            "and quality requirements",
            quick_start,
        )
        self.assertIn("do not invent missing information", quick_start)
        self.assertIn("Staged review makes evidence gaps", quick_start)

    def test_chinese_skill_guides_are_complete_and_unique(self):
        required_headings = [
            "## 1. 技能简介",
            "## 2. 适合用它做什么",
            "## 3. 工作方式",
            "## 4. 请求说明",
            "## 5. 示例预览",
            "## 6. 你需要提供",
            "## 7. 产出",
            "## 8. 内置参考",
            "## 9. 边界",
            "## 10. 相关技能",
            "## 11. 与其他技能的关系",
        ]
        documents = set()
        for skill in self.skills:
            path = ROOT / skill["paths"]["zh-CN"]
            text = path.read_text(encoding="utf-8")
            with self.subTest(skill=skill["id"]):
                self.assertTrue(text.startswith(f"# {skill['title']['zh-CN']}\n"))
                self.assertGreater(len(text), 1800)
                self.assertIn("[查看原始 SKILL](../SKILL.md)", text)
                self.assertNotIn("质量状态：", text)
                self.assertNotIn("来源类型：", text)
                outline = text.split("原始指令的重点阅读路径为：", 1)[1].split("。", 1)[0]
                self.assertNotRegex(outline, r"[A-Za-z]{4,}")
                for heading in required_headings:
                    self.assertEqual(text.count(heading), 1)
                skill_root = (ROOT / skill["paths"]["skill"]).parent
                for bundled in skill_root.rglob("*"):
                    if (
                        bundled.is_file()
                        and bundled.name != "SKILL.md"
                        and "locales" not in bundled.parts
                    ):
                        relative = bundled.relative_to(skill_root).as_posix()
                        self.assertIn(f"[`{relative}`](", text)
            documents.add(text)
        self.assertEqual(len(documents), len(self.skills))


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
