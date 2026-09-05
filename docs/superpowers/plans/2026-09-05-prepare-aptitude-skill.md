# Prepare Aptitude Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a standalone Aptitude plugin workflow that stages an existing skill as an Aptitude-compatible draft and replaces the source only after explicit approval.

**Architecture:** Keep the implementation documentation-only: one plugin skill reuses Resolver discovery for dependency research and native file operations for draft creation and replacement. Extend the existing plugin manifest, README, reporting contract, and one contract test; add no MCP server, conversion script, or Publisher invocation.

**Tech Stack:** Markdown agent skills, JSON plugin manifest, Python `unittest`, existing Resolver MCP tools.

**Spec:** `docs/superpowers/specs/2026-09-05-prepare-aptitude-skill-design.md`

## Global Constraints

- Create the converted copy at `<skill-root>/draft/`; do not modify the source before approval.
- Do not call Aptitude Publisher or run external evaluators.
- Do not read dotenv files, credentials, Publisher artifacts, or caches.
- Dependency discovery is advisory and every proposed relationship requires user review.
- Replacement requires an unchanged-source check, explicit approval, a sibling rollback backup, final-location validation, and automatic rollback on failure.
- Do not publish, release, update a marketplace, delete a successful backup, or commit without separate authorization.

---

### Task 1: Lock and implement the preparation workflow

**Files:**
- Create: `plugins/aptitude/skills/prepare-aptitude-skill/SKILL.md`
- Modify: `plugins/aptitude/skills/references/action-reporting.md`
- Modify: `plugins/aptitude/.codex-plugin/plugin.json`
- Modify: `README.md`
- Test: `tests/test_plugin.py`

**Interfaces:**
- Consumes: Resolver MCP tools `aptitude_search_skills` and `aptitude_inspect_skill`; native file inspection and editing tools.
- Produces: a discoverable `prepare-aptitude-skill` workflow and plugin version `0.1.10`.

- [ ] **Step 1: Write the failing plugin contract assertions**

Add `prepare-aptitude-skill` to the exact skill-name set in
`test_marketplace_manifest_and_skills_are_wired_to_public_interfaces`, then add:

```python
prepare_skill = (
    ROOT / "plugins/aptitude/skills/prepare-aptitude-skill/SKILL.md"
).read_text()
for phrase in (
    "name: prepare-aptitude-skill",
    "description: Use when",
    "<skill-root>/draft/",
    "aptitude.yaml",
    "aptitude_search_skills",
    "aptitude_inspect_skill",
    "README.md",
    "explicit approval",
    "source has not changed",
    "temporary sibling backup",
    "restore",
    "structural validation",
    "../references/action-reporting.md",
):
    self.assertIn(phrase, prepare_skill)
self.assertNotIn("aptitude_publisher_inspect_skill", prepare_skill)
self.assertNotIn("aptitude_publisher_publish_skill", prepare_skill)
self.assertLess(len(prepare_skill.split()), 500)
```

Update the manifest assertions to require version `0.1.10`, description
`"Prepare, inspect, publish, and install skills."`, short description
`"Prepare, inspect, publish, and install skills"`, and this first default prompt:

```python
"Prepare an existing skill for Aptitude"
```

Add `"prepare-aptitude-skill"` to the reporting-reference loop and require
`"aptitude_search_skills"`, `"aptitude_inspect_skill"`, and
`"prepare-aptitude-skill"` in the normalized reference.

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
UV_CACHE_DIR=.uv-cache uv run python -m unittest tests.test_plugin.AptitudePluginTests.test_marketplace_manifest_and_skills_are_wired_to_public_interfaces -v
```

Expected: FAIL because `prepare-aptitude-skill/SKILL.md` does not exist and the
manifest is still version `0.1.9`.

- [ ] **Step 3: Create the minimal workflow skill**

Create `plugins/aptitude/skills/prepare-aptitude-skill/SKILL.md` with this
behavioral contract:

```markdown
---
name: prepare-aptitude-skill
description: Use when adapting an existing agent skill that lacks Aptitude metadata or needs local Aptitude compatibility checks.
---

# Prepare an Aptitude Skill

Create a reviewable converted draft. Do not publish or run Aptitude Publisher.

## Instructions

1. Resolve the exact skill root and inspect `SKILL.md` plus non-secret supporting
   files. Do not read dotenv files, credentials, caches, Publisher artifacts, or
   an existing `draft/`.
2. Record the source file inventory and content checksums. Copy the useful skill
   package into `<skill-root>/draft/`; keep the source unchanged.
3. Normalize the draft:
   - Keep `name`, `description`, and supported standard fields such as `license`
     and `compatibility` in `SKILL.md` frontmatter.
   - Move `version`, `intent`, `tags`, `inputs_schema`, `outputs_schema`,
     `relationships`, `token_estimate`, `maturity_score`, and `security_score`
     into `aptitude.yaml`.
   - Require a semantic version and `create_skill` or `publish_version`. Check
     the registry before choosing intent; ask when identity remains ambiguous.
   - Move useful `README.md` material into `SKILL.md` or `references/`; do not
     leave `README.md` in the draft.
