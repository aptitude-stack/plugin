import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def parse_frontmatter(skill_text: str) -> dict[str, str]:
    if not skill_text.startswith("---\n"):
        raise AssertionError("skill is missing a YAML frontmatter block")
    parts = skill_text[4:].split("\n---\n", 1)
    if len(parts) != 2:
        raise AssertionError("skill is missing a YAML frontmatter closing fence")
    fields: dict[str, str] = {}
    for line in parts[0].splitlines():
        key, separator, value = line.partition(": ")
        if separator:
            fields[key] = value
    return fields


class AptitudePluginTests(unittest.TestCase):
    def test_marketplace_manifest_and_skills_are_wired_to_public_interfaces(self) -> None:
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        manifest = json.loads((ROOT / "plugins/aptitude/.codex-plugin/plugin.json").read_text())
        mcp = json.loads((ROOT / "plugins/aptitude/.mcp.json").read_text())

        self.assertEqual(marketplace["plugins"][0]["name"], "aptitude")
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./plugins/aptitude")
        self.assertEqual(manifest["name"], "aptitude")
        self.assertEqual(manifest["version"], "0.1.9")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["mcpServers"], "./.mcp.json")
        self.assertEqual(manifest["interface"]["logo"], "./assets/profile-logo.png")
        self.assertEqual(manifest["interface"]["composerIcon"], "./assets/profile-logo.png")
        self.assertTrue((ROOT / "plugins/aptitude/assets/profile-logo.png").is_file())
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
        self.assertIn(
            "without installing project/skill files or mutating the registry",
            readme,
        )
        self.assertNotIn("without file writes", readme)
        self.assertNotIn("resolves without file\nwithout installing", readme)
        self.assertEqual(
            mcp["mcpServers"]["resolver"],
            {
                "command": "uvx",
                "args": ["aptitude-resolver", "mcp"],
                "env_vars": ["APTITUDE_READ_TOKEN"],
            },
        )
        self.assertEqual(
            mcp["mcpServers"]["publisher"],
            {
                "command": "uvx",
                "args": ["aptitude-publisher", "mcp"],
                "env_vars": [
                    "APTITUDE_PUBLISH_TOKEN",
                    "APTITUDE_READ_TOKEN",
                    "APTITUDE_REGISTRY_URL",
                    "OPENAI_API_KEY",
                ],
            },
        )

        install_skill = (ROOT / "plugins/aptitude/skills/install-skill/SKILL.md").read_text()
        self.assertIn("../inspect-for-install/SKILL.md", install_skill)
        self.assertIn("aptitude_preview_install_destinations", install_skill)
        self.assertIn("aptitude_install_skill", install_skill)
        self.assertIn("explicit confirmation", install_skill)
        self.assertIn("user requests installing", install_skill)
        self.assertIn("select_slug", install_skill)
        self.assertIn('"select_slug": "<reviewed-slug>"', install_skill)
        self.assertIn('"version": "<reviewed-version>"', install_skill)
        self.assertIn('"query": "<reviewed-query>"', install_skill)
        self.assertIn('"agents": ["<preview-agent>"]', install_skill)
        self.assertIn('"scope": "<preview-scope>"', install_skill)
        self.assertIn('"cwd": "<preview-cwd>"', install_skill)
        self.assertIn('"export_root": null', install_skill)
        self.assertIn("No fresh unpinned resolution", install_skill)
        self.assertLess(
            install_skill.index("aptitude_preview_install_destinations"),
            install_skill.index("explicit confirmation"),
        )
        self.assertLess(
            install_skill.index("explicit confirmation"),
            install_skill.index("aptitude_install_skill"),
        )
        for inspection_tool in (
            "aptitude_search_skills",
            "aptitude_inspect_skill",
            "aptitude_resolve_skill",
        ):
            self.assertNotIn(inspection_tool, install_skill)

        publish_skill = (ROOT / "plugins/aptitude/skills/publish-skill/SKILL.md").read_text()
        self.assertIn("../inspect-for-publish/SKILL.md", publish_skill)
        self.assertIn("aptitude_publisher_publish_skill", publish_skill)
        self.assertIn("user requests publishing", publish_skill)
        self.assertIn('"confirm_upload": true', publish_skill)
        self.assertIn('"skill_path": "<skill-path>"', publish_skill)
        self.assertIn('"slug": "<evaluated-slug>"', publish_skill)
        self.assertIn('"version": "<reviewed-version>"', publish_skill)
        self.assertIn('"intent": "<evaluated-intent>"', publish_skill)
        self.assertIn("explicit confirmation", publish_skill)
        self.assertIn("fresh receipt", publish_skill)
        self.assertIn("stale", publish_skill)
        self.assertIn("auto-refresh", publish_skill)
        self.assertIn("approved plan", publish_skill)
        self.assertIn("exact confirmed identity still matches", publish_skill)
        self.assertIn("refreshed result is allowed", publish_skill)
        self.assertIn(
            "If identity changes or the result is blocked, do not upload",
            publish_skill,
        )
        self.assertIn("without a second confirmation", publish_skill)
        self.assertLess(
            publish_skill.index("auto-refresh"),
            publish_skill.index("aptitude_publisher_publish_skill"),
        )
        self.assertLess(
            publish_skill.index("explicit confirmation"),
            publish_skill.index("aptitude_publisher_publish_skill"),
        )
        self.assertIn('"registry_url": "<reviewed-registry-url>"', publish_skill)
        self.assertIn("registry target unchanged", publish_skill)
        self.assertNotIn("aptitude_publisher_inspect_skill", publish_skill)
        self.assertIn("Do not print, repeat, or store tokens", publish_skill)

        self.assertEqual(
            {
                path.parent.name
                for path in (ROOT / "plugins/aptitude/skills").glob("*/SKILL.md")
            },
            {
                "configure-resolver-preferences",
                "inspect-for-install",
                "inspect-for-publish",
                "install-skill",
                "publish-skill",
            },
        )

        inspect_publish = (
            ROOT / "plugins/aptitude/skills/inspect-for-publish/SKILL.md"
        ).read_text()
        self.assertLess(len(inspect_publish.split()), 500)
        for phrase in (
            "name: inspect-for-publish",
            "description: Use when",
            "aptitude_publisher_inspect_skill",
            "local",
            "does not upload",
            "does not mutate",
            "path",
            "coordinate",
            "intent",
            "validation",
            "gates",
            "maturity",
            "security",
            "overall",
            "out of 10",
            "performance",
            "non-persisted",
            "warnings",
            "receipt",
            "fresh",
            "reuse",
            "../references/action-reporting.md",
        ):
            self.assertIn(phrase, inspect_publish)
        self.assertNotIn("aptitude_publisher_publish_skill", inspect_publish)
        self.assertNotIn("confirm_upload", inspect_publish)
        self.assertNotRegex(inspect_publish.lower(), r"\btrust(?:_tier)?\b")

        inspect_install = (
            ROOT / "plugins/aptitude/skills/inspect-for-install/SKILL.md"
        ).read_text()
        self.assertLess(len(inspect_install.split()), 500)
        for phrase in (
            "name: inspect-for-install",
            "description: Use when",
            "aptitude_search_skills",
            "aptitude_inspect_skill",
            "aptitude_resolve_skill",
            "selected coordinate",
            "maturity",
            "security",
            "overall",
            "out of 10",
            "warnings",
            "policy outcome",
            "safe next step",
            "does not install skill/project files",
            "does not mutate the registry",
            "advisory cache",
            "../references/action-reporting.md",
        ):
            self.assertIn(phrase, inspect_install)
        self.assertNotIn("aptitude_install_skill", inspect_install)
        self.assertNotIn("There are no file writes", inspect_install)
        self.assertNotRegex(inspect_install.lower(), r"\btrust(?:_tier)?\b")
        self.assertIn("which one to install", inspect_install.lower())
        self.assertIn("purpose", inspect_install)
        self.assertIn("dependencies", inspect_install)
        self.assertIn("one combined", inspect_install)
        self.assertIn("target agents", inspect_install)
        self.assertIn("scope", inspect_install)
        self.assertIn("after the user selects", install_skill.lower())
        self.assertIn("preview", install_skill)
        self.assertIn("one approval", install_skill)
        self.assertIn("exact reviewed", install_skill)

        self.assertIn("which one to publish", inspect_publish.lower())
        self.assertIn("plausible local skill", inspect_publish)
        self.assertIn("registry target", inspect_publish)
        self.assertIn("after the user selects", publish_skill.lower())
        self.assertIn("preview", publish_skill)
        self.assertIn("one approval", publish_skill)
        self.assertIn("exact reviewed", publish_skill)

        self.assertIn(".publisher_artifacts/", inspect_publish)
        self.assertIn("inspection receipt", inspect_publish)
        self.assertIn("no upload or Registry mutation", inspect_publish)

        self.assertEqual(
            manifest["description"],
            "Inspect or publish local skills; inspect or install registry skills.",
        )
        self.assertEqual(
            manifest["interface"]["shortDescription"],
            "Inspect, publish, and install skills",
        )
        self.assertEqual(
            manifest["interface"]["defaultPrompt"],
            [
                "Inspect a local skill before publishing",
                "Publish a local skill to Aptitude",
                "Inspect a registry skill before installing",
                "Find and install an Aptitude skill",
            ],
        )

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

    def test_skill_frontmatter_names_and_descriptions(self) -> None:
        for skill_path in sorted((ROOT / "plugins/aptitude/skills").glob("*/SKILL.md")):
            metadata = parse_frontmatter(skill_path.read_text())
            self.assertEqual(metadata.get("name"), skill_path.parent.name)
            self.assertTrue(metadata.get("description", "").startswith("Use when "))
            self.assertNotIn("\n", metadata["description"])

    def test_skills_share_action_reporting_reference(self) -> None:
        reference_path = ROOT / "plugins/aptitude/skills/references/action-reporting.md"
        self.assertTrue(reference_path.is_file())
        reference = reference_path.read_text()
        normalized_reference = " ".join(reference.split())

        for skill_name in (
            "inspect-for-publish",
            "inspect-for-install",
            "publish-skill",
            "install-skill",
            "configure-resolver-preferences",
        ):
            skill = (ROOT / f"plugins/aptitude/skills/{skill_name}/SKILL.md").read_text()
            self.assertIn("../references/action-reporting.md", skill)

        for action in (
            "aptitude_publisher_inspect_skill",
            "aptitude_publisher_publish_skill",
            "aptitude_search_skills",
            "aptitude_inspect_skill",
            "aptitude_resolve_skill",
            "aptitude_preview_install_destinations",
            "aptitude_install_skill",
            "aptitude_show_policy",
        ):
            self.assertIn(action, normalized_reference)

        for phrase in (
            "Inspection is local and does not upload anything to the registry.",
            "`slug-name@vx.y.z`",
            "standalone version in backticks",
            "inspection result",
            "scores",
            "Initial read",
            "Edit",
            "Post-read",
            "selection field's source",
            "contributing layers",
            "### Report format",
            "Scores: <named canonical scores, or not scored; inspection actions when available>",
            "maturity, security, and overall scores are displayed out of 10",
            "machine-normalized values in the range [0,1]",
            "maturity_score",
            "security_score",
            "overall_score",
            "human-readable results render them as `/10`",
            "Performance evidence is non-persisted",
            "Do not report trust or trust_tier labels or fields",
            "allowed_trust_tiers",
            "**Action: <inspect-for-publish|inspect-for-install|publish|install|policy update>**",
            "- Target:",
            "- Result:",
            "- Inspection:",
            "- Scores:",
            "- Warnings:",
            "- Changes:",
            "Next:",
        ):
            self.assertIn(phrase, normalized_reference)

        self.assertIn("\n\nNext: <safe follow-up; omit when none>", reference)
        self.assertNotIn("\n- Next:", reference)

        self.assertNotIn("- Outcome:", normalized_reference)
        self.assertNotIn("- Action:", normalized_reference)
        self.assertNotIn("- Key result:", normalized_reference)
        self.assertNotIn("- Changes made:", normalized_reference)
        self.assertNotIn("publisher_artifacts", normalized_reference)

        self.assertIn(
            "Do not copy credentials, tokens, internal plans, or unrelated response fields.",
            normalized_reference,
        )
        self.assertIn("Do not report telemetry.", normalized_reference)
        for phase in (
            "Discover and select",
            "Preview",
            "Execute and report",
        ):
            self.assertIn(phase, normalized_reference)


if __name__ == "__main__":
    unittest.main()
