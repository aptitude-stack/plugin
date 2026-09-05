# Streamlined Install and Publish Dialogs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Aptitude installation and publication use symmetric candidate selection, one exact preview, and one post-preview approval.

**Architecture:** Keep the existing five skills and shared reporting reference. Tighten their written contracts rather than adding code or abstractions: discovery owns candidate presentation and combined target selection, inspection/resolution owns the non-mutating preview, and the mutation skill reuses the exact reviewed inputs after one approval.

**Tech Stack:** Markdown agent skills, JSON plugin manifest, Python `unittest` contract tests.

---

### Task 1: Lock the streamlined interaction contract

**Files:**
- Modify: `tests/test_plugin.py`

- [x] **Step 1: Write failing contract assertions**

Add assertions to `test_marketplace_manifest_and_skills_are_wired_to_public_interfaces` requiring:

```python
self.assertIn("which one to install", inspect_install.lower())
self.assertIn("purpose", inspect_install)
self.assertIn("dependencies", inspect_install)
self.assertIn("one combined", inspect_install)
self.assertIn("target agents", inspect_install)
self.assertIn("scope", inspect_install)
self.assertIn("after the user selects", install_skill)
self.assertIn("preview", install_skill)
self.assertIn("one approval", install_skill)
self.assertIn("exact reviewed", install_skill)

self.assertIn("which one to publish", inspect_publish.lower())
self.assertIn("plausible local skill", inspect_publish)
self.assertIn("registry target", inspect_publish)
self.assertIn("after the user selects", publish_skill)
self.assertIn("preview", publish_skill)
self.assertIn("one approval", publish_skill)
self.assertIn("exact reviewed", publish_skill)
```

Also assert that the shared reference names the common three phases and the plugin version is `0.1.9`.

- [x] **Step 2: Run the focused test and verify RED**

Run:

```bash
UV_CACHE_DIR=.uv-cache uv run python -m unittest tests.test_plugin.AptitudePluginTests.test_marketplace_manifest_and_skills_are_wired_to_public_interfaces -v
```

Expected: FAIL because the current skills require separate destination questions and do not define symmetric candidate-first publication.

### Task 2: Implement the minimum skill-contract changes

**Files:**
- Modify: `plugins/aptitude/skills/inspect-for-install/SKILL.md`
- Modify: `plugins/aptitude/skills/install-skill/SKILL.md`
- Modify: `plugins/aptitude/skills/inspect-for-publish/SKILL.md`
- Modify: `plugins/aptitude/skills/publish-skill/SKILL.md`
- Modify: `plugins/aptitude/skills/references/action-reporting.md`
- Modify: `plugins/aptitude/.codex-plugin/plugin.json`

- [x] **Step 1: Make installation candidate-first**

Change `inspect-for-install` to show each candidate's purpose, scores, warnings,
dependencies, and fit. Its only selection prompt collects the candidate, target
agents, and project/global/custom destination inputs together. It must not
resolve, preview, or install before selection.

- [x] **Step 2: Make the selected installation preview-first**

Change `install-skill` to inspect and resolve only after selection, call
`aptitude_preview_install_destinations`, show the exact coordinate, dependency
plan, agents, scope, paths, and warnings, then ask for one approval. Install
with exactly those reviewed inputs and report changes or blockers.

- [x] **Step 3: Make publication symmetric**

Change `inspect-for-publish` to discover plausible local skill directories,
show each candidate's purpose and available identity, and ask once for the path
and registry target. After selection, inspect without upload and show the exact
path, slug, version, intent, target, scores, gates, and warnings.

Change `publish-skill` to treat that inspection report as the publication
preview, ask for one approval, then publish the exact reviewed identity and
target. Preserve the existing stale-receipt and identity-change safeguards.

- [x] **Step 4: Align shared reporting and version**

Document the common `Discover and select` → `Preview` → `Execute and report`
phases in `action-reporting.md`. Keep `Next:` outside the bullet list. Bump
`plugin.json` to `0.1.9`.

- [x] **Step 5: Run the focused test and verify GREEN**

Run the focused command from Task 1. Expected: PASS.

### Task 3: Verify the packaged plugin

**Files:**
- Test: `tests/test_plugin.py`
- Test: `tests/smoke.sh`

- [x] **Step 1: Run all contract tests**

```bash
UV_CACHE_DIR=.uv-cache uv run python -m unittest discover -s tests -v
```

Expected: 3 tests pass.

- [x] **Step 2: Run the smoke test**

```bash
./tests/smoke.sh
```

Expected: exit 0 with Resolver MCP and Publisher command help available.

- [x] **Step 3: Check the diff**

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only the approved plugin contract, tests,
manifest, spec, and plan are changed. Do not commit without explicit user
authorization.