4. Search with `aptitude_search_skills` for capabilities related to the source.
   Inspect plausible matches with `aptitude_inspect_skill`. Propose exact or
   constrained relationships with reasons; do not add them until the user
   reviews the dependency set.
5. Run local structural validation: kebab-case folder/name match, required
   `SKILL.md`, non-empty trigger-oriented description, valid `aptitude.yaml`
   fields and types, valid semantic version/intent, valid relationship selectors,
   readable relative references, no unsafe links, and no forbidden `README.md`.
6. Preview source and draft paths, coordinate, intent, dependencies, changed or
   relocated files, structural validation, and warnings. Use the
   [shared action-reporting reference](../references/action-reporting.md). Ask for
   explicit approval before replacement.
7. After approval, verify the source has not changed from the recorded checksums.
   If changed, regenerate the draft and preview again. Otherwise move the draft
   to a temporary sibling path, move the source to a temporary sibling backup,
   and move the reviewed draft to the original source path.
8. Validate the final location. On failure, restore the backup and report the
   blocker. On success, keep the backup until the user separately authorizes
   deletion. The converted skill must not contain `draft/`.

## Example

For `skills/code-review/`, create `skills/code-review/draft/`, migrate Aptitude
fields to its `aptitude.yaml`, research relevant dependencies, and show the full
replacement preview. Only approval permits replacing `skills/code-review/`.

## Troubleshooting

- Missing version or uncertain registry identity: ask; do not invent it.
- Unsafe links or unreadable files: stop before drafting.
- Failed final validation: restore the sibling backup automatically.
```

- [ ] **Step 4: Extend shared action reporting**

Add `prepare-aptitude-skill` to the report action alternatives. Add a concise
preparation note requiring source path, draft path, proposed coordinate,
dependency suggestions, structural validation, warnings, and either no changes
before approval or the exact replacement/backup paths after approval.

- [ ] **Step 5: Update plugin discovery metadata**

In `plugins/aptitude/.codex-plugin/plugin.json`:

```json
"version": "0.1.10",
"description": "Prepare, inspect, publish, and install skills."
```

Set `interface.shortDescription` to
`"Prepare, inspect, publish, and install skills"`, update the long description
to mention adapting existing skills, and prepend
`"Prepare an existing skill for Aptitude"` to `interface.defaultPrompt`.

- [ ] **Step 6: Update the README workflow inventory**

Change the inventory to six workflows and add a “Prepare a skill” subsection
that states the workflow creates `<skill-root>/draft/`, uses registry discovery
for dependency suggestions, validates locally, and requires approval before
replacing the original. State that it neither invokes Publisher nor publishes.

- [ ] **Step 7: Run the focused test and verify GREEN**

Run the command from Step 2.

Expected: PASS.

---

### Task 2: Validate packaging and behavior

**Files:**
- Verify: `plugins/aptitude/skills/prepare-aptitude-skill/SKILL.md`
- Verify: `tests/test_plugin.py`
- Verify: `tests/smoke.sh`

**Interfaces:**
- Consumes: the completed workflow and plugin metadata from Task 1.
- Produces: static, package-level, and independent behavioral evidence.

- [ ] **Step 1: Validate the new skill structure**

Run:

```bash
python /Users/yonatan/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/aptitude/skills/prepare-aptitude-skill
```

Expected: validation succeeds with no scaffold placeholders.

- [ ] **Step 2: Run all plugin contract tests**

```bash
UV_CACHE_DIR=.uv-cache uv run python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 3: Run the plugin smoke test**

```bash
./tests/smoke.sh
```

Expected: exit `0` with Resolver MCP and Publisher command help available.

- [ ] **Step 4: Confirm Publisher is excluded from preparation**

```bash
rg -n "aptitude_publisher_(inspect|publish)_skill|confirm_upload" plugins/aptitude/skills/prepare-aptitude-skill
```

Expected: no matches.

- [ ] **Step 5: Forward-test the skill with an independent agent**

Dispatch `gpt-5.6-luna` at `xhigh` with the completed skill and the original
baseline scenario. Require a read-only response describing its actions.

Expected behavior:

- targets `plugins/aptitude/skills/prepare-aptitude-skill` as the workflow source;
- stages the converted package under the selected skill's `draft/`;
- creates sibling `aptitude.yaml` instead of nested Aptitude frontmatter;
- relocates useful `README.md` content and removes `README.md` from the draft;
- uses Resolver search/inspection only for dependency suggestions;
- keeps the source untouched until explicit approval;
- includes unchanged-source verification and rollback backup;
- never invokes Publisher or uploads to the registry.

- [ ] **Step 6: Inspect the final diff**

```bash
git diff --check
git status --short
git diff -- tests/test_plugin.py plugins/aptitude/skills/prepare-aptitude-skill/SKILL.md plugins/aptitude/skills/references/action-reporting.md plugins/aptitude/.codex-plugin/plugin.json README.md
```

Expected: no whitespace errors and only the approved spec, plan, workflow,
plugin metadata, reporting reference, README, and contract test are changed.
Do not commit without explicit authorization.
