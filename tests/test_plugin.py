import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class AptitudePluginTests(unittest.TestCase):
    def test_marketplace_manifest_and_skills_are_wired_to_public_interfaces(self) -> None:
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        manifest = json.loads((ROOT / "plugins/aptitude/.codex-plugin/plugin.json").read_text())
        mcp = json.loads((ROOT / "plugins/aptitude/.mcp.json").read_text())

        self.assertEqual(marketplace["plugins"][0]["name"], "aptitude")
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./plugins/aptitude")
        self.assertEqual(manifest["name"], "aptitude")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["mcpServers"], "./.mcp.json")
        self.assertEqual(manifest["interface"]["logo"], "./assets/logo.svg")
        self.assertEqual(manifest["interface"]["composerIcon"], "./assets/logo.svg")
        self.assertTrue((ROOT / "plugins/aptitude/assets/logo.svg").is_file())
        self.assertEqual(
            manifest["interface"]["privacyPolicyURL"],
            "https://github.com/aptitude-stack/plugin/blob/main/PRIVACY.md",
        )
        self.assertEqual(
            manifest["interface"]["termsOfServiceURL"],
            "https://github.com/aptitude-stack/plugin/blob/main/TERMS.md",
        )
        self.assertTrue((ROOT / "PRIVACY.md").is_file())
        self.assertTrue((ROOT / "TERMS.md").is_file())
        self.assertTrue((ROOT / "tests/smoke.sh").is_file())
        self.assertEqual(
            mcp["mcpServers"]["aptitude"],
            {
                "command": "uvx",
                "args": ["aptitude-resolver", "mcp"],
                "env_vars": ["APTITUDE_READ_TOKEN"],
            },
        )

        install_skill = (ROOT / "plugins/aptitude/skills/install-skill/SKILL.md").read_text()
        self.assertIn("aptitude_preview_install_destinations", install_skill)
        self.assertIn("aptitude_install_skill", install_skill)
        self.assertIn("explicit confirmation", install_skill)
        self.assertNotIn("aptitude install", install_skill)

        publish_skill = (ROOT / "plugins/aptitude/skills/publish-skill/SKILL.md").read_text()
        self.assertIn("uvx aptitude-publisher inspect", publish_skill)
        self.assertIn("uvx aptitude-publisher publish", publish_skill)
        self.assertIn("explicit confirmation", publish_skill)
        self.assertIn("Do not print, repeat, or store tokens", publish_skill)


if __name__ == "__main__":
    unittest.main()
