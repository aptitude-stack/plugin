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
        self.assertEqual(manifest["version"], "0.1.2")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["mcpServers"], "./.mcp.json")
        self.assertEqual(manifest["interface"]["logo"], "./assets/logo.png")
        self.assertEqual(manifest["interface"]["composerIcon"], "./assets/logo.png")
        self.assertTrue((ROOT / "plugins/aptitude/assets/logo.png").is_file())
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
        readme = (ROOT / "README.md").read_text()
        self.assertIn(
            "--sparse .agents/plugins --sparse plugins/aptitude",
            readme,
        )
        self.assertEqual(
            mcp["mcpServers"]["aptitude"],
            {
                "command": "uvx",
                "args": ["aptitude-resolver", "mcp"],
                "env_vars": ["APTITUDE_READ_TOKEN"],
            },
        )
        self.assertEqual(
            mcp["mcpServers"]["aptitude-publisher"],
            {
                "command": "uvx",
                "args": ["aptitude-publisher", "mcp"],
                "env_vars": [
                    "APTITUDE_PUBLISH_TOKEN",
                    "APTITUDE_READ_TOKEN",
                    "APTITUDE_REGISTRY_URL",
                ],
            },
        )

        install_skill = (ROOT / "plugins/aptitude/skills/install-skill/SKILL.md").read_text()
        self.assertIn("aptitude_preview_install_destinations", install_skill)
        self.assertIn("aptitude_install_skill", install_skill)
        self.assertIn("explicit confirmation", install_skill)
        self.assertNotIn("aptitude install", install_skill)

        publish_skill = (ROOT / "plugins/aptitude/skills/publish-skill/SKILL.md").read_text()
        self.assertIn("aptitude_publisher_inspect_skill", publish_skill)
        self.assertIn("aptitude_publisher_publish_skill", publish_skill)
        self.assertIn('"confirm_upload": true', publish_skill)
        self.assertIn("explicit confirmation", publish_skill)
        self.assertIn("Do not print, repeat, or store tokens", publish_skill)

        preferences_skill = (
            ROOT / "plugins/aptitude/skills/configure-resolver-preferences/SKILL.md"
        ).read_text()
        self.assertIn("aptitude_show_policy", preferences_skill)
        self.assertIn("name: configure-resolver-preferences", preferences_skill)
        self.assertIn(
            "description: Use when changing Aptitude resolver selection preferences",
            preferences_skill,
        )
        self.assertIn("user or workspace", preferences_skill)
        self.assertIn("explicit confirmation", preferences_skill)
        self.assertIn("[selection]", preferences_skill)
        self.assertIn("[policy]", preferences_skill)
        self.assertIn("never silently broaden", preferences_skill)
        self.assertIn('"response_format": "json"', preferences_skill)
        self.assertIn('"cwd"', preferences_skill)
        self.assertIn("allowed_trust_tiers", preferences_skill)
        self.assertIn("allowed_lifecycle_statuses", preferences_skill)
        self.assertIn("max_token_estimate", preferences_skill)
        self.assertIn("max_content_size_bytes", preferences_skill)
        self.assertIn("max_total_token_estimate", preferences_skill)
        self.assertIn("max_total_content_size_bytes", preferences_skill)
        self.assertIn("Preserve unrelated TOML fields", preferences_skill)
        self.assertLess(
            preferences_skill.index("aptitude_show_policy"),
            preferences_skill.index("explicit confirmation"),
        )
        self.assertLess(
            preferences_skill.index("explicit confirmation"),
            preferences_skill.rindex("aptitude_show_policy"),
        )
        self.assertIn(
            'Call `aptitude_show_policy` again with the same `cwd` and\n'
            '   `response_format: "json"`.',
            preferences_skill,
        )
        self.assertIn("selection field's source", preferences_skill)
        self.assertIn("aggregate policy source", preferences_skill)
        self.assertIn("contributing layers", preferences_skill)
        post_edit_report = "After the second policy call, report effective selection"
        self.assertIn(post_edit_report, preferences_skill)
        self.assertLess(
            preferences_skill.rindex("aptitude_show_policy"),
            preferences_skill.index(post_edit_report),
        )


if __name__ == "__main__":
    unittest.main()
