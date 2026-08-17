# Configure Resolver Preferences Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one Aptitude plugin skill that safely configures resolver selection preferences and restrictive client policy.

**Architecture:** The new standalone skill uses the released resolver MCP policy-report tool as the read/verify surface and directs agents to make a confirmed, scope-specific `aptitude.toml` edit. A focused unit test locks in the discovery and safety instructions; no publisher skill is added because publisher has no personalized policy.

**Tech Stack:** Markdown Agent Skill, Python `unittest`, released Aptitude resolver MCP.

---

### Task 1: Establish the skill-test baseline

**Files:**
- Test: `plugin/tests/test_plugin.py`

- [ ] **Step 1: Run a no-skill baseline scenario with a fresh agent**

Ask the agent: “A user wants Aptitude to prefer verified skills but not be prompted in this repository. Configure it quickly.” Record whether it distinguishes soft selection from hard policy, asks for scope and confirmation, preserves TOML, and verifies the effective result.

- [ ] **Step 2: Add the failing plugin contract test**

```python
preferences_skill = (
    ROOT / "plugins/aptitude/skills/configure-resolver-preferences/SKILL.md"
).read_text()
self.assertIn("aptitude_show_policy", preferences_skill)
self.assertIn("user or workspace", preferences_skill)
self.assertIn("explicit confirmation", preferences_skill)
self.assertIn("[selection]", preferences_skill)
self.assertIn("[policy]", preferences_skill)
self.assertIn("never silently broaden", preferences_skill)
```

- [ ] **Step 3: Run the focused test to verify it fails**

Run from `plugin`: `UV_CACHE_DIR=.uv-cache uv run python -m unittest tests.test_plugin.AptitudePluginTests.test_marketplace_manifest_and_skills_are_wired_to_public_interfaces`

Expected: FAIL because the new skill path does not exist.

### Task 2: Add the minimum resolver-preferences skill

**Files:**
- Create: `plugin/plugins/aptitude/skills/configure-resolver-preferences/SKILL.md`

- [ ] **Step 1: Create the skill with searchable frontmatter**

```markdown
---
name: configure-resolver-preferences
description: Use when changing Aptitude resolver selection preferences or local client policy in user or workspace aptitude.toml.
---
```

- [ ] **Step 2: Add the confirmed configuration workflow**

Include `aptitude_show_policy` before and after the edit; ask for user or workspace scope and explicit confirmation; distinguish `[selection]` from `[policy]`; preserve unrelated TOML; and forbid silently broadening policy.

- [ ] **Step 3: Run the focused test to verify it passes**

Run from `plugin`: `UV_CACHE_DIR=.uv-cache uv run python -m unittest tests.test_plugin.AptitudePluginTests.test_marketplace_manifest_and_skills_are_wired_to_public_interfaces`

Expected: PASS.

### Task 3: Verify the skill is usable

**Files:**
- Test: `plugin/tests/test_plugin.py`

- [ ] **Step 1: Run the same scenario with the skill available**

Verify the agent first inspects effective policy, asks scope/confirmation, uses `[selection]` for `high-trust` ranking preference and `[policy]` only if the user asks to restrict legality, then verifies the result.

- [ ] **Step 2: Run the full plugin test suite and static checks**

Run from `plugin`: `UV_CACHE_DIR=.uv-cache uv run python -m unittest discover -s tests -v && git diff --check`

Expected: all tests pass and no whitespace errors.

- [ ] **Step 3: Inspect the final diff**

Run: `git -C plugin status --short && git -C plugin diff --check`

Expected: only the new skill, its test assertion, and the pre-existing user version-bump changes are present. Do not commit because workspace instructions require explicit authorization.
