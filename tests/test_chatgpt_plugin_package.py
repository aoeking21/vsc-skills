import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "vsc"


class ChatGPTPluginPackageTests(unittest.TestCase):
    def test_marketplace_points_to_vsc_plugin(self):
        data = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text())
        self.assertEqual(data["name"], "vsc-plugins")
        entry = next(item for item in data["plugins"] if item["name"] == "vsc")
        self.assertEqual(entry["source"], {"source": "local", "path": "./plugins/vsc"})
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
        self.assertIn(entry["policy"]["authentication"], {"ON_INSTALL", "ON_USE"})

    def test_openai_manifests_are_complete(self):
        portable = json.loads((PLUGIN / "plugin.json").read_text())
        native = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())

        self.assertEqual(portable["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertEqual(portable["name"], "vsc")
        self.assertRegex(portable["version"], r"^\d+\.\d+\.\d+$")
        self.assertNotIn("skills", portable)
        self.assertNotIn("interface", portable)
        self.assertTrue((PLUGIN / "skills").is_dir())

        self.assertEqual(native["name"], portable["name"])
        self.assertEqual(native["version"], portable["version"])
        self.assertEqual(native["description"], portable["description"])
        self.assertEqual(native["skills"], "./skills/")

        portable_interface = portable["extensions"]["com.openai"]["interface"]
        native_interface = native["interface"]
        self.assertEqual(portable_interface, native_interface)
        for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
            self.assertTrue(portable_interface[key])
        for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
            self.assertTrue(portable_interface[key].startswith("https://"))
        self.assertLessEqual(len(portable_interface["defaultPrompt"]), 3)
        self.assertTrue(all(len(item) <= 128 for item in portable_interface["defaultPrompt"]))

    def test_router_has_chatgpt_hard_gate(self):
        router = (PLUGIN / "skills" / "vsc" / "SKILL.md").read_text()
        for trigger in ("@vsc创作入口", "$vsc", "/vsc", "严格模式"):
            self.assertIn(trigger, router)
        self.assertIn("不得静默跳过 VSC 后直接调用普通生图", router)
        self.assertIn("用户追问“调用 skill 了吗”", router)

    def test_all_catalog_skills_are_packaged_and_discoverable(self):
        skills_root = PLUGIN / "skills"
        script = skills_root / "vsc" / "scripts" / "discover_skills.py"
        result = subprocess.run(
            [sys.executable, str(script), "--root", str(skills_root)],
            check=True,
            text=True,
            capture_output=True,
        )
        discovered = json.loads(result.stdout)["skills"]
        self.assertTrue(discovered)
        for item in discovered:
            self.assertEqual(item["status"], "available", item)
            self.assertFalse(item.get("needs_review", False), item)


if __name__ == "__main__":
    unittest.main()
